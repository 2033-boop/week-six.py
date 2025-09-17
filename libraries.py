import requests
import os
import hashlib
from urllib.parse import urlparse

def fetch_image(url, download_dir="Fetched_Images", known_hashes=None):
    """
    Fetch and save an image from the given URL.
    - Handles HTTP errors gracefully
    - Creates directory if it does not exist
    - Avoids duplicates using hash check
    """
    try:
        os.makedirs(download_dir, exist_ok=True)

        # Fetch image with timeout
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Check important headers
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return None

        # Extract filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        filepath = os.path.join(download_dir, filename)

        # Compute hash to avoid duplicates
        file_bytes = response.content
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        if known_hashes is not None and file_hash in known_hashes:
            print(f"✗ Duplicate skipped: {filename}")
            return None

        # Save image
        with open(filepath, "wb") as f:
            f.write(file_bytes)

        if known_hashes is not None:
            known_hashes.add(file_hash)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")
    return None


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get multiple URLs from user (comma separated)
    urls = input("Please enter one or more image URLs (comma separated): ").split(",")

    # Keep track of known file hashes to avoid duplicates
    known_hashes = set()

    for url in [u.strip() for u in urls if u.strip()]:
        fetch_image(url, known_hashes=known_hashes)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
