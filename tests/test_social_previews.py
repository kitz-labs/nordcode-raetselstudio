"""Offline regression tests for organic sharing previews on NORDCODE free pages.

No network calls, trackers, checkout actions or customer information.
The scheduled weekly workflow discovers this test automatically.
"""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://kitz-labs.github.io/nordcode-raetselstudio/"
FREE_PAGES = {
    "index.html": BASE,
    "demo.html": BASE + "demo.html",
    "wochenraetsel.html": BASE + "wochenraetsel.html",
    "kindergeburtstag.html": BASE + "kindergeburtstag.html",
}


class HeadTags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.meta = {}
        self.canonical = []
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            key = values.get("property") or values.get("name")
            if key:
                self.meta[key] = values.get("content", "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.in_head = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


class TestSocialPreviews(unittest.TestCase):
    def test_free_pages_share_canonical_url_and_local_image(self):
        for filename, canonical in FREE_PAGES.items():
            with self.subTest(page=filename):
                parser = HeadTags()
                parser.feed((ROOT / filename).read_text(encoding="utf-8"))
                self.assertEqual(parser.canonical, [canonical])
                self.assertEqual(parser.meta.get("og:url"), canonical)
                self.assertTrue(parser.title.strip())
                for key in ("description", "og:title", "og:description"):
                    self.assertTrue(parser.meta.get(key, "").strip(), f"Missing {key} on {filename}")
                self.assertIn(parser.meta.get("twitter:card"), ("summary", "summary_large_image"))
                image = parser.meta.get("og:image", "")
                self.assertTrue(image.startswith(BASE), f"Preview image must be on NORDCODE: {filename}")
                parsed = urlsplit(image)
                relative_path = unquote(parsed.path).removeprefix("/nordcode-raetselstudio/")
                target = (ROOT / relative_path).resolve()
                self.assertTrue(target.is_relative_to(ROOT.resolve()))
                self.assertTrue(target.is_file(), f"Missing social preview image: {filename}")


if __name__ == "__main__":
    unittest.main()
