"""Offline checks for the free, original birthday treasure-hunt landing page."""
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://kitz-labs.github.io/nordcode-raetselstudio/"


class TestBirthdayPuzzle(unittest.TestCase):
    def test_page_is_searchable_and_printable(self):
        html = (ROOT / "kindergeburtstag.html").read_text(encoding="utf-8")
        self.assertIn("<title>Kindergeburtstag-Schatzsuche", html)
        self.assertIn('<link rel="canonical" href="' + BASE + 'kindergeburtstag.html"', html)
        self.assertIn('property="og:image"', html)
        self.assertIn("window.print()", html)
        self.assertIn('href="demo.html"', html)
        self.assertIn('href="wochenraetsel.html"', html)

    def test_complete_free_game_has_consistent_code(self):
        html = (ROOT / "kindergeburtstag.html").read_text(encoding="utf-8")
        for n in (1, 2, 3):
            self.assertIn('id="station' + str(n) + '"', html)
        self.assertIn("2 + 3 = 5", html)
        self.assertIn("9 − 5 = 4", html)
        self.assertIn("3 × 2 = 6", html)
        self.assertIn("<strong>546</strong>", html)
        self.assertIn('class="no-print"><summary>Lösung', html)

    def test_page_linked_from_home_and_sitemap(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="kindergeburtstag.html"', index)
        xml = ElementTree.parse(ROOT / "sitemap.xml")
        locs = {
            node.text
            for node in xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        }
        self.assertIn(BASE + "kindergeburtstag.html", locs)

    def test_no_unverified_checkout_or_buyer_data(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        page = (ROOT / "kindergeburtstag.html").read_text(encoding="utf-8")
        self.assertIn('id="buy-button" disabled', index)
        self.assertNotIn("payhip.com", page)
        self.assertNotIn("<form", page)


if __name__ == "__main__":
    unittest.main()
