"""
k-Nearest Neighbors Service
Handles fast similarity search and graph construction using FAISS
"""

import numpy as np
import faiss
from typing import List, Tuple, Dict, Optional
import json
from pathlib import Path


class KNNService:
    def __init__(self, embedding_dim: int, metric: str = "cosine"):
        """
        Initialize kNN service with FAISS
        
        Args:
            embedding_dim: Dimensionality of embeddings
            metric: Distance metric ("cosine" or "euclidean")
        """
        self.embedding_dim = embedding_dim
        self.metric = metric
        
        # Create FAISS index
        if metric == "cosine":
            # For cosine similarity, use inner product with normalized vectors
            self.index = faiss.IndexFlatIP(embedding_dim)
        else:
            # L2 (Euclidean) distance
            self.index = faiss.IndexFlatL2(embedding_dim)
        
        self.embeddings = None
        self.ids = []
        
        print(f"🔍 FAISS index initialized: {embedding_dim}D, {metric} metric")
    
    def add_embeddings(self, embeddings: np.ndarray, ids: List[str]):
        """
        Add embeddings to the index
        
        Args:
            embeddings: Embedding matrix (shape: [n, embedding_dim])
            ids: List of unique IDs for each embedding
        """
        if embeddings.shape[1] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {embeddings.shape[1]}")
        
        # Ensure float32 for FAISS
        embeddings = embeddings.astype(np.float32)
        
        # For cosine similarity, normalize vectors
        if self.metric == "cosine":
            faiss.normalize_L2(embeddings)
        
        self.index.add(embeddings)
        self.ids.extend(ids)
        
        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        
        print(f"➕ Added {len(ids)} embeddings to index (total: {self.index.ntotal})")
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> Tuple[List[str], List[float]]:
        """
        Find k nearest neighbors for a query embedding
        
        Args:
            query_embedding: Query vector (shape: [embedding_dim])
            k: Number of neighbors to return
            
        Returns:
            (neighbor_ids, distances) tuple
        """
        if self.index.ntotal == 0:
            return [], []
        
        # Ensure correct shape and type
        query = query_embedding.astype(np.float32).reshape(1, -1)
        
        # Normalize for cosine similarity
        if self.metric == "cosine":
            faiss.normalize_L2(query)
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query, k)
        
        # Convert to lists
        neighbor_ids = [self.ids[idx] for idx in indices[0]]
        neighbor_distances = distances[0].tolist()
        
        return neighbor_ids, neighbor_distances
    
    def search_batch(self, query_embeddings: np.ndarray, k: int = 10) -> Tuple[List[List[str]], List[List[float]]]:
        """
        Find k nearest neighbors for multiple query embeddings
        
        Args:
            query_embeddings: Query matrix (shape: [n_queries, embedding_dim])
            k: Number of neighbors to return per query
            
        Returns:
            (neighbor_ids_list, distances_list) tuple
        """
        if self.index.ntotal == 0:
            return [[] for _ in range(len(query_embeddings))], [[] for _ in range(len(query_embeddings))]
        
        # Ensure correct type
        queries = query_embeddings.astype(np.float32)
        
        # Normalize for cosine similarity
        if self.metric == "cosine":
            faiss.normalize_L2(queries)
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(queries, k)
        
        # Convert to lists
        neighbor_ids_list = [[self.ids[idx] for idx in row] for row in indices]
        distances_list = [row.tolist() for row in distances]
        
        return neighbor_ids_list, distances_list
    
    def build_knn_graph(self, k: int = 8) -> Dict[str, List[Dict[str, any]]]:
        """
        Build k-NN graph for all points in the index
        
        Args:
            k: Number of neighbors per node
            
        Returns:
            Graph dictionary: {node_id: [{"target": target_id, "weight": similarity}, ...]}
        """
        if self.embeddings is None or len(self.ids) == 0:
            return {}
        
        print(f"🕸️  Building k-NN graph with k={k}...")
        
        # Find k+1 neighbors (includes self)
        neighbor_ids_list, distances_list = self.search_batch(self.embeddings, k=k+1)
        
        # Build graph (exclude self from neighbors)
        graph = {}
        for i, node_id in enumerate(self.ids):
            neighbors = []
            for j, (neighbor_id, distance) in enumerate(zip(neighbor_ids_list[i], distances_list[i])):
                if neighbor_id != node_id:  # Skip self
                    # Convert distance to similarity (for cosine, distance is already similarity)
                    if self.metric == "cosine":
                        weight = float(distance)  # Already in [0, 1]
                    else:
                        # For euclidean, convert to similarity
                        weight = 1.0 / (1.0 + float(distance))
                    
                    neighbors.append({
                        "target": neighbor_id,
                        "weight": weight
                    })
            
            graph[node_id] = neighbors[:k]  # Ensure exactly k neighbors
        
        print(f"✅ Graph built: {len(graph)} nodes, avg {k} edges per node")
        return graph
    
    def save_graph(self, graph: Dict, path: str):
        """Save k-NN graph to JSON file"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to edge list format for easier frontend consumption
        edges = []
        for source, neighbors in graph.items():
            for neighbor in neighbors:
                edges.append({
                    "source": source,
                    "target": neighbor["target"],
                    "weight": neighbor["weight"]
                })
        
        output = {
            "k": len(graph[next(iter(graph))]) if graph else 0,
            "num_nodes": len(graph),
            "num_edges": len(edges),
            "edges": edges
        }
        
        with open(path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"💾 Graph saved to {path}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the index"""
        return {
            "total_embeddings": self.index.ntotal,
            "embedding_dim": self.embedding_dim,
            "metric": self.metric,
            "num_ids": len(self.ids)
        }


# Singleton instance
_knn_service = None


def get_knn_service(embedding_dim: int, metric: str = "cosine") -> KNNService:
    """Get or create kNN service singleton"""
    global _knn_service
    if _knn_service is None:
        _knn_service = KNNService(embedding_dim, metric)
    return _knn_service

