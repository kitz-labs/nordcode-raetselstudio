import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from importlib.machinery import SourceFileLoader

mod=SourceFileLoader("make_weekly",str(Path(__file__).resolve().parents[1]/"tools"/"make_weekly.py")).load_module()

class TestWeekly(unittest.TestCase):
    def test_every_week_has_one_valid_digit(self):
        for year in (2026,2027):
            for week in range(1,53):
                try: day=date.fromisocalendar(year,week,1)
                except ValueError: continue
                p=mod.puzzle(day)
                self.assertEqual(p["result"],p["red"]*3-p["removed"])
                self.assertTrue(1 <= p["result"] <= 9)

    def test_generated_page_shows_correct_answer_check(self):
        previous_root=mod.ROOT
        with TemporaryDirectory() as folder:
            try:
                mod.ROOT=Path(folder)
                p=mod.generate(date(2026,10,30))
                text=(Path(folder)/"wochenraetsel.html").read_text(encoding="utf-8")
            finally:
                mod.ROOT=previous_root
        self.assertIn(str(p["week"])+"/"+str(p["year"]),text)
        self.assertIn("n==="+str(p["result"]),text)
        self.assertIn("Impressum",text)
        self.assertIn('property="og:image"',text)
        self.assertIn('https://wa.me/?text=',text)
        self.assertIn('Kostenloses Rätsel zum Ausdrucken',text)
        self.assertIn('onclick="window.print()"',text)
        self.assertIn('href="./#paket"',text)
        self.assertIn('Der Verkauf startet erst nach geprüfter Zahlung und Auslieferung.',text)


    def test_sitemap_weekly_lastmod_is_idempotent_and_updates_on_new_week(self):
        previous_root = mod.ROOT
        with TemporaryDirectory() as folder:
            try:
                mod.ROOT = Path(folder)
                path = Path(folder) / "sitemap.xml"
                path.write_text(
                    '<?xml version="1.0" encoding="utf-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    '<url><loc>https://kitz-labs.github.io/nordcode-raetselstudio/</loc></url>\n'
                    '<url><loc>https://kitz-labs.github.io/nordcode-raetselstudio/wochenraetsel.html</loc></url>\n'
                    '</urlset>', encoding="utf-8"
                )
                mod.generate(date(2026, 11, 2))
                first = path.read_text(encoding="utf-8")
                self.assertIn("<lastmod>2026-11-02</lastmod>", first)
                mod.generate(date(2026, 11, 3))
                self.assertEqual(first, path.read_text(encoding="utf-8"))
                mod.generate(date(2026, 11, 9))
                self.assertIn("<lastmod>2026-11-09</lastmod>", path.read_text(encoding="utf-8"))
                self.assertNotIn("<lastmod>2026-11-02</lastmod>", path.read_text(encoding="utf-8"))
            finally:
                mod.ROOT = previous_root

    def test_checkout_remains_disabled_without_verified_gateway(self):
        index = (Path(__file__).resolve().parents[1] / "index.html").read_text(encoding="utf-8")
        self.assertRegex(index, r'<button[^>]*id="buy-button"[^>]*disabled')
        self.assertIn("Der Bezahlvorgang wird erst aktiviert", index)

if __name__=="__main__":
    unittest.main()
