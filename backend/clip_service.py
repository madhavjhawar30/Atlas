"""
CLIP Embedding Service
Handles image and text embedding generation using OpenAI's CLIP model
"""

import torch
import open_clip
from PIL import Image
import numpy as np
from typing import List, Union
import io
from pathlib import Path


class CLIPService:
    def __init__(self, model_name: str = "ViT-B-32", pretrained: str = "openai"):
        """
        Initialize CLIP model
        
        Args:
            model_name: CLIP model architecture (e.g., "ViT-B-32", "ViT-L-14")
            pretrained: Pretrained weights to use (e.g., "openai", "laion2b_s34b_b79k")
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Loading CLIP model '{model_name}' on {self.device}...")
        
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name, 
            pretrained=pretrained
        )
        self.model = self.model.to(self.device).eval()
        self.tokenizer = open_clip.get_tokenizer(model_name)
        
        # Get embedding dimension
        with torch.no_grad():
            dummy_img = torch.zeros(1, 3, 224, 224).to(self.device)
            dummy_features = self.model.encode_image(dummy_img)
            self.embedding_dim = dummy_features.shape[1]
        
        print(f"✅ CLIP loaded. Embedding dimension: {self.embedding_dim}")
    
    def embed_image(self, image: Union[Image.Image, bytes, str, np.ndarray]) -> np.ndarray:
        """
        Generate CLIP embedding for a single image
        
        Args:
            image: PIL Image, bytes, file path, or numpy array
            
        Returns:
            Normalized embedding vector (shape: [embedding_dim])
        """
        # Convert to PIL Image if needed
        if isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))
        elif isinstance(image, str):
            image = Image.open(image)
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Ensure RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Preprocess and embed
        img_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            image_features = self.model.encode_image(img_tensor)
            # L2 normalize
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.squeeze(0).cpu().numpy()
    
    def embed_images_batch(self, images: List[Union[Image.Image, bytes, str]]) -> np.ndarray:
        """
        Generate CLIP embeddings for a batch of images
        
        Args:
            images: List of PIL Images, bytes, or file paths
            
        Returns:
            Normalized embedding matrix (shape: [n_images, embedding_dim])
        """
        # Convert all to PIL Images
        pil_images = []
        for img in images:
            if isinstance(img, bytes):
                pil_images.append(Image.open(io.BytesIO(img)))
            elif isinstance(img, str):
                pil_images.append(Image.open(img))
            elif isinstance(img, np.ndarray):
                pil_images.append(Image.fromarray(img))
            else:
                pil_images.append(img)
        
        # Ensure RGB and preprocess
        pil_images = [img.convert("RGB") if img.mode != "RGB" else img for img in pil_images]
        img_tensors = torch.stack([self.preprocess(img) for img in pil_images]).to(self.device)
        
        with torch.no_grad():
            image_features = self.model.encode_image(img_tensors)
            # L2 normalize
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy()
    
    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate CLIP embedding for text query
        
        Args:
            text: Single text string or list of text strings
            
        Returns:
            Normalized embedding vector(s)
        """
        if isinstance(text, str):
            text = [text]
        
        text_tokens = self.tokenizer(text).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            # L2 normalize
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        result = text_features.cpu().numpy()
        return result[0] if len(text) == 1 else result
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        return float(np.dot(embedding1, embedding2))
    
    def compute_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Compute pairwise cosine similarity matrix
        
        Args:
            embeddings: Matrix of embeddings (shape: [n, embedding_dim])
            
        Returns:
            Similarity matrix (shape: [n, n])
        """
        # Embeddings are already normalized, so dot product = cosine similarity
        return embeddings @ embeddings.T


# Singleton instance
_clip_service = None


def get_clip_service(model_name: str = "ViT-B-32", pretrained: str = "openai") -> CLIPService:
    """Get or create CLIP service singleton"""
    global _clip_service
    if _clip_service is None:
        _clip_service = CLIPService(model_name, pretrained)
    return _clip_service

