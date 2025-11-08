"""
Claude Service via AWS Bedrock
Handles cluster naming, explanations, and natural language processing
"""

import json
import boto3
from typing import List, Dict, Optional
from botocore.exceptions import ClientError


class ClaudeService:
    def __init__(
        self,
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        region: str = "us-east-1"
    ):
        """
        Initialize Claude service via AWS Bedrock
        
        Args:
            model_id: Bedrock model ID for Claude
            region: AWS region
        """
        self.model_id = model_id
        self.region = region
        
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=region
            )
            print(f"🤖 Claude service initialized via AWS Bedrock ({model_id})")
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize Bedrock client: {e}")
            print("   Claude features will be unavailable")
            self.bedrock_runtime = None
    
    def _invoke_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1024,
        temperature: float = 1.0
    ) -> Optional[str]:
        """
        Invoke Claude via Bedrock
        
        Args:
            system_prompt: System instructions
            user_prompt: User query
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text or None if error
        """
        if self.bedrock_runtime is None:
            return None
        
        # Prepare request body for Claude 3
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_prompt}]
                }
            ]
        }
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            print(f"❌ Bedrock error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def name_cluster(
        self,
        top_objects: List[Dict[str, float]],
        color_profile: Optional[str] = None,
        sample_captions: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Generate a human-readable name and description for a cluster
        
        Args:
            top_objects: List of {name, confidence} dicts for top detected objects
            color_profile: Optional color description (e.g., "warm, low saturation")
            sample_captions: Optional example captions from cluster images
            
        Returns:
            {"title": str, "description": str}
        """
        system_prompt = "You are labeling visual clusters in an image embedding space. Be concise and descriptive."
        
        # Build user prompt
        user_prompt = "Top objects: "
        user_prompt += ", ".join([f"{obj['name']}({obj['confidence']:.2f})" for obj in top_objects])
        
        if color_profile:
            user_prompt += f"\nColor profile: {color_profile}"
        
        if sample_captions:
            user_prompt += f"\nSample captions: {json.dumps(sample_captions[:3])}"
        
        user_prompt += "\n\nReturn JSON with: {\"title\": \"<max 6 words>\", \"description\": \"<one sentence>\"}"
        
        response = self._invoke_claude(system_prompt, user_prompt, max_tokens=200, temperature=0.7)
        
        if response:
            try:
                # Try to extract JSON from response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    result = json.loads(response[start:end])
                    return result
            except json.JSONDecodeError:
                pass
        
        # Fallback
        top_obj_names = ", ".join([obj['name'] for obj in top_objects[:3]])
        return {
            "title": f"Cluster: {top_obj_names}",
            "description": f"Images featuring {top_obj_names}."
        }
    
    def explain_cluster(
        self,
        top_objects: List[Dict[str, float]],
        color_profile: Optional[str] = None,
        num_images: int = 0
    ) -> str:
        """
        Explain why images are grouped together in a cluster
        
        Args:
            top_objects: List of {name, confidence} dicts
            color_profile: Optional color description
            num_images: Number of images in cluster
            
        Returns:
            One-sentence explanation
        """
        system_prompt = "You explain why selected images are visually similar. Be concise and insightful."
        
        user_prompt = f"This cluster contains {num_images} images.\n"
        user_prompt += "Common objects: " + ", ".join([f"{obj['name']}({obj['confidence']:.2f})" for obj in top_objects])
        
        if color_profile:
            user_prompt += f"\nColor profile: {color_profile}"
        
        user_prompt += "\n\nExplain in one clear sentence why these images are grouped together."
        
        response = self._invoke_claude(system_prompt, user_prompt, max_tokens=150, temperature=0.8)
        
        if response:
            return response.strip()
        
        # Fallback
        top_obj_names = " and ".join([obj['name'] for obj in top_objects[:2]])
        return f"These images share common visual elements like {top_obj_names}."
    
    def process_nl_query(self, query: str) -> Dict[str, any]:
        """
        Process natural language search query to extract visual cues
        
        Args:
            query: Natural language search string (e.g., "cozy desk with coffee")
            
        Returns:
            {"objects": [str], "colors": [str], "context": str}
        """
        system_prompt = "You extract visual search cues from natural language queries."
        
        user_prompt = f"Query: \"{query}\"\n\n"
        user_prompt += "Extract: {\"objects\": [list of objects], \"colors\": [list of colors/lighting], \"context\": \"brief scene description\"}"
        
        response = self._invoke_claude(system_prompt, user_prompt, max_tokens=200, temperature=0.5)
        
        if response:
            try:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    result = json.loads(response[start:end])
                    return result
            except json.JSONDecodeError:
                pass
        
        # Fallback: return query as context
        return {
            "objects": [],
            "colors": [],
            "context": query
        }
    
    def generate_guided_tour(self, clusters: List[Dict]) -> str:
        """
        Generate a guided tour narrative through clusters
        
        Args:
            clusters: List of cluster dicts with title and description
            
        Returns:
            Tour narrative
        """
        if not clusters:
            return "No clusters to tour."
        
        system_prompt = "You create engaging guided tours through visual collections."
        
        user_prompt = "Create a short guided tour (2-3 sentences) through these visual clusters:\n\n"
        for i, cluster in enumerate(clusters[:3], 1):
            user_prompt += f"{i}. {cluster['title']}: {cluster['description']}\n"
        
        user_prompt += "\nWrite an engaging tour narrative that connects these visual themes."
        
        response = self._invoke_claude(system_prompt, user_prompt, max_tokens=300, temperature=0.9)
        
        if response:
            return response.strip()
        
        # Fallback
        titles = ", then ".join([c['title'] for c in clusters[:3]])
        return f"Explore this visual journey: {titles}."


# Singleton instance
_claude_service = None


def get_claude_service(
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    region: str = "us-east-1"
) -> ClaudeService:
    """Get or create Claude service singleton"""
    global _claude_service
    if _claude_service is None:
        _claude_service = ClaudeService(model_id, region)
    return _claude_service

