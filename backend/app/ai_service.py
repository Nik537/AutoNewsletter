import os
import base64
from typing import List, Tuple, Dict
from pathlib import Path
import anthropic
from anthropic import Anthropic


class AIService:
    """Handles AI operations using Claude API"""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-haiku-4-5-20251001"
    
    def _encode_image(self, image_path: Path) -> str:
        """Encode image to base64, resizing if necessary"""
        from PIL import Image
        import io
        
        # Open and resize image if needed
        with Image.open(image_path) as img:
            # Get current dimensions
            width, height = img.size
            max_dimension = 1900  # Keep under 2000 pixel limit
            
            # Resize if any dimension exceeds limit
            if width > max_dimension or height > max_dimension:
                # Calculate new dimensions maintaining aspect ratio
                if width > height:
                    new_width = max_dimension
                    new_height = int(height * (max_dimension / width))
                else:
                    new_height = max_dimension
                    new_width = int(width * (max_dimension / height))
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary (remove alpha channel)
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img
            
            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            
            return base64.standard_b64encode(buffer.read()).decode("utf-8")
    
    async def select_key_frames(
        self, 
        frames: List[Tuple[float, Path]], 
        transcript: str
    ) -> List[Dict]:
        """Analyze frames and select key moments using Claude Vision"""
        
        # Limit to analyzing every Nth frame to avoid too many API calls
        # Analyze max 20 frames
        step = max(1, len(frames) // 20)
        frames_to_analyze = frames[::step]
        
        # Prepare frames for analysis
        frame_contents = []
        for timestamp, frame_path in frames_to_analyze:
            image_data = self._encode_image(frame_path)
            frame_contents.append({
                "timestamp": timestamp,
                "path": frame_path,
                "image_data": image_data
            })
        
        # Build message with all frames
        message_content = [
            {
                "type": "text",
                "text": f"""You are analyzing frames from a video to select the most important moments for a newsletter article.

Video Transcript:
{transcript[:2000]}...

I'm providing you with {len(frame_contents)} frames extracted from the video. Please analyze these frames and identify the 5-8 most visually interesting and relevant frames that would work well as screenshots in a newsletter article.

For each selected frame, provide:
1. The frame number (0-{len(frame_contents)-1})
2. A brief description of what makes it important
3. A caption in English

Respond in JSON format:
{{
  "selected_frames": [
    {{
      "frame_index": 0,
      "reason": "Shows the main topic introduction",
      "caption": "Introduction to the topic"
    }}
  ]
}}"""
            }
        ]
        
        # Add all frame images
        for i, frame in enumerate(frame_contents):
            message_content.append({
                "type": "text",
                "text": f"\n--- Frame {i} (at {frame['timestamp']}s) ---"
            })
            message_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": frame["image_data"]
                }
            })
        
        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": message_content}]
        )
        
        # Parse response
        import json
        response_text = response.content[0].text
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            
            # Map selected frames back to original frame data
            selected_frames = []
            for selection in result["selected_frames"]:
                frame_idx = selection["frame_index"]
                if 0 <= frame_idx < len(frame_contents):
                    frame_data = frame_contents[frame_idx]
                    selected_frames.append({
                        "timestamp": frame_data["timestamp"],
                        "path": frame_data["path"],
                        "caption": selection["caption"],
                        "reason": selection["reason"]
                    })
            
            return selected_frames
            
        except (json.JSONDecodeError, KeyError) as e:
            # Fallback: select frames evenly distributed
            print(f"Failed to parse AI response: {e}")
            num_frames = min(6, len(frame_contents))
            step = len(frame_contents) // num_frames
            return [
                {
                    "timestamp": frame_contents[i * step]["timestamp"],
                    "path": frame_contents[i * step]["path"],
                    "caption": f"Frame at {frame_contents[i * step]['timestamp']}s",
                    "reason": "Auto-selected"
                }
                for i in range(num_frames)
            ]
    
    async def generate_newsletter_content(
        self, 
        transcript: str, 
        key_frames: List[Dict]
    ) -> str:
        """Generate newsletter article in Slovenian based on transcript and key frames"""
        
        # Prepare frame descriptions
        frame_descriptions = "\n".join([
            f"- Frame at {f['timestamp']}s: {f['caption']} ({f['reason']})"
            for f in key_frames
        ])
        
        prompt = f"""You are a professional newsletter writer. Create a comprehensive newsletter article in Slovenian language based on the following English video content.

Video Transcript (English):
{transcript}

Key Visual Moments:
{frame_descriptions}

Instructions:
1. Write the article entirely in Slovenian language
2. The article should be well-structured with a title, introduction, main content sections, and conclusion
3. The article should be approximately 800-1200 words
4. Create natural transitions between sections
5. The tone should be informative and engaging
6. Include relevant context and explanations
7. Make it suitable for a newsletter format

Important: Write ONLY the article content in Slovenian. Do not include any English text, explanations, or meta-commentary."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

