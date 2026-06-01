import pandas as pd

from app.recommenders.genetic_algorithm import (
    GeneticAlgorithm
)


class ItineraryEngine:

    def __init__(self, data_loader):

        self.data_loader = data_loader

        (
            self.df_wisata,
            self.df_kuliner,
            self.df_jarak,
            self.df_waktu
        ) = self.data_loader.load_all()

    def generate(
        self,
        wisata_ids,
        kuliner_ids,
        total_hari,
        budget=1000000,
        start_time="08:00",
        end_time="20:00"
    ):

        df_wisata = self.data_loader.load_wisata()

        df_kuliner = self.data_loader.load_kuliner()

        df_jarak = self.data_loader.load_jarak()

        df_waktu = self.data_loader.load_waktu()
        
        # =========================
        # FILTER DESTINASI USER
        # =========================

        df_wisata = self.data_loader.load_wisata()
        df_kuliner = self.data_loader.load_kuliner()
        df_jarak = self.data_loader.load_jarak()
        df_waktu = self.data_loader.load_waktu()
        
        wisata_selected = df_wisata[
            df_wisata["wisata_id"].isin(
                wisata_ids
            )
        ].copy()

        kuliner_selected = df_kuliner[
            df_kuliner["kuliner_id"].isin(
                kuliner_ids
            )
        ].copy()

        # =========================
        # TAMBAH TYPE
        # =========================

        wisata_selected["place_type"] = "wisata"

        kuliner_selected["place_type"] = "kuliner"

        # =========================
        # SAMAKAN ID
        # =========================

        wisata_selected["place_id"] = (
            "W" + wisata_selected["wisata_id"].astype(str)
        )

        kuliner_selected["place_id"] = (
            "K" + kuliner_selected["kuliner_id"].astype(str)
        )

        # =========================
        # SAMAKAN HARGA
        # =========================

        wisata_selected["harga"] = wisata_selected[
            "htm_max_domestik"
        ].fillna(0)

        kuliner_selected["harga"] = kuliner_selected[
            "htm_max"
        ].fillna(0)

        # =========================
        # DURASI DEFAULT
        # =========================

        wisata_selected["durasi"] = 120

        kuliner_selected["durasi"] = 60

        # =========================
        # AMBIL KOLOM YANG DIPAKAI
        # =========================

        wisata_selected = wisata_selected[
            [
                "place_id",
                "place_type",
                "nama_tempat",
                "kategori",
                "alamat",
                "jam_buka",
                "jam_tutup",
                "harga",
                "durasi"
            ]
        ]

        kuliner_selected = kuliner_selected[
            [
                "place_id",
                "place_type",
                "nama_tempat",
                "kategori",
                "alamat",
                "jam_buka",
                "jam_tutup",
                "harga",
                "durasi"
            ]
        ]

        # =========================
        # DF PLACES = WISATA SAJA
        # =========================

        df_places = wisata_selected.copy()

        # =========================
        # DF KULINER TERPISAH
        # =========================

        df_kuliner = kuliner_selected.copy()

        # =========================
        # JALANKAN GA
        # =========================

        ga = GeneticAlgorithm(
            df_places=df_places,
            df_kuliner=df_kuliner,
            df_jarak=df_jarak,
            df_waktu=df_waktu,
            total_days=total_hari,
            max_budget=budget,
            start_time=start_time,
            end_time=end_time
        )

        itinerary, fitness, total_budget, total_distance = ga.run()

        # =========================
        # RESPONSE
        # =========================

        return {
            "itinerary": itinerary,
            "fitness": fitness,
            "total_budget": total_budget,
            "total_distance": total_distance
        }