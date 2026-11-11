"""Offline check that public pages do not link to missing local files or anchors.

The weekly GitHub Actions job runs these tests without network access,
customer data, payment integrations, or paid services.
"""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class PageReferences(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.anchors.add(values["id"])
        if tag == "a" and values.get("name"):
            self.anchors.add(values["name"])
        attr = "href" if tag in ("a", "link") else "src" if tag in ("img", "script") else None
        if attr and values.get(attr):
            self.references.append(values[attr])


def parse_page(path):
    parser = PageReferences()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


class TestLocalLinks(unittest.TestCase):
    def test_all_public_local_links_and_anchors_resolve(self):
        pages = sorted(ROOT.glob("*.html"))
        self.assertTrue(pages, "No public HTML pages found")
        parsed = {page.resolve(): parse_page(page) for page in pages}
        for page, data in parsed.items():
            for link in data.references:
                parts = urlsplit(link)
                if parts.scheme or parts.netloc or link.startswith("//"):
                    continue  # External pages, sharing and mailto links are not fetched.
                path = unquote(parts.path)
                if path.startswith("/"):
                    self.fail(f"Root-relative link incompatible with GitHub Pages subpath: {page.name}: {link}")
                target = (page.parent / path).resolve() if path else page
                if target.is_dir():
                    target = target / "index.html"
                with self.subTest(source=page.name, href=link):
                    self.assertTrue(target.is_relative_to(ROOT.resolve()), "Link escapes repository root")
                    self.assertTrue(target.is_file(), f"Broken internal resource: {link}")
                    if parts.fragment and target.suffix == ".html":
                        self.assertIn(
                            unquote(parts.fragment),
                            parsed.get(target, parse_page(target)).anchors,
                            f"Missing destination anchor in {target.name}: {link}",
                        )


if __name__ == "__main__":
    unittest.main()
