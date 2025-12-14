#!/usr/bin/env python3
"""Script to fetch book covers from bibliotece.pl"""

import urllib.request
import re
import time

# List of ISBN numbers from ksiazki.html
books = [
    {"isbn": "9788302203718", "name": "sieci-komputerowe-inf02-cz3"},
    {"isbn": "9788302188794", "name": "repetytorium-testy-inf02"},
    {"isbn": "9788302203787", "name": "zbior-zadan-inf02-cz2-systemy"},
    {"isbn": "9788302203770", "name": "zbior-zadan-inf02-cz1-urzadzenia"},
    {"isbn": "9788302203725", "name": "administrowanie-inf02-cz4"},
    {"isbn": "9788328359024", "name": "inf02-administracja-orczykowski"},
    {"isbn": "9788328358966", "name": "inf02-systemy-czerwonka"},
    {"isbn": "9788328359000", "name": "inf02-naprawa-czerwonka"},
    {"isbn": "9788328359017", "name": "inf02-sieci-orczykowski"},
    {"isbn": "9788302211485", "name": "zbior-zadan-sieci"},
    {"isbn": "9788302187544", "name": "administracja-inf02-cz2-pytel"},
    {"isbn": "9788302203695", "name": "urzadzenia-inf02-cz1"}
]

def fetch_cover_url(isbn):
    """Fetch cover image URL from bibliotece.pl"""
    # Format ISBN with hyphens
    formatted_isbn = f"{isbn[:3]}-{isbn[3:5]}-{isbn[5:7]}-{isbn[7:12]}-{isbn[12]}"
    search_url = f"https://w.bibliotece.pl/search/?q=isbn%3A+{formatted_isbn}"

    print(f"Searching for ISBN: {formatted_isbn}")
    print(f"URL: {search_url}")

    try:
        with urllib.request.urlopen(search_url, timeout=10) as response:
            html = response.read().decode('utf-8')

        # Find image URLs with regex
        pattern = r'src="(//dziupla\.sowa\.pl/[^"]+)"'
        matches = re.findall(pattern, html)

        if matches:
            img_url = matches[0]
            # Convert to absolute URL and increase size
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            # Replace size parameter for larger image
            img_url = re.sub(r'\?imwh=\d+x\d+', '?imwh=300x400', img_url)
            print(f"Found cover: {img_url}")
            return img_url
        else:
            print("No cover image found")
            return None

    except Exception as e:
        print(f"Error fetching {isbn}: {e}")
        return None

def download_image(url, filename):
    """Download image from URL"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()

        with open(filename, 'wb') as f:
            f.write(data)
        print(f"Saved: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    """Main function"""
    for book in books:
        isbn = book['isbn']
        name = book['name']

        print(f"\n{'='*60}")
        print(f"Processing: {name}")

        cover_url = fetch_cover_url(isbn)
        if cover_url:
            filename = f"images/covers/{name}.jpg"
            download_image(cover_url, filename)

        # Be polite, wait between requests
        time.sleep(2)

if __name__ == "__main__":
    main()
