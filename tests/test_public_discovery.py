"""Offline regression checks for the free discovery funnel and checkout lock.

Run by the existing weekly GitHub Actions job; no network calls, buyer data,
payment credentials, messages or paid services are used.
"""
import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://kitz-labs.github.io/nordcode-raetselstudio/"


def page(name):
    return (ROOT / name).read_text(encoding="utf-8")


class TestPublicDiscovery(unittest.TestCase):
    def test_free_pages_have_search_metadata(self):
        for name, canonical in (
            ("index.html", BASE),
            ("demo.html", BASE + "demo.html"),
            ("wochenraetsel.html", BASE + "wochenraetsel.html"),
        ):
            with self.subTest(page=name):
                html = page(name)
                self.assertIn("<title>", html)
                self.assertIn('<meta name="description"', html)
                self.assertIn('<link rel="canonical" href="' + canonical + '"', html)
                self.assertIn('property="og:image"', html)
                self.assertNotIn('name="robots" content="noindex"', html)

    def test_free_funnel_navigation_remains_available(self):
        home = page("index.html")
        demo = page("demo.html")
        weekly = page("wochenraetsel.html")
        self.assertIn('href="demo.html"', home)
        self.assertIn('href="wochenraetsel.html"', home)
        self.assertIn('href="wochenraetsel.html"', demo)
        self.assertIn('href="demo.html"', weekly)
        self.assertIn('href="./#paket"', weekly)

    def test_free_entrypoints_in_sitemap(self):
        tree = ElementTree.parse(ROOT / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = {node.text for node in tree.findall(".//sm:loc", ns)}
        for url in (BASE, BASE + "demo.html", BASE + "wochenraetsel.html"):
            self.assertIn(url, urls)
        self.assertIn(BASE + "sitemap.xml", page("robots.txt"))

    def test_checkout_stays_locked_until_verified(self):
        html = page("index.html")
        self.assertRegex(html, r'<button[^>]*id="buy-button"[^>]*disabled')
        self.assertIn("Der Bezahlvorgang wird erst aktiviert", html)
        self.assertNotIn('href="https://payhip.com/b/', html)
        self.assertNotIn("window.location='https://payhip.com/", html)

    def test_sharing_is_only_user_initiated(self):
        weekly = page("wochenraetsel.html")
        self.assertIn('href="https://wa.me/?text=', weekly)
        self.assertIn('rel="noopener noreferrer"', weekly)
        self.assertNotIn("window.open('https://wa.me/", weekly)


if __name__ == "__main__":
    unittest.main()
