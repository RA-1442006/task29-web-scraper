# Web Scraper for Book Data (Task 29)

A simple Python web scraper built as part of Task 29 of my Python internship. The script extracts book details from [books.toscrape.com](https://books.toscrape.com), iterates through the first 5 catalog pages, and exports the collected data into a structured CSV file.

---

## Objective

The goal of this project is to practice web scraping on a publicly permitted practice website, extract structured information from raw HTML, handle pagination, and store the cleaned results into a CSV file for analysis.

---

## Tools Used

- **Python 3**: Core language used for writing the script.
- **Requests**: Sends HTTP GET requests to fetch web pages.
- **BeautifulSoup4 (bs4)**: Parses HTML documents and searches DOM elements using tag names and CSS classes.
- **csv (Standard Library)**: Writes scraped records into a standard comma-separated values file.
- **time (Standard Library)**: Adds delays between page requests to avoid overwhelming the server.

---

## Project Structure

```text
web-scraper-csv-task29/
├── scraper.py          # Main scraping script
├── books_output.csv    # Scraped dataset (100 books from pages 1-5)
├── requirements.txt    # Project dependencies
├── .gitignore          # Git ignore file for Python
└── README.md           # Project documentation and interview Q&A
```

---

## How to Install and Run

1. **Clone or navigate to the project directory:**
   ```bash
   cd web-scraper-csv-task29
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper:**
   ```bash
   python scraper.py
   ```

5. **Check the output:**
   After the script finishes, `books_output.csv` will be generated with 100 rows of extracted book data.

---

## Extracted Fields

For every book, the script extracts five data points:

1. **Title**: Full book title extracted from the `title` attribute of the `<a>` tag inside the `<h3>` header.
2. **Price**: Book price in British Pounds (e.g. `£51.77`), retrieved from `<p class="price_color">`.
3. **Rating**: Star rating mapped from CSS classes (`One`, `Two`, `Three`, `Four`, `Five`) to clean text (e.g., `3 stars`).
4. **Availability**: Stock status (e.g., `In stock`), found in `<p class="instock availability">`.
5. **Product Link**: Absolute URL to the individual book details page, resolved using `urllib.parse.urljoin`.

---

## Ethical Scraping Notes

- **Permitted Target**: The target site `https://books.toscrape.com` is an open sandbox explicitly hosted for learning and practicing web scraping.
- **robots.txt Check**: A check was made against `https://books.toscrape.com/robots.txt` (which returns a 404 response, indicating no crawling restrictions).
- **Polite Crawling Rate**: The script includes a 1-second pause (`time.sleep(1)`) between consecutive requests to avoid flooding the server with traffic.
- **Descriptive Headers**: A standard `User-Agent` header is provided with requests to identify the client transparently.

---

## Sample CSV Output

Here is a snippet from `books_output.csv`:

| Title | Price | Rating | Availability | Product Link |
|---|---|---|---|---|
| A Light in the Attic | £51.77 | 3 stars | In stock | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |
| Tipping the Velvet | £53.74 | 1 star | In stock | https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html |
| Soumission | £50.10 | 1 star | In stock | https://books.toscrape.com/catalogue/soumission_998/index.html |
| Sharp Objects | £47.82 | 4 stars | In stock | https://books.toscrape.com/catalogue/sharp-objects_997/index.html |
| Sapiens: A Brief History of Humankind | £54.23 | 5 stars | In stock | https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html |

---

## What I Learned

- **HTTP Requests**: How to use `requests.get()` with custom headers, verify status codes, and handle response character encodings properly (UTF-8).
- **HTML Parsing**: How BeautifulSoup traverses the DOM tree, searches with `find()` and `find_all()`, and pulls data from both tag contents and element attributes.
- **Data Extraction & Cleaning**: Converting relative URLs into absolute links using `urljoin`, parsing CSS class names for ratings, and writing clean dictionaries to CSV using `csv.DictWriter`.

---

## Interview Questions & Answers

### 1. What is web scraping?
Web scraping is the automated process of fetching web pages over HTTP and extracting target data from their HTML structure. It allows developers to collect publicly available information from sites that do not provide an official API.

### 2. What is BeautifulSoup?
BeautifulSoup is a popular Python library used to parse HTML and XML documents. It builds a parse tree from page source code, making it easy to navigate, search, and extract elements using tag names, attributes, and CSS selectors.

### 3. What is the difference between HTML parsing and API consumption?
HTML parsing involves downloading unstructured markup designed for human display and extracting text using tag patterns, which can break when the site layout changes. API consumption retrieves structured data (typically JSON or XML) directly from defined backend endpoints, making it more reliable, efficient, and intentional.

### 4. Why should scraping respect website policies?
Scraping should respect website policies (such as `robots.txt` and Terms of Service) to prevent server overload, avoid legal and copyright violations, and maintain ethical boundaries. Uncontrolled or aggressive scraping can cause service disruptions or lead to IP bans.
