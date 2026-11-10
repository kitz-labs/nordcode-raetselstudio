"""Guard organic entry points and weekly puzzle indexing without external services."""
import re
import unittest
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://kitz-labs.github.io/nordcode-raetselstudio/"
PAGES = {
    "index.html": "",
    "demo.html": "demo.html",
    "wochenraetsel.html": "wochenraetsel.html",
    "kindergeburtstag.html": "kindergeburtstag.html",
}
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class TestDiscoverability(unittest.TestCase):
    def test_free_entry_pages_are_indexable(self):
        sitemap = ElementTree.parse(ROOT / "sitemap.xml")
        locations = {node.text for node in sitemap.iter(NS + "loc")}
        for filename, url_path in PAGES.items():
            with self.subTest(page=filename):
                html = (ROOT / filename).read_text(encoding="utf-8")
                canonical = BASE + url_path
                self.assertIn(canonical, locations)
                self.assertIn(f'rel="canonical" href="{canonical}"', html)
                self.assertIn('name="description"', html)

    def test_homepage_reaches_all_free_entry_points(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        for url_path in ("demo.html", "wochenraetsel.html", "kindergeburtstag.html"):
            with self.subTest(link=url_path):
                self.assertIn(f'href="{url_path}"', homepage)

    def test_weekly_sitemap_date_matches_visible_iso_week(self):
        html = (ROOT / "wochenraetsel.html").read_text(encoding="utf-8")
        match = re.search(r"KW (\d{1,2})/(\d{4})", html)
        self.assertIsNotNone(match, "Weekly page has no visible ISO week")
        week, year = map(int, match.groups())
        monday = date.fromisocalendar(year, week, 1).isoformat()
        sitemap = ElementTree.parse(ROOT / "sitemap.xml")
        entries = [
            node for node in sitemap.iter(NS + "url")
            if node.findtext(NS + "loc") == BASE + "wochenraetsel.html"
        ]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].findtext(NS + "lastmod"), monday)


if __name__ == "__main__":
    unittest.main()
