import pandas as pd
import numpy as np
from typing import List
from .base import BaseRecommender


class WisataRecommender(BaseRecommender):
    """Recommender system untuk wisata"""

    def __init__(self):
        super().__init__()
        self._item_column = 'wisata'
        self._name_column = 'nama_tempat'

    def build_user_item_matrix(self, ratings_df: pd.DataFrame):
        """Build user-item matrix untuk wisata"""
        return self.train_collaborative_filtering(ratings_df)

    def recommend_cf(self, user_id: int, top_n: int = 10) -> list:
        """Get CF recommendations untuk wisata"""
        similar_users = self.get_similar_users(user_id, top_n=5)

        if not similar_users:
            return []

        # Get items rated by similar users
        recommended_items = []
        for similar_user in similar_users:
            user_items = self.user_item_matrix.loc[similar_user]
            top_items = user_items[user_items > 0].nlargest(top_n).index.tolist()
            recommended_items.extend(top_items)

        return list(set(recommended_items))[:top_n]

    def recommend_content_based(
        self,
        item_list: List[str],
        kategori: List[str],
        budget_min: float,
        budget_max: float,
        rating_min: float,
        top_n: int = 10
    ) -> pd.DataFrame:
        """Content-based filtering untuk wisata"""
        filtered = self.df[
            (self.df[self._name_column].isin(item_list)) &
            (self.df['kategori_wisata_id'].isin(kategori)) &
            (self.df['htm_min_domestik'] >= budget_min) &
            (self.df['htm_max_domestik'] <= budget_max) &
            (self.df['rating'] >= rating_min)
        ]

        result = filtered.sort_values(by='rating', ascending=False).head(top_n)

        # Add recommendation score
        if not result.empty:
            max_rating = result['rating'].max()
            result['skor_rekomendasi'] = (result['rating'] / max_rating).round(2)
        else:
            result = pd.DataFrame()

        return result
