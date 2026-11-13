"""Catch stale public weekly puzzles before the scheduled GitHub Actions commit.

Offline checks only: no payment calls, buyer data, network requests, or paid services.
"""
import re
import unittest
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
WEEKLY_URL = "https://kitz-labs.github.io/nordcode-raetselstudio/wochenraetsel.html"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class TestWeeklyFreshness(unittest.TestCase):
    def test_published_puzzle_matches_current_iso_week(self):
        iso = date.today().isocalendar()  # GitHub runner uses UTC; jobs are daytime UTC.
        html = (ROOT / "wochenraetsel.html").read_text(encoding="utf-8")
        match = re.search(r"<title>[^<]*KW (\d{1,2})/(\d{4})", html)
        self.assertIsNotNone(match, "Weekly page title is missing its ISO week")
        self.assertEqual(
            (int(match.group(1)), int(match.group(2))),
            (iso.week, iso.year),
            "Published puzzle is stale; do not publish an out-of-date weekly puzzle",
        )

    def test_sitemap_lastmod_is_current_week_monday(self):
        iso = date.today().isocalendar()
        expected = date.fromisocalendar(iso.year, iso.week, 1).isoformat()
        sitemap = ElementTree.parse(ROOT / "sitemap.xml")
        entries = [
            url for url in sitemap.iter(NS + "url")
            if url.findtext(NS + "loc") == WEEKLY_URL
        ]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].findtext(NS + "lastmod"), expected)

    def test_iso_week_53_still_produces_a_valid_answer(self):
        from importlib.util import module_from_spec, spec_from_file_location
        source = ROOT / "tools" / "make_weekly.py"
        spec = spec_from_file_location("nordcode_weekly_53", source)
        self.assertIsNotNone(spec)
        generator = module_from_spec(spec)
        spec.loader.exec_module(generator)
        puzzle = generator.puzzle(date.fromisocalendar(2026, 53, 1))
        self.assertEqual((puzzle["year"], puzzle["week"]), (2026, 53))
        self.assertTrue(1 <= puzzle["result"] <= 9)


if __name__ == "__main__":
    unittest.main()
