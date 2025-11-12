"""
X (Twitter) content downloader for extracting post content, images, and videos.
"""
import os
import re
import logging
import requests
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XDownloader:
    """
    Downloads and extracts content from X (Twitter) posts.
    Note: X has strict API access requirements. This implementation assumes
    users have API access or use third-party services.
    """

    VALID_DOMAINS = [
        'twitter.com',
        'www.twitter.com',
        'm.twitter.com',
        'x.com',
        'www.x.com',
        'm.x.com',
        'mobile.twitter.com'
    ]

    def __init__(self, output_dir: str = "uploads"):
        """
        Initialize the X downloader.

        Args:
            output_dir: Directory to save downloaded content
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    @staticmethod
    def is_x_url(url: str) -> bool:
        """
        Check if the URL is a valid X (Twitter) URL.

        Args:
            url: The URL to check

        Returns:
            True if it's an X URL, False otherwise
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Check if it's an X/Twitter domain
            is_valid_domain = any(domain.endswith(valid_domain) for valid_domain in XDownloader.VALID_DOMAINS)

            # Check if it's a status/tweet URL pattern
            is_tweet = '/status/' in parsed.path or '/statuses/' in parsed.path

            return is_valid_domain and is_tweet
        except Exception as e:
            logger.error(f"Error parsing X URL: {e}")
            return False

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate if the X URL is properly formatted.

        Args:
            url: The X URL to validate

        Returns:
            True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False

        url = url.strip()

        if not XDownloader.is_x_url(url):
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

    def extract_tweet_id(self, url: str) -> Optional[str]:
        """
        Extract the tweet ID from an X URL.

        Args:
            url: The X post URL

        Returns:
            The tweet ID if found, None otherwise
        """
        try:
            # Pattern for /status/tweetid or /statuses/tweetid
            status_match = re.search(r'/status(?:es)?/(\d+)', url)
            if status_match:
                return status_match.group(1)

            return None
        except Exception as e:
            logger.error(f"Error extracting tweet ID: {e}")
            return None

    def extract_username(self, url: str) -> Optional[str]:
        """
        Extract the username from an X URL.

        Args:
            url: The X post URL

        Returns:
            The username if found, None otherwise
        """
        try:
            # Pattern for /username/status/tweetid
            username_match = re.search(r'/([^/]+)/status', url)
            if username_match:
                username = username_match.group(1)
                # Filter out special paths
                if username not in ['i', 'home', 'explore', 'notifications', 'messages']:
                    return username

            return None
        except Exception as e:
            logger.error(f"Error extracting username: {e}")
            return None

    def download(self, url: str, bearer_token: Optional[str] = None) -> Dict:
        """
        Download content from an X (Twitter) post URL.

        Note: This is a placeholder implementation. In production, you would need:
        1. X API v2 access (requires developer account)
        2. Bearer token or OAuth authentication
        3. Proper API rate limiting
        4. Or use third-party services like nitter, or syndication API

        Args:
            url: The X post URL
            bearer_token: Optional bearer token for X API v2

        Returns:
            Dictionary containing tweet content and metadata

        Raises:
            ValueError: If the URL is invalid
            Exception: If download fails
        """
        if not self.validate_url(url):
            raise ValueError(f"Invalid X URL: {url}")

        tweet_id = self.extract_tweet_id(url)
        username = self.extract_username(url)

        logger.info(f"Downloading X post: {tweet_id} from @{username}")

        # PLACEHOLDER: In production, implement actual X API calls
        # For now, return a structure that matches what the system expects
        result = {
            'url': url,
            'tweet_id': tweet_id,
            'username': username,
            'text': '',  # Tweet text content
            'author': '',  # Author display name
            'images': [],  # List of image URLs
            'videos': [],  # List of video URLs
            'type': 'x_post',
            'is_thread': False,  # Whether this is part of a thread
            'thread_tweets': [],  # If thread, list of tweet IDs in order
            'error': 'X API integration required. Please implement X API authentication and calls.'
        }

        # Note for developers:
        # To implement this properly, you'll need to:
        # 1. Register for X API access (https://developer.twitter.com/)
        # 2. Get API keys and bearer token
        # 3. Use X API v2 endpoints:
        #    - GET /2/tweets/:id
        #    - Include expansions for media, author, referenced_tweets
        # 4. Or consider using alternatives:
        #    - nitter instances (privacy-friendly frontend)
        #    - Syndication API (public tweets)
        #    - Third-party services like RapidAPI

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

    def get_thread(self, tweet_id: str, bearer_token: str) -> List[Dict]:
        """
        Get all tweets in a thread starting from the given tweet.

        Args:
            tweet_id: The tweet ID to start from
            bearer_token: Bearer token for X API v2

        Returns:
            List of tweet data dictionaries in thread order

        Note: This requires X API v2 implementation
        """
        # PLACEHOLDER: Implement X API v2 thread retrieval
        logger.warning("Thread retrieval not yet implemented. Requires X API v2 access.")
        return []
