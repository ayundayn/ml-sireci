import pandas as pd
import os
from app.config import settings


class DataLoader:
    """Load dan manage dataset kuliner & wisata"""

    def __init__(self):
        self.kuliner_df = None
        self.wisata_df = None

    def load_kuliner(self) -> pd.DataFrame:
        """Load dataset kuliner dari CSV"""
        path = os.path.join(settings.data_dir, "kuliner.csv")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset kuliner tidak ditemukan: {path}")

        self.kuliner_df = pd.read_csv(path)
        return self._preprocess_kuliner(self.kuliner_df)

    def load_wisata(self) -> pd.DataFrame:
        """Load dataset wisata dari CSV"""
        path = os.path.join(settings.data_dir, "wisata.csv")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset wisata tidak ditemukan: {path}")

        self.wisata_df = pd.read_csv(path)
        return self._preprocess_wisata(self.wisata_df)

    def _preprocess_kuliner(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocessing dataset kuliner"""
        df = df.copy()

        # Clean rating column
        df['rating'] = df['rating'].astype(str).str.replace(',', '.')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

        # Ensure numeric columns
        df['htm_min'] = pd.to_numeric(df['htm_min'], errors='coerce').fillna(0.0)
        df['htm_max'] = pd.to_numeric(df['htm_max'], errors='coerce').fillna(0.0)

        return df

    def _preprocess_wisata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocessing dataset wisata"""
        df = df.copy()

        # Clean rating column
        df['rating'] = df['rating'].astype(str).str.replace(',', '.')
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

        # Ensure numeric columns
        df['htm_min_domestik'] = pd.to_numeric(df['htm_min_domestik'], errors='coerce').fillna(0.0)
        df['htm_max_domestik'] = pd.to_numeric(df['htm_max_domestik'], errors='coerce').fillna(0.0)
        df['htm_min_mancanegara'] = pd.to_numeric(df['htm_min_mancanegara'], errors='coerce').fillna(0.0)
        df['htm_max_mancanegara'] = pd.to_numeric(df['htm_max_mancanegara'], errors='coerce').fillna(0.0)

        return df
