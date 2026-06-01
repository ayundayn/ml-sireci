import pandas as pd
import numpy as np
from typing import List
from collections import Counter
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
        similar_users = self.get_similar_users(user_id, top_n=30)

        if not similar_users:
            return []

        if user_id not in self.user_item_matrix.index:
            return []

        # item yang sudah pernah dirating user aktif
        current_user_items = set(
            self.user_item_matrix.loc[user_id]
            [self.user_item_matrix.loc[user_id] > 0]
            .index
        )

        recommended_items = []

        for similar_user in similar_users:

            user_items = self.user_item_matrix.loc[similar_user]

            top_items = user_items[
                user_items > 0
            ].nlargest(top_n).index.tolist()

            # buang item yang sudah pernah dirating user
            top_items = [
                item for item in top_items
                if item not in current_user_items
            ]

            recommended_items.extend(top_items)

        counter = Counter(recommended_items)

        return [
            item
            for item, _ in counter.most_common()
        ]

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
            (self.df['kategori'].isin(kategori)) &
            (
                (self.df['htm_min_domestik'] <= budget_max) &
                (self.df['htm_max_domestik'] >= budget_min)
            ) &
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
