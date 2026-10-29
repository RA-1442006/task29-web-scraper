"""
Web Scraper for books.toscrape.com
Task 29 - Python Internship

Note on robots.txt:
Checked https://books.toscrape.com/robots.txt (returns 404).
This sandbox site is built specifically for web scraping practice,
and no endpoints are disallowed. We still use a 1-second delay between
page requests to be polite and avoid unnecessary load on the server.
"""

import csv
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Base URL for catalogue pages
BASE_URL = "https://books.toscrape.com/catalogue/"

# Map rating class names to readable values
RATING_MAP = {
    "One": "1 star",
    "Two": "2 stars",
    "Three": "3 stars",
    "Four": "4 stars",
    "Five": "5 stars"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_page(url):
    """Fetch HTML content of a single page."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = "utf-8"
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url} - Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error requesting {url}: {e}")
        return None


def parse_books(html, current_url):
    """Extract book details from page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    # Each book is contained in an <article class="product_pod">
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        # Title is in the title attribute of the <a> tag inside <h3>
        title_tag = article.find("h3").find("a")
        title = title_tag.get("title", title_tag.text.strip())

        # Price text
        price_tag = article.find("p", class_="price_color")
        price = price_tag.text.strip() if price_tag else "N/A"

        # Star rating from CSS class (e.g., ['star-rating', 'Three'])
        rating_tag = article.find("p", class_="star-rating")
        rating = "Not rated"
        if rating_tag:
            rating_classes = rating_tag.get("class", [])
            for cls in rating_classes:
                if cls in RATING_MAP:
                    rating = RATING_MAP[cls]
                    break

        # Availability status (e.g. In stock)
        avail_tag = article.find("p", class_="instock availability")
        availability = avail_tag.text.strip() if avail_tag else "Unknown"

        # Full product link
        link_rel = title_tag.get("href", "")
        product_link = urljoin(current_url, link_rel)

        books.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability,
            "Product Link": product_link
        })

    return books


def save_to_csv(books, filename="books_output.csv"):
    """Save the list of book dictionaries to a CSV file."""
    if not books:
        print("No books found to save.")
        return

    fieldnames = ["Title", "Price", "Rating", "Availability", "Product Link"]

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)

    print(f"Saved {len(books)} books to {filename}")


def main():
    all_books = []
    total_pages = 5  # Scrape first 5 pages

    print(f"Starting scraper for first {total_pages} pages...")

    for page_num in range(1, total_pages + 1):
        page_url = f"{BASE_URL}page-{page_num}.html"
        print(f"Fetching page {page_num}: {page_url}")

        html = get_page(page_url)
        if not html:
            print(f"Skipping page {page_num} due to fetch error.")
            continue

        page_books = parse_books(html, page_url)
        all_books.extend(page_books)
        print(f"Extracted {len(page_books)} books from page {page_num}.")

        # Be polite to the server
        time.sleep(1)

    print(f"\nScraping complete. Total books extracted: {len(all_books)}")
    save_to_csv(all_books, "books_output.csv")


if __name__ == "__main__":
    main()
