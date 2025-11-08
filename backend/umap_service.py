"""
UMAP Projection Service
Handles dimensionality reduction from high-D embeddings to 3D coordinates
"""

import numpy as np
from umap import UMAP
from typing import Optional, Tuple
import pickle
from pathlib import Path


class UMAPService:
    def __init__(
        self,
        n_components: int = 3,
        n_neighbors: int = 15,
        min_dist: float = 0.1,
        metric: str = "cosine",
        random_state: int = 42
    ):
        """
        Initialize UMAP projection service
        
        Args:
            n_components: Dimensionality of output (3 for 3D visualization)
            n_neighbors: Size of local neighborhood (larger = more global structure)
            min_dist: Minimum distance between points (smaller = tighter clusters)
            metric: Distance metric to use
            random_state: Random seed for reproducibility
        """
        self.n_components = n_components
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.metric = metric
        self.random_state = random_state
        
        self.model = UMAP(
            n_components=n_components,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            metric=metric,
            random_state=random_state,
            verbose=True
        )
        
        self.is_fitted = False
        print(f"🗺️  UMAP initialized: {n_components}D, {n_neighbors} neighbors, {metric} metric")
    
    def fit_transform(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Fit UMAP on embeddings and transform to low-D coordinates
        
        Args:
            embeddings: High-dimensional embedding matrix (shape: [n_samples, n_features])
            
        Returns:
            Low-dimensional coordinates (shape: [n_samples, n_components])
        """
        print(f"🔄 Fitting UMAP on {embeddings.shape[0]} samples...")
        
        if embeddings.shape[0] < self.n_neighbors:
            print(f"⚠️  Warning: n_samples ({embeddings.shape[0]}) < n_neighbors ({self.n_neighbors})")
            print(f"   Adjusting n_neighbors to {embeddings.shape[0] - 1}")
            self.model.n_neighbors = embeddings.shape[0] - 1
        
        coords = self.model.fit_transform(embeddings)
        self.is_fitted = True
        
        print(f"✅ UMAP projection complete: {coords.shape}")
        return coords
    
    def transform(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Transform new embeddings using fitted UMAP model
        
        Args:
            embeddings: High-dimensional embedding matrix
            
        Returns:
            Low-dimensional coordinates
        """
        if not self.is_fitted:
            raise ValueError("UMAP model must be fitted before transform()")
        
        return self.model.transform(embeddings)
    
    def save(self, path: str):
        """Save fitted UMAP model to disk"""
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted UMAP model")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 UMAP model saved to {path}")
    
    def load(self, path: str):
        """Load fitted UMAP model from disk"""
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        self.is_fitted = True
        print(f"📂 UMAP model loaded from {path}")
    
    def get_bounds(self, coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get min/max bounds of coordinates for visualization
        
        Args:
            coords: Coordinate matrix
            
        Returns:
            (min_bounds, max_bounds) tuples
        """
        return coords.min(axis=0), coords.max(axis=0)
    
    def normalize_coords(self, coords: np.ndarray, scale: float = 10.0) -> np.ndarray:
        """
        Normalize coordinates to a specific range for better visualization
        
        Args:
            coords: Coordinate matrix
            scale: Scale factor (coords will be in range [-scale, +scale])
            
        Returns:
            Normalized coordinates
        """
        min_vals, max_vals = self.get_bounds(coords)
        
        # Center at origin
        centered = coords - (min_vals + max_vals) / 2
        
        # Scale to desired range
        max_range = (max_vals - min_vals).max()
        if max_range > 0:
            normalized = (centered / max_range) * 2 * scale
        else:
            normalized = centered
        
        return normalized


# Singleton instance
_umap_service = None


def get_umap_service(
    n_components: int = 3,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    metric: str = "cosine"
) -> UMAPService:
    """Get or create UMAP service singleton"""
    global _umap_service
    if _umap_service is None:
        _umap_service = UMAPService(n_components, n_neighbors, min_dist, metric)
    return _umap_service

