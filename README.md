# NORDCODE Rätselstudio

## Status 02.11.2026

- Neues, eigenständiges Produkt (keine vorhandenen KI/Spotify/Web-Template-Dienstleistungen).
- Website: https://kitz-labs.github.io/nordcode-raetselstudio/
- Kostenloses interaktives Demo-Rätsel funktioniert; Lösung 8.
- GitHub Pages: öffentlich ausgeliefert; alle HTML- und Rechteseiten HTTP 200.
- Kostenloses Wochenrätsel: manueller GitHub-Actions-Lauf am 02.11.2026 mit **success** (inkl. Tests). KW 45/2026 ist live. Montags-Schedule am 02.11. wurde nicht ausgelöst; dienstags ist jetzt ein kostenloser Fallback-Termin vorgesehen. Ein regulärer Zeitplanlauf ist weiterhin nicht bestätigt.
- Bezahlprodukt **Rettet den Nordstern**: privates, lokal gesichertes ZIP mit 12-seitigem Spiel und 3-seitigem Lösungsheft erstellt und auf Integrität sowie Lösungslogik geprüft.
- Payhip Free: Verkäuferkonto angelegt, digitale ZIP-Datei samt eigenem Cover hochgeladen.
- Payhip-Produktlink (vorerst unsichtbar): https://payhip.com/b/NSIgO
- Kaufpreis 9,90 EUR, einmalig.
- **0 bezahlte Bestellungen / 0,00 EUR Umsatz (02.11.2026)** in Payhip Customers und Analytics read-only geprüft; Auszahlungsdaten nicht separat verifiziert. Payhip-/Stripe-Zahlungsverbindung erfordert Abschluss der Stripe-OAuth-Anmeldung mit dem Kontoinhaber. Produkt bis dahin unsichtbar; Kaufbutton der Website deaktiviert.
- Payhip Free: 0 EUR/Monat + 5 % Payhip-Gebühr pro Verkauf plus Zahlungsgebühren (aktuelle Bedingungen vor Livegang prüfen).
- Rechtliche Seiten vorhanden; finale Verbraucherrechts-/Steuerprüfung vor Freischaltung.
- Keine Käuferdaten und keine Stripe API-Keys im GitHub-Repository.
- Ziel: sichere automatische Checkout-Auslieferung von Payhip und messbare organische Konversion nach Stripe-Freigabe.

## Automatisierung

GitHub Actions plant den Wochenrätsel-Generator montags um 05:21 UTC und als Absicherung dienstags um 08:37 UTC. Der Generator committet nur bei Inhaltsänderung. Die Wochenrätselseite enthält eine Open-Graph-Linkvorschau und einen freiwilligen Teilen-Link, der Nachrichten nicht automatisch versendet. Der Workflow ist getestet und benötigt keine kostenpflichtige KI. Die separate tägliche ChatGPT-Automation kontrolliert Umsatz und technische Verfügbarkeit, soweit die verbundenen Werkzeuge zugänglich sind.

## Sicheres Go-Live-Gate

1. Stripe-Login und OAuth-Verbindung in Payhip im vorhandenen Safari-Tab abschließen (keine Passwörter in Chats).
2. In Payhip `Settings → Payment Details` den verbundenen Stripe-Account kontrollieren, ohne Kontodaten offenzulegen.
3. Produktdownload und Endpreis durch den **offiziellen** Payhip-Testcheckout prüfen; keine Echtgeld-Testkäufe zu Lasten der Person.
4. Widerspruchsfreie steuerliche und rechtliche Texte sowie Endpreis prüfen.
5. Produkt in Payhip sichtbar stellen. Dann Website-Kaufbutton auf https://payhip.com/b/NSIgO aktivieren.
6. Verfügbarkeit von Website und Checkout über Smartphone prüfen. Eine erste reale Bestellung nur nach Stripe-Beleg als Umsatz verbuchen.

## Sicherheit

Es dürfen keine produktiven Zahlungen, Stripe-API-Credentials, privaten Puzzle-ZIP-Dateien, Passwörter oder Kundenlisten im GitHub-Repo gespeichert werden. Die passwortgeschützte Payhip-Kontoanmeldung liegt im macOS-Schlüsselbund auf dem eigenen Mac.
