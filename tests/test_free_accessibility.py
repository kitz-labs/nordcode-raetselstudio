"""Offline accessibility smoke checks for NORDCODE's free entry pages.

Protects the first visit from keyboard/screen-reader regressions.
No network, tracking, payments, personal data, or external dependencies.
"""
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREE_PAGES = ("index.html", "demo.html", "wochenraetsel.html", "kindergeburtstag.html")


class AccessibilityTags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.language = None
        self.h1_count = 0
        self.main_count = 0
        self.has_viewport = False
        self.input_ids = {}
        self.label_targets = set()
        self.live_region_ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.language = a.get("lang")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "main":
            self.main_count += 1
        elif tag == "meta" and a.get("name") == "viewport":
            self.has_viewport = bool(a.get("content"))
        elif tag == "input":
            self.input_ids[a.get("id")] = a.get("aria-describedby")
        elif tag == "label" and a.get("for"):
            self.label_targets.add(a["for"])
        if a.get("id") and (a.get("aria-live") == "polite" or a.get("role") == "status"):
            self.live_region_ids.add(a["id"])


def parse_page(name):
    parser = AccessibilityTags()
    parser.feed((ROOT / name).read_text(encoding="utf-8"))
    return parser


class TestFreeAccessibility(unittest.TestCase):
    def test_each_free_page_has_one_clear_heading_and_main_region(self):
        for name in FREE_PAGES:
            with self.subTest(page=name):
                page = parse_page(name)
                self.assertEqual(page.language, "de", f"{name} must declare German")
                self.assertEqual(page.h1_count, 1, f"{name} must have exactly one H1")
                self.assertEqual(page.main_count, 1, f"{name} must have exactly one main region")
                self.assertTrue(page.has_viewport, f"{name} needs mobile viewport metadata")

    def test_free_puzzle_inputs_have_labels_and_accessible_feedback(self):
        for name in ("demo.html", "wochenraetsel.html"):
            with self.subTest(page=name):
                page = parse_page(name)
                self.assertTrue(page.input_ids, f"{name} needs an answer input")
                for input_id, description_id in page.input_ids.items():
                    self.assertTrue(input_id, "Inputs must have a stable id")
                    self.assertIn(input_id, page.label_targets, "Input needs a visible label")
                    self.assertIn(description_id, page.live_region_ids, "Feedback needs an announced live region")


if __name__ == "__main__":
    unittest.main()
