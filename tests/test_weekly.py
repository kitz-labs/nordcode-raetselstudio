import unittest
from datetime import date
from pathlib import Path
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
  p=mod.generate(date(2026,10,30))
  text=(Path(__file__).resolve().parents[1]/"wochenraetsel.html").read_text()
  self.assertIn(str(p["week"])+"/"+str(p["year"]),text)
  self.assertIn("n==="+str(p["result"]),text)
  self.assertIn("Impressum",text)
if __name__=="__main__": unittest.main()
