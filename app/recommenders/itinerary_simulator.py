from datetime import datetime, timedelta, time as dt_time
import random


class ItinerarySimulator:

    def __init__(
        self,
        df_places,
        df_kuliner,
        df_jarak,
        df_waktu,
        total_days=1,
        start_time="08:00:00",
        end_time="20:00:00",
        max_budget=1000000,
        base_code=None
    ):

        self.df_places = df_places
        self.df_kuliner = df_kuliner

        self.df_jarak = df_jarak
        self.df_waktu = df_waktu

        self.total_days = total_days

        self.start_time = self.itinerary_time(start_time)
        self.end_time = self.itinerary_time(end_time)

        self.max_budget = max_budget

        self.base_code = base_code

    # =====================================================
    # CONVERT TIME
    # =====================================================

    def itinerary_time(self, value):

        if value is None:
            value = "08:00:00"

        if isinstance(value, str):

            try:

                t = datetime.strptime(
                    value,
                    "%H:%M:%S"
                ).time()

            except:

                t = datetime.strptime(
                    value,
                    "%H:%M"
                ).time()

        elif isinstance(value, datetime):

            t = value.time()

        elif isinstance(value, dt_time):

            t = value

        else:

            t = datetime.strptime(
                "08:00:00",
                "%H:%M:%S"
            ).time()

        return datetime.combine(
            datetime.now().date(),
            t
        )

    # =====================================================
    # CULINARY CHECK
    # =====================================================

    def should_insert_culinary(self, current_time):

        lunch_start = self.itinerary_time("11:00:00")
        lunch_end = self.itinerary_time("13:00:00")

        dinner_start = self.itinerary_time("18:00:00")
        dinner_end = self.itinerary_time("20:00:00")

        current = self.itinerary_time(
            current_time.strftime("%H:%M:%S")
        )

        # jam makan siang / malam
        if (
            lunch_start <= current <= lunch_end
        ) or (
            dinner_start <= current <= dinner_end
        ):
            return True

        # setelah makan siang sebelum malam
        if lunch_end < current < dinner_start:
            return True

        # lewat malam
        if current > dinner_end:
            return True

        return False

    # =====================================================
    # FITNESS
    # =====================================================

    def fuzzy_budget_violation(
        self,
        total_cost,
        budget,
        tolerance=0.2
    ):

        if total_cost <= budget:
            return 0.0

        elif total_cost <= budget * (
            1 + tolerance
        ):

            return (
                total_cost - budget
            ) / (
                budget * tolerance
            )

        else:
            return 1.0

    def fuzzy_time_window_violation(self, x):

        if x <= 0:
            return 0.0

        elif 0 < x <= 120:
            return x / 120

        else:
            return 1.0

    def fitness_function(
        self,
        TW_prime,
        D,
        B_prime,
        alpha=0.4,
        gamma=0.3,
        delta=0.3
    ):

        return (
            alpha * (1 - TW_prime)
            +
            gamma * (1 / (1 + D))
            +
            delta * (1 - B_prime)
        )

    # =====================================================
    # SIMULATE
    # =====================================================

    def simulate(self, order):

        itinerary = {
            d: []
            for d in range(
                1,
                self.total_days + 1
            )
        }

        day = 1

        current_time = self.start_time

        total_budget = 0
        total_distance = 0

        tw_violation = 0

        last_place = self.base_code

        for i in range(len(order)):

            if day > self.total_days:
                break

            idx = order[i]

            next_idx = (
                order[i + 1]
                if i + 1 < len(order)
                else None
            )

            row = self.df_places.iloc[idx]

            place_id = row["place_id"]

            place_type = row["place_type"]

            name = row["nama_tempat"]

            open_time = row["jam_buka"]

            close_time = row["jam_tutup"]

            price = row["harga"]

            duration = row["durasi"]

            # =====================================================
            # TRAVEL
            # =====================================================

            if last_place is not None:

                try:

                    travel_distance = self.df_jarak.loc[
                        last_place,
                        place_id
                    ]

                    travel_time = self.df_waktu.loc[
                        last_place,
                        place_id
                    ]

                except:

                    travel_distance = 0
                    travel_time = 0

            else:

                travel_distance = 0
                travel_time = 0

            current_time += timedelta(
                minutes=int(travel_time)
            )

            total_distance += float(
                travel_distance
            )

            # =====================================================
            # PINDAH HARI
            # =====================================================

            if current_time + timedelta(
                minutes=int(duration)
            ) > self.end_time:

                day += 1

                if day > self.total_days:
                    break

                current_time = self.start_time

                last_place = self.base_code

            # =====================================================
            # INSERT KULINER
            # =====================================================

            if self.should_insert_culinary(
                current_time
            ):

                if not self.df_kuliner.empty:

                    resto = self.df_kuliner.sample(
                        1
                    ).iloc[0]

                    resto_id = resto["place_id"]

                    try:

                        resto_distance = self.df_jarak.loc[
                            last_place,
                            resto_id
                        ]

                        resto_time = self.df_waktu.loc[
                            last_place,
                            resto_id
                        ]

                    except:

                        resto_distance = 0
                        resto_time = 0

                    current_time += timedelta(
                        minutes=int(resto_time)
                    )

                    total_distance += float(
                        resto_distance
                    )

                    r_open = self.itinerary_time(
                        resto["jam_buka"]
                    )

                    r_close = self.itinerary_time(
                        resto["jam_tutup"]
                    )

                    if current_time < r_open:

                        diff = (
                            r_open - current_time
                        ).total_seconds() / 60

                        tw_violation += diff

                        current_time = r_open

                    elif current_time > r_close:

                        tw_violation += 120

                    if current_time + timedelta(
                        minutes=60
                    ) <= r_close:

                        start_r = current_time

                        leave_r = (
                            current_time
                            +
                            timedelta(minutes=60)
                        )

                        itinerary[day].append({

                            "place_id": str(resto_id),

                            "type": "kuliner",

                            "name": resto[
                                "nama_tempat"
                            ],
                            
                            "kategori": resto[
                                "kategori"
                            ],

                            "alamat": resto[
                                "alamat"
                            ],

                            "start": start_r.strftime(
                                "%H:%M"
                            ),

                            "end": leave_r.strftime(
                                "%H:%M"
                            )
                        })

                        total_budget += resto[
                            "harga"
                        ]

                        current_time = leave_r

                        last_place = resto_id

                        # lanjut ke next wisata
                        if next_idx is not None:

                            next_place = (
                                self.df_places.iloc[
                                    next_idx
                                ]
                            )

                            next_place_id = next_place[
                                "place_id"
                            ]

                            try:

                                next_time = (
                                    self.df_waktu.loc[
                                        last_place,
                                        next_place_id
                                    ]
                                )

                                current_time += timedelta(
                                    minutes=int(
                                        next_time
                                    )
                                )

                            except:
                                pass

            # =====================================================
            # OPEN CLOSE WISATA
            # =====================================================

            open_dt = self.itinerary_time(
                open_time
            )

            close_dt = self.itinerary_time(
                close_time
            )

            if current_time < open_dt:

                diff = (
                    open_dt - current_time
                ).total_seconds() / 60

                tw_violation += diff

                current_time = open_dt

            elif current_time > close_dt:

                tw_violation += 120

                continue

            # =====================================================
            # TAMBAH ITINERARY
            # =====================================================

            start = current_time

            leave = current_time + timedelta(
                minutes=int(duration)
            )

            itinerary[day].append({

                "place_id": str(place_id),

                "type": place_type,

                "name": name,
                
                "kategori": row["kategori"],

                "alamat": row["alamat"],

                "start": start.strftime("%H:%M"),

                "end": leave.strftime("%H:%M")
            })

            total_budget += price

            current_time = leave

            last_place = place_id

        # =====================================================
        # FITNESS
        # =====================================================

        budget_violation = (
            self.fuzzy_budget_violation(
                total_budget,
                self.max_budget
            )
        )

        tw_violation = (
            self.fuzzy_time_window_violation(
                tw_violation
            )
        )

        fitness = self.fitness_function(
            tw_violation,
            total_distance,
            budget_violation
        )

        return (
            itinerary,
            fitness,
            total_budget,
            total_distance
        )