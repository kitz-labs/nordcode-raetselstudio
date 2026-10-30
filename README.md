# NORDCODE Rätselstudio

Eigenständiges digitales Mikroprodukt, neu aufgebaut am 30.10.2026.

- Originale druckbare Escape-Spiele für Familien
- Gratis-Mission im Browser
- Mobile-first, keine externen JS-Frameworks oder Trackingdienste
- Öffentliche Demo: https://kitz-labs.github.io/nordcode-raetselstudio/
- Kostenlose Infrastruktur: GitHub Pages + öffentliche GitHub Actions
- Das käufliche PDF-Paket liegt **nicht** in diesem öffentlichen Repository
- Checkout: **absichtlich deaktiviert**, solange sichere und verlässliche Auslieferung sowie Compliance nicht nachgewiesen sind
- Vertraglicher Betreiber: AI Kitz Art & Labs e.U. (bestehendes Unternehmen)

## Betrieb

Die öffentliche Website wird über GitHub Pages ausgeliefert. Der Workflow .github/workflows/wochenraetsel.yml generiert automatisch jede Woche ein neues kostenloses Originalrätsel aus einer geprüften Rechenlogik. Hierzu sind weder KI-API-Keys noch bezahlte Dienste notwendig.

## Qualitätschecks
- Seitenstruktur & Links per grep/curl
- iPhone-Viewport, responsives CSS
- Code-Eingabe im Demo mit 8 -> erfolgreich, mit anderen Ziffern -> Fehlertext
- Puzzle-Pack-Lösungen automatisiert gegen Spielgenerator geprüft
- Checkout bleibt deaktiviert bis Auslieferung verifiziert ist

## Business
Testpreis 9,90 € pro einmaligem Familien-PDF-Paket. Stripe Standardkarten AT derzeit 1,5 % + 0,25 € je erfolgreicher Zahlung; weitere Gebühren sind möglich. Umsätze sind nicht garantiert. In Deutschland/Österreich geltende Verbraucher- und Steuerpflichten beachten.

## Sicherheit
Keine Secrets in Git. Kein Käuferdatenspeicher im Frontend. Keine automatisierten Spam-Mails. Kein Datenbezug zum Bankkonto des Projektinhabers. Bei späterer Zahlung: Stripe Checkout/Payment Links, signierte Webhooks und sichere Auslieferung vor Live-Schaltung.

## Status
Website & Demo lauffähig; Produkt im privaten lokalen Projektverzeichnis generiert. Echtgeld-Verkauf wird erst nach verifizierter Auslieferung und Compliance aktiviert.
