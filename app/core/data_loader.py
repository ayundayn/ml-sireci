import pandas as pd
import pymysql
from app.config import settings
# from app.database import SessionLocal
# from app.models import Wisata, Kuliner


class DataLoader:
    """Load dan manage dataset kuliner & wisata dari MySQL"""

    def __init__(self):
        self.kuliner_df = None
        self.wisata_df = None
        # self.db = SessionLocal()

    def _get_connection(self):
        """Get MySQL connection"""
        return pymysql.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_database
        )

    def load_kuliner(self) -> pd.DataFrame:
        """Load dataset kuliner dari MySQL"""
        conn = self._get_connection()

        query = '''
        SELECT
            k.kuliner_id,
            k.kategori_kuliner_id,
            kk.nama_kategori as kategori,
            k.nama_tempat,
            k.jam_buka,
            k.jam_tutup,
            k.alamat,
            k.lokasi_geo,
            k.htm_min,
            k.htm_max,
            k.rating
        FROM kuliner k
        JOIN kategori_kuliner kk ON k.kategori_kuliner_id = kk.kategori_kuliner_id
        '''

        self.kuliner_df = pd.read_sql(query, conn)
        conn.close()

        return self._preprocess_kuliner(self.kuliner_df)

    def load_wisata(self) -> pd.DataFrame:
        """Load dataset wisata dari MySQL"""
        conn = self._get_connection()

        query = '''
        SELECT
            w.wisata_id,
            w.kategori_wisata_id,
            kw.nama_kategori as kategori,
            w.nama_tempat,
            w.jam_buka,
            w.jam_tutup,
            w.alamat,
            w.lokasi_geo,
            w.htm_min_domestik,
            w.htm_max_domestik,
            w.htm_min_mancanegara,
            w.htm_max_mancanegara,
            w.akses_transportasi,
            w.rating
        FROM wisata w
        JOIN kategori_wisata kw ON w.kategori_wisata_id = kw.kategori_wisata_id
        '''

        self.wisata_df = pd.read_sql(query, conn)
        conn.close()

        return self._preprocess_wisata(self.wisata_df)

    def load_ratings_kuliner(self) -> pd.DataFrame:
        """Load rating kuliner dari MySQL"""
        conn = self._get_connection()

        query = '''
        SELECT
            rk.user_id,
            k.nama_tempat as kuliner,
            rk.nilai_rating as rating
        FROM rating_kuliner rk
        JOIN kuliner k
            ON rk.kuliner_id = k.kuliner_id

        UNION ALL

        SELECT
            fk.user_id,
            k.nama_tempat as kuliner,
            5.0 as rating
        FROM favorit_kuliner fk
        JOIN kuliner k
            ON fk.kuliner_id = k.kuliner_id

        ORDER BY user_id
        '''

        df = pd.read_sql(query, conn)
        conn.close()

        return df

    def load_ratings_wisata(self) -> pd.DataFrame:
        """Load rating wisata dari MySQL"""
        conn = self._get_connection()

        query = '''
        SELECT
            rw.user_id,
            w.nama_tempat as wisata,
            rw.nilai_rating as rating
        FROM rating_wisata rw
        JOIN wisata w
            ON rw.wisata_id = w.wisata_id

        UNION ALL

        SELECT
            fw.user_id,
            w.nama_tempat as wisata,
            5.0 as rating
        FROM favorit_wisata fw
        JOIN wisata w
            ON fw.wisata_id = w.wisata_id

        ORDER BY user_id
        '''

        df = pd.read_sql(query, conn)
        conn.close()

        return df

    def _preprocess_kuliner(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocessing dataset kuliner"""
        df = df.copy()

        # Add default rating column (kuliner table doesn't have rating in DB)
        if 'rating' not in df.columns:
            df['rating'] = 0.0
        else:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

        # Ensure numeric columns
        df['htm_min'] = pd.to_numeric(df['htm_min'], errors='coerce').fillna(0.0)
        df['htm_max'] = pd.to_numeric(df['htm_max'], errors='coerce').fillna(0.0)

        # Remove duplicates based on nama_tempat, keep first occurrence
        df = df.drop_duplicates(subset='nama_tempat', keep='first')

        return df

    def _preprocess_wisata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocessing dataset wisata"""
        df = df.copy()

        # Ensure rating is numeric
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

        # Ensure numeric columns
        df['htm_min_domestik'] = pd.to_numeric(df['htm_min_domestik'], errors='coerce').fillna(0.0)
        df['htm_max_domestik'] = pd.to_numeric(df['htm_max_domestik'], errors='coerce').fillna(0.0)
        df['htm_min_mancanegara'] = pd.to_numeric(df['htm_min_mancanegara'], errors='coerce').fillna(0.0)
        df['htm_max_mancanegara'] = pd.to_numeric(df['htm_max_mancanegara'], errors='coerce').fillna(0.0)

        # Remove duplicates based on nama_tempat, keep first occurrence
        df = df.drop_duplicates(subset='nama_tempat', keep='first')

        return df
    
    def load_jarak(self):
        return pd.read_excel("app/datasets/dataset_jarak.xlsx", index_col=0)

    def load_waktu(self):
        return pd.read_excel("app/datasets/dataset_waktu.xlsx", index_col=0)

    def load_all(self):

        df_wisata = self.load_wisata()
        df_kuliner = self.load_kuliner()

        df_jarak = self.load_jarak()
        df_waktu = self.load_waktu()

        return (
            df_wisata,
            df_kuliner,
            df_jarak,
            df_waktu
        )
    