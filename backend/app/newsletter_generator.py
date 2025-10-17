import shutil
from pathlib import Path
from typing import List, Dict
from app.ai_service import AIService


class NewsletterGenerator:
    """Generates newsletter markdown with embedded images"""
    
    async def generate(
        self,
        transcript: str,
        key_frames: List[Dict],
        output_dir: Path,
        ai_service: AIService
    ) -> Path:
        """Generate newsletter markdown file with images"""
        
        # Create images directory
        images_dir = output_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Copy images to output directory
        frame_references = []
        for i, frame in enumerate(key_frames):
            # Copy image
            image_name = f"frame_{i+1}.jpg"
            image_dest = images_dir / image_name
            shutil.copy(frame["path"], image_dest)
            
            frame_references.append({
                "path": f"images/{image_name}",
                "caption": frame["caption"],
                "timestamp": frame["timestamp"]
            })
        
        # Generate article content using AI
        article_content = await ai_service.generate_newsletter_content(
            transcript, key_frames
        )
        
        # Build markdown
        markdown_parts = []
        
        # Split article into sections and insert images
        # Simple approach: split by paragraphs and insert images evenly
        paragraphs = [p.strip() for p in article_content.split("\n\n") if p.strip()]
        
        # Calculate positions to insert images
        images_to_insert = len(frame_references)
        if len(paragraphs) > images_to_insert:
            insert_interval = len(paragraphs) // (images_to_insert + 1)
        else:
            insert_interval = 1
        
        image_idx = 0
        for para_idx, paragraph in enumerate(paragraphs):
            markdown_parts.append(paragraph)
            markdown_parts.append("")  # Empty line
            
            # Insert image after certain intervals
            if (para_idx + 1) % insert_interval == 0 and image_idx < len(frame_references):
                frame_ref = frame_references[image_idx]
                markdown_parts.append(f"![{frame_ref['caption']}]({frame_ref['path']})")
                markdown_parts.append(f"*{frame_ref['caption']}*")
                markdown_parts.append("")
                image_idx += 1
        
        # Add any remaining images at the end
        while image_idx < len(frame_references):
            frame_ref = frame_references[image_idx]
            markdown_parts.append(f"![{frame_ref['caption']}]({frame_ref['path']})")
            markdown_parts.append(f"*{frame_ref['caption']}*")
            markdown_parts.append("")
            image_idx += 1
        
        # Write markdown file
        markdown_content = "\n".join(markdown_parts)
        newsletter_path = output_dir / "newsletter.md"
        newsletter_path.write_text(markdown_content, encoding="utf-8")
        
        # Clean up temporary frames
        for frame in key_frames:
            frame_path = Path(frame["path"])
            if frame_path.exists() and frame_path.parent.name.endswith("_frames"):
                # Clean up the entire frames directory
                shutil.rmtree(frame_path.parent, ignore_errors=True)
                break
        
        return newsletter_path

