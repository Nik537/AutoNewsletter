"""
LinkedIn content downloader for extracting post content, images, and videos.
"""
import os
import re
import logging
import requests
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInDownloader:
    """
    Downloads and extracts content from LinkedIn posts.
    Note: LinkedIn has strict scraping policies. This implementation assumes
    users provide their own authentication or use public posts.
    """

    VALID_DOMAINS = [
        'linkedin.com',
        'www.linkedin.com',
        'm.linkedin.com'
    ]

    def __init__(self, output_dir: str = "uploads"):
        """
        Initialize the LinkedIn downloader.

        Args:
            output_dir: Directory to save downloaded content
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    @staticmethod
    def is_linkedin_url(url: str) -> bool:
        """
        Check if the URL is a valid LinkedIn URL.

        Args:
            url: The URL to check

        Returns:
            True if it's a LinkedIn URL, False otherwise
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Check if it's a LinkedIn domain
            is_valid_domain = any(domain.endswith(valid_domain) for valid_domain in LinkedInDownloader.VALID_DOMAINS)

            # Check if it's a post URL pattern
            is_post = '/posts/' in parsed.path or '/feed/update/' in parsed.path or '/pulse/' in parsed.path

            return is_valid_domain and is_post
        except Exception as e:
            logger.error(f"Error parsing LinkedIn URL: {e}")
            return False

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate if the LinkedIn URL is properly formatted.

        Args:
            url: The LinkedIn URL to validate

        Returns:
            True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False

        url = url.strip()

        if not LinkedInDownloader.is_linkedin_url(url):
            return False

        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return url_pattern.match(url) is not None

    def extract_post_id(self, url: str) -> Optional[str]:
        """
        Extract the post ID from a LinkedIn URL.

        Args:
            url: The LinkedIn post URL

        Returns:
            The post ID if found, None otherwise
        """
        try:
            # Pattern for /posts/username_postid format
            posts_match = re.search(r'/posts/[^/]+_(\d+)', url)
            if posts_match:
                return posts_match.group(1)

            # Pattern for /feed/update/urn:li:activity:postid format
            activity_match = re.search(r'urn:li:activity:(\d+)', url)
            if activity_match:
                return activity_match.group(1)

            # Pattern for /pulse/articleid format
            pulse_match = re.search(r'/pulse/([^/]+)/?', url)
            if pulse_match:
                return pulse_match.group(1)

            return None
        except Exception as e:
            logger.error(f"Error extracting post ID: {e}")
            return None

    def download(self, url: str, auth_token: Optional[str] = None) -> Dict:
        """
        Download content from a LinkedIn post URL.

        Note: This is a placeholder implementation. In production, you would need:
        1. LinkedIn API access (requires LinkedIn Developer account)
        2. OAuth authentication
        3. Proper API rate limiting
        4. Or use a third-party service like PhantomBuster or Apify

        Args:
            url: The LinkedIn post URL
            auth_token: Optional authentication token for LinkedIn API

        Returns:
            Dictionary containing post content and metadata

        Raises:
            ValueError: If the URL is invalid
            Exception: If download fails
        """
        if not self.validate_url(url):
            raise ValueError(f"Invalid LinkedIn URL: {url}")

        post_id = self.extract_post_id(url)
        logger.info(f"Downloading LinkedIn post: {post_id}")

        # PLACEHOLDER: In production, implement actual LinkedIn API calls
        # For now, return a structure that matches what the system expects
        result = {
            'url': url,
            'post_id': post_id,
            'text': '',  # Post text content
            'author': '',  # Post author name
            'images': [],  # List of image URLs
            'videos': [],  # List of video URLs
            'type': 'linkedin_post',
            'error': 'LinkedIn API integration required. Please implement LinkedIn authentication and API calls.'
        }

        # Note for developers:
        # To implement this properly, you'll need to:
        # 1. Register a LinkedIn Developer application
        # 2. Implement OAuth 2.0 flow
        # 3. Use the LinkedIn Marketing Developer Platform API
        # 4. Or consider using services like:
        #    - PhantomBuster (https://phantombuster.com/)
        #    - Apify (https://apify.com/)
        #    - RapidAPI LinkedIn scraper

        return result

    def download_media(self, media_url: str, output_filename: str) -> Optional[Path]:
        """
        Download a media file (image or video) from URL.

        Args:
            media_url: URL of the media to download
            output_filename: Name for the output file

        Returns:
            Path to the downloaded file, or None if failed
        """
        try:
            response = requests.get(media_url, stream=True, timeout=30)
            response.raise_for_status()

            output_path = self.output_dir / output_filename

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Downloaded media to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to download media from {media_url}: {e}")
            return None
