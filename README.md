<div align="center">

# 📚 Books to Scrape Web Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Requests](https://img.shields.io/badge/requests-2.31.0%2B-green)](https://pypi.org/project/requests/)
[![BeautifulSoup](https://img.shields.io/badge/beautifulsoup4-4.12.0%2B-green)](https://pypi.org/project/beautifulsoup4/)

*A robust, Python web scraper for extracting book data from [Books to Scrape](https://books.toscrape.com/).*

</div>

---

## 🚀 Features

Built this project demonstrates clean and maintainable Python code:

- **🏗️ Object-Oriented Architecture (OOP):** Modular design using a dedicated `BookScraper` class for better state management and reusability.
- **✨ Type Hinting:** Fully type-hinted methods ensuring better IDE integration, static analysis, and code readability.
- **⚡ Performance Optimized:** Utilizes `requests.Session()` for connection pooling, significantly reducing overhead and speeding up HTTP requests.
- **🛡️ Robust Error Handling:** Comprehensive `try...except` blocks to gracefully handle network timeouts, HTTP errors, and unexpected DOM parsing exceptions.
- **📝 Standardized Logging:** Replaces standard `print()` statements with Python's built-in `logging` module for production-ready execution monitoring.
- **💻 Command-Line Interface (CLI):** Interactive terminal execution using `argparse` for dynamic argument parsing.

## 🛠️ Prerequisites

Ensure you have Python 3.8 or higher installed on your system. It is highly recommended to use a virtual environment.

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install required dependencies
pip install requests beautifulsoup4
```

## 💻 Usage

The scraper can be executed directly from the terminal. It accepts arguments to control the scraping process.

```bash
# Basic usage (scrapes the first 5 pages and saves to hasil_buku.csv)
python scraper.py

# Specify the number of pages and custom output filename
python scraper.py --pages 3 --output my_books_data.csv

# View help and available commands
python scraper.py --help
```

### ⚙️ Command-Line Arguments

| Argument | Short Flag | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `--pages` | `-p` | `5` | Maximum number of pages to scrape from the catalogue. |
| `--output` | `-o` | `hasil_buku.csv` | Output filename for the exported CSV data. |

## 📊 Output Data Format

The scraped data is automatically exported to a UTF-8 encoded CSV file containing the following fields:

- `judul`: The title of the book.
- `harga`: The price of the book (including currency symbol).
- `rating`: The star rating in numeric format (1-5).
- `stok`: Availability status of the book.

**Example CSV Output (`hasil_buku.csv`):**
```csv
judul,harga,rating,stok
A Light in the Attic,£51.77,3,In stock
Tipping the Velvet,£53.74,1,In stock
Soumission,£50.10,1,In stock
Sharp Objects,£47.82,4,In stock
```

## 📂 Project Structure

```text
.
├── scraper.py       # Main scraper script containing the BookScraper class
├── hasil_buku.csv   # Generated output file (created after execution)
└── README.md        # Project documentation
```

---
