#!/usr/bin/env python3
"""Generates a fresh, verifiable public mini-puzzle each ISO week without API calls."""
from datetime import date
from pathlib import Path
from html import escape
import argparse
ROOT = Path(__file__).resolve().parents[1]
def puzzle(when):
    iso=when.isocalendar()
    seed=(iso.year*53+iso.week)
    red=2+(seed%3)
    gold=red*2
    removed=red+1
    result=red+gold-removed
    assert 0<result<10
    return dict(year=iso.year,week=iso.week,red=red,gold=gold,removed=removed,result=result)
def generate(when=date.today()):
    d=puzzle(when)
    body=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wochenrätsel KW {d["week"]}/{d["year"]} | NORDCODE</title><meta name="description" content="Kostenloses originales Familienrätsel der Woche. Direkt am Handy lösen oder ausdrucken."><link rel="stylesheet" href="styles.css"><link rel="canonical" href="https://kitz-labs.github.io/nordcode-raetselstudio/wochenraetsel.html"></head><body><header class="topbar"><a href="./" class="brand">✳ NORDCODE</a><nav><a href="./">Start</a><a href="demo.html">Probemission</a></nav></header><main class="shell simple-main"><span class="eyebrow">DAS KOSTENLOSE WOCHENRÄTSEL · KW {d["week"]}/{d["year"]}</span><h1>Die Laternenwerkstatt</h1><p>In der Sternenstadt stehen <strong>{d["red"]} rote Laternen</strong> und genau doppelt so viele goldene. Der Wind bläst <strong>{d["removed"]} Laternen</strong> aus. Wie viele bleiben an?</p><div class="card"><p>So findest du die Antwort: zuerst die goldenen Laternen zählen, dann die roten addieren und die erloschenen abziehen.</p><label for="weekly">Deine Antwort</label><div class="answer-box"><input id="weekly" inputmode="numeric" maxlength="1" aria-describedby="feedback"><button class="button primary" id="solve">Antwort prüfen</button></div><p id="feedback" role="status" aria-live="polite"></p><details><summary>Hinweis anzeigen</summary><p class="hint">Goldene: {d["red"]} × 2 = {d["gold"]}. Dann alle zusammenzählen.</p></details></div><a href="demo.html" class="button outline">Nächste Gratismission ↗</a></main><footer><div class="shell foot"><div class="brand">✳ NORDCODE</div><div class="foot-links"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></div></div></footer><script>document.querySelector("#solve").addEventListener("click",()=>{{const n=Number(document.querySelector("#weekly").value);document.querySelector("#feedback").textContent=n==={d["result"]}?"Richtig! Diese Woche hast du das Licht gerettet. ✦":"Noch nicht – prüfe das Ergebnis deiner Rechnung.";}});</script></body></html>'''
    (ROOT/"wochenraetsel.html").write_text(body,encoding="utf-8")
    return d
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--date",type=date.fromisoformat,default=date.today())
    a=parser.parse_args()
    print(generate(a.date))
