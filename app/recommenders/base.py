from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class BaseRecommender(ABC):
    """Base class untuk recommender systems"""

    def __init__(self):
        self.df = None
        self.user_item_matrix = None
        self.similarity_matrix = None

    def load_data(self, df: pd.DataFrame):
        """Load dataset"""
        self.df = df

    @abstractmethod
    def build_user_item_matrix(self, ratings_df: pd.DataFrame):
        """Build user-item interaction matrix"""
        pass

    def train_collaborative_filtering(self, ratings_df: pd.DataFrame):
        """Train collaborative filtering model"""
        interaction = self._create_interaction_data(ratings_df)
        self.user_item_matrix = self._build_matrix(interaction)

        # Calculate similarity
        self.similarity_matrix = cosine_similarity(self.user_item_matrix)

        return self.similarity_matrix

    def _create_interaction_data(self, ratings_df: pd.DataFrame):
        """Create interaction data from ratings"""
        interaction = ratings_df.copy()
        interaction['score'] = interaction['rating']
        return interaction

    def _build_matrix(self, interaction_df: pd.DataFrame):
        """Build user-item matrix"""
        matrix = interaction_df.pivot_table(
            index='user_id',
            columns=self._item_column,
            values='rating'
        ).fillna(0)
        return matrix

    def get_similar_users(self, user_id: int, top_n: int = 5):
        """Get similar users based on CF similarity"""
        if self.similarity_matrix is None:
            return []

        user_idx = self._get_user_index(user_id)
        if user_idx is None:
            return []

        similarities = self.similarity_matrix[user_idx]
        similar_indices = similarities.argsort()[::-1][1:top_n + 1]

        return self._get_user_ids_from_indices(similar_indices)

    def _get_user_index(self, user_id: int) -> int:
        """Get matrix index for user_id"""
        if self.user_item_matrix is None:
            return None
        try:
            return self.user_item_matrix.index.get_loc(user_id)
        except KeyError:
            return None

    def _get_user_ids_from_indices(self, indices: np.ndarray) -> list:
        """Convert matrix indices to user_ids"""
        if self.user_item_matrix is None:
            return []
        return [self.user_item_matrix.index[i] for i in indices if i < len(self.user_item_matrix.index)]

    @abstractmethod
    def recommend_cf(self, user_id: int, top_n: int = 10) -> list:
        """Get recommendations using collaborative filtering"""
        pass

    @abstractmethod
    def recommend_content_based(
        self,
        item_list: list,
        kategori: list,
        budget_min: float,
        budget_max: float,
        rating_min: float,
        top_n: int = 10
    ) -> pd.DataFrame:
        """Get recommendations using content-based filtering"""
        pass

    def recommend_hybrid(
        self,
        user_id: int,
        kategori: list,
        budget_min: float,
        budget_max: float,
        rating_min: float,
        top_n: int = 10
    ) -> pd.DataFrame:
        """Hybrid recommendation: CF + Content-based"""
        # Get CF recommendations
        cf_items = self.recommend_cf(user_id, top_n=top_n * 2)

        # Fallback if CF returns few items
        if len(cf_items) < 5:
            cf_items = self.df[self._name_column].tolist()

        # Apply content-based filtering
        result = self.recommend_content_based(
            cf_items,
            kategori,
            budget_min,
            budget_max,
            rating_min,
            top_n
        )

        return result
