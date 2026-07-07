"""
Web Scraper - Books to Scrape
=============================

Skrip scraper untuk mengekstrak data buku dari https://books.toscrape.com.
Didesain dengan pendekatan Object-Oriented Programming (OOP), Type Hinting,
Logging, Error Handling, dan Command-Line Interface (CLI).

Cara Penggunaan:
    python scraper.py --pages 5 --output hasil_buku.csv
"""

import argparse
import csv
import logging
import sys
from typing import List, Dict, Optional, Any

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class BookScraper:
    """Kelas utama untuk melakukan scraping pada situs books.toscrape.com."""

    BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
    
    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def __init__(self, timeout: int = 10):
        """
        Inisialisasi scraper dengan session untuk performa lebih baik.

        Args:
            timeout (int): Waktu maksimal untuk menunggu respons HTTP.
        """
        self.timeout = timeout
        # Menggunakan Session untuk mempercepat koneksi secara keseluruhan (connection pooling)
        self.session = requests.Session()

    def scrape_page(self, page_number: int) -> Optional[List[Dict[str, Any]]]:
        """
        Mengambil data buku dari nomor halaman tertentu.

        Args:
            page_number (int): Nomor halaman yang ingin di-scrape.

        Returns:
            Optional[List[Dict[str, Any]]]: Daftar dictionary berisi data buku,
                                            atau None jika halaman tidak ditemukan/error.
        """
        url = self.BASE_URL.format(page_number)
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()  # Memunculkan error jika status HTTP bukan 200 OK
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                logger.info(f"Halaman {page_number} tidak ditemukan (akhir katalog).")
                return None
            logger.error(f"HTTP error pada halaman {page_number}: {e}")
            return None
        except RequestException as e:
            logger.error(f"Terjadi kesalahan koneksi pada halaman {page_number}: {e}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        data = []
        for book in books:
            try:
                title = book.h3.a.get("title", "")
                price_text = book.find("p", class_="price_color").text.strip()
                
                # Mengambil rating (contoh: ['star-rating', 'Three'])
                rating_classes = book.p.get("class", [])
                rating_word = rating_classes[1] if len(rating_classes) > 1 else "None"
                rating = self.RATING_MAP.get(rating_word, 0)
                
                availability = book.find("p", class_="instock availability").text.strip()

                data.append({
                    "judul": title,
                    "harga": price_text,
                    "rating": rating,
                    "stok": availability
                })
            except (AttributeError, IndexError, TypeError) as e:
                logger.warning(f"Gagal memparsing data buku di halaman {page_number}: {e}")
                continue

        return data

    def scrape_multiple_pages(self, max_pages: int) -> List[Dict[str, Any]]:
        """
        Mengambil data buku dari beberapa halaman sekaligus.

        Args:
            max_pages (int): Batas maksimum halaman yang akan di-scrape.

        Returns:
            List[Dict[str, Any]]: Kumpulan data buku dari semua halaman.
        """
        all_books = []
        for page in range(1, max_pages + 1):
            logger.info(f"Mengambil data dari halaman {page}...")
            result = self.scrape_page(page)
            
            if result is None:
                logger.info("Proses scraping berhenti.")
                break
                
            all_books.extend(result)
            
        return all_books


def save_to_csv(books: List[Dict[str, Any]], filename: str) -> None:
    """
    Menyimpan hasil scraping ke dalam format file CSV.

    Args:
        books (List[Dict[str, Any]]): Daftar data buku.
        filename (str): Nama file CSV tempat penyimpanan.
    """
    if not books:
        logger.warning("Tidak ada data untuk disimpan.")
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["judul", "harga", "rating", "stok"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(books)
            
        logger.info(f"Selesai! {len(books)} buku berhasil disimpan ke '{filename}'.")
    except IOError as e:
        logger.error(f"Gagal menyimpan data ke file {filename}: {e}")


def main():
    """Fungsi utama program (Entry point)."""
    parser = argparse.ArgumentParser(
        description="Skrip Web Scraper Profesional untuk situs Books to Scrape."
    )
    parser.add_argument(
        "-p", "--pages",
        type=int,
        default=5,
        help="Jumlah maksimum halaman yang ingin di-scrape (default: 5)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="hasil_buku.csv",
        help="Nama file hasil output CSV (default: hasil_buku.csv)"
    )
    
    args = parser.parse_args()

    scraper = BookScraper(timeout=10)
    logger.info(f"Memulai proses scraping maksimal {args.pages} halaman...")
    
    hasil = scraper.scrape_multiple_pages(max_pages=args.pages)
    
    save_to_csv(hasil, filename=args.output)
    
    if hasil:
        print("\n--- Contoh Data ---")
        for b in hasil[:5]:
            print(b)


if __name__ == "__main__":
    main()
