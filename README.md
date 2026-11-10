# NORDCODE Rätselstudio

## Basisstatus 04.11.2026 (historisch)

- Neues, eigenständiges Produkt (keine vorhandenen KI/Spotify/Web-Template-Dienstleistungen).
- Website: https://kitz-labs.github.io/nordcode-raetselstudio/
- Kostenloses interaktives Demo-Rätsel funktioniert; Lösung 8.
- GitHub Pages: öffentlich ausgeliefert; alle HTML- und Rechteseiten HTTP 200.
- Kostenloses Wochenrätsel: **reguläre Zeitplanläufe am 02.11. und 03.11.2026 erfolgreich** (Generator und Tests). KW 45/2026 ist live. Ein separater Dienstags-Fallback sichert den Wochenplan ab; der nächste Wochenwechsel bleibt zu beobachten.
- Bezahlprodukt **Rettet den Nordstern**: privates, lokal gesichertes ZIP mit 12-seitigem Spiel und 3-seitigem Lösungsheft erstellt und auf Integrität sowie Lösungslogik geprüft.
- Payhip Free: Verkäuferkonto angelegt, digitale ZIP-Datei samt eigenem Cover hochgeladen.
- Payhip-Produktlink (vorerst unsichtbar): https://payhip.com/b/NSIgO
- Kaufpreis 9,90 EUR, einmalig.
- **0 bezahlte Bestellungen / 0,00 EUR Umsatz (04.11.2026)** in Payhip Customers und Analytics read-only geprüft; Auszahlungshistorie nicht separat verifiziert. Payhip zeigt weder Stripe noch PayPal verbunden. Produkt bis dahin unsichtbar; Kaufbutton der Website deaktiviert.
- Payhip Free: 0 EUR/Monat + 5 % Payhip-Gebühr pro Verkauf plus Zahlungsgebühren (aktuelle Bedingungen vor Livegang prüfen).
- Rechtliche Seiten vorhanden; finale Verbraucherrechts-/Steuerprüfung vor Freischaltung.
- Keine Käuferdaten und keine Stripe API-Keys im GitHub-Repository.
- Ziel: sichere automatische Checkout-Auslieferung von Payhip und messbare organische Konversion nach Stripe-Freigabe.

## Aktuelle Technikprüfung 10.11.2026

- **KW 46/2026 im Repository aktualisiert**, Sitemap-Datum 09.11.2026.
- Zwei geplante Wochenrätsel-Läufe vom **09.11.2026 erfolgreich**, inklusive Generator, Tests und Commit-Prüfung: [erster Lauf](https://github.com/kitz-labs/nordcode-raetselstudio/actions/runs/42630721618), [zweiter Lauf](https://github.com/kitz-labs/nordcode-raetselstudio/actions/runs/42710994052). Der zweite Lauf wurde von GitHub verzögert ausgeführt.
- [GitHub-Pages-Deployment vom 09.11.](https://github.com/kitz-labs/nordcode-raetselstudio/actions/runs/42630742086) erfolgreich. Eine erneute HTTP-Abfrage der öffentlichen Website war am 10.11.2026 aufgrund nicht verfügbarer Browser- bzw. DNS-Verbindung nicht möglich; Erfolg des Deployments ist kein direkter HTTP-Nachweis.
- Interne Qualitätssicherung um `tests/test_discoverability.py` ergänzt: Sitemap, Canonical-Tags, interne Links zu Gratisangeboten und Wochenrätsel-Datum. Die neue Testdatei wird beim nächsten Workflow-Testlauf mit ausgeführt; **noch kein CI-Nachweis für diese neue Datei**.
- Payhip-Konto am 10.11. wegen nicht verfügbarer Safari-Verbindung **nicht erneut lesbar**. Letzter belegter Kontostand bleibt **0 Verkäufe / 0,00 EUR Umsatz vom 04.11.2026**; neue Verkäufe und Auszahlungen seither unbekannt. Kein Liveverkauf freigegeben.
- Kostenlose Wachstumsoption: Die Kindergeburtstag-Schatzsuche auch direkt auf der Wochenrätselseite intern verlinken, um Besucher ohne Werbung zu einem zweiten Gratisangebot zu führen. Öffentlich noch nicht geändert.

## Automatisierung

GitHub Actions plant den Wochenrätsel-Generator montags um 05:21 UTC, einen zweiten idempotenten Montagsversuch um 12:19 UTC (seit 09.11.2026) und als weitere Absicherung dienstags um 08:37 UTC. Hintergrund: GitHub kann geplante Läufe verzögern; der zusätzliche Montagsversuch lief am 09.11.2026 erfolgreich (durch GitHub verzögert). Der Generator committet nur bei Inhaltsänderung. Die Wochenrätselseite enthält eine Open-Graph-Linkvorschau und einen freiwilligen Teilen-Link, der Nachrichten nicht automatisch versendet. Der Workflow ist getestet und benötigt keine kostenpflichtige KI. Die separate tägliche ChatGPT-Automation kontrolliert Umsatz und technische Verfügbarkeit, soweit die verbundenen Werkzeuge zugänglich sind.

## Sicheres Go-Live-Gate

1. Stripe-Login und OAuth-Verbindung in Payhip im vorhandenen Safari-Tab abschließen (keine Passwörter in Chats).
2. In Payhip `Settings → Payment Details` den verbundenen Stripe-Account kontrollieren, ohne Kontodaten offenzulegen.
3. Produktdownload und Endpreis durch den **offiziellen** Payhip-Testcheckout prüfen; keine Echtgeld-Testkäufe zu Lasten der Person.
4. Widerspruchsfreie steuerliche und rechtliche Texte sowie Endpreis prüfen.
5. Produkt in Payhip sichtbar stellen. Dann Website-Kaufbutton auf https://payhip.com/b/NSIgO aktivieren.
6. Verfügbarkeit von Website und Checkout über Smartphone prüfen. Eine erste reale Bestellung nur nach Stripe-Beleg als Umsatz verbuchen.

## Sicherheit

Es dürfen keine produktiven Zahlungen, Stripe-API-Credentials, privaten Puzzle-ZIP-Dateien, Passwörter oder Kundenlisten im GitHub-Repo gespeichert werden. Die passwortgeschützte Payhip-Kontoanmeldung liegt im macOS-Schlüsselbund auf dem eigenen Mac.
