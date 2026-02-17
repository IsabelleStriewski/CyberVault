# CyberVault - Encrypted Password Manager (MVP)

**CyberVault** ist ein in Python entwickelter **Prototyp (MVP - Minimum Viable Product)** für die sichere Verwaltung von Zugangsdaten. Bei der Entwicklung stand nicht die grafische Oberfläche, sondern die Implementierung einer robusten **Sicherheitsarchitektur** und der Schutz vor gängigen Angriffsvektoren (-punkten) im Fokus.

---

## Kernfunktionen & Sicherheitsmerkmale

### 1. Authentifizierung (Master-Passwort)
Der Zugang zum Tresor wird durch ein Master-Passwort geschützt. Um die Sicherheit zu maximieren, wird das Passwort niemals im Klartext gespeichert.
* **Verfahren:** Einweg-Hashing mittels **SHA-256**.
* **Logik:** Das Passwort wird beim Login gehasht und mit dem gespeicherten Hash in der Datei `.secret` verglichen.

### 2. Daten-Verschlüsselung (Database)
Die gesamte Passwort-Datenbank (`vault.json`) wird als verschlüsselter Binärblock gespeichert.
* **Algorithmus:** **Fernet (AES-128)**.
* **Integrität:** Durch die Verwendung von Fernet wird sichergestellt, dass jede Manipulation an der Datenbankdatei (z. B. durch einen Angreifer) beim Entschlüsselungsvorgang sofort erkannt wird.

### 3. Key-Management (Separation of Concerns)
Ein zentrales Feature dieses Projekts ist die logische Trennung von Quellcode und kryptografischen Schlüsseln.
* **Implementierung:** Der Verschlüsselungs-Key wird in den **System-Umgebungsvariablen** (`CYBERVAULT_KEY`) des Betriebssystems hinterlegt.
* **Sicherheitsvorteil:** Selbst bei einem Diebstahl des Projektordners oder des Quellcodes bleibt der Tresor ohne den systemgebundenen Schlüssel unlesbar.

---

## Installation & Setup

### Voraussetzungen
* Python 3.x
* Installierte Bibliotheken: `pip install cryptography`

### Schnellstart
1. Repository klonen.
2. Abhängigkeiten installieren: `pip install -r requirements.txt`.
3. Anwendung starten: `python src/main.py`.
4. Folgen Sie den Anweisungen zur Ersteinrichtung (Master-Passwort & Key-Generierung).

> **Wichtiger Hinweis:** Nach der Generierung des Schlüssels sollte dieser als Umgebungsvariable `CYBERVAULT_KEY` im System hinterlegt werden, um die Sicherheitsfeatures voll zu nutzen.

### Konfiguration der Umgebungsvariablen

Damit CyberVault den Schlüssel erkennt, muss dieser im System hinterlegt werden:

#### Windows (PowerShell)

powershell
setx CYBERVAULT_KEY "DEIN_GENERIERTER_SCHLÜSSEL"```

# Wichtig: Starten Sie VS Code oder Ihr Terminal danach neu, damit die Änderungen wirksam werden.

#### Linux (Bash)
Da das Projekt Linux-optimiert ist (LPI Linux Essentials Standard), nutzen Sie:

echo 'export CYBERVAULT_KEY="DEIN_GENERIERTER_SCHLÜSSEL"' >> ~/.bashrc
source ~/.bashrc

---

## Roadmap (Nächste Schritte)

Dieses Projekt wird aktiv weiterentwickelt. Geplante Meilensteine sind:

- [ ] **Speicher-Optimierung:** Umstellung auf Stream-Processing beim Laden der Datenbank, um den RAM-Verbrauch bei großen Datensätzen zu minimieren
- [ ] **GUI-Entwicklung:** Implementierung einer modernen grafischen Benutzeroberfläche mittels `CustomTkinter`
- [ ] **Erweiterte Validierung:** Robuste Fehlerbehandlung für Nutzereingaben (Input Validation)

---

## Entwicklungsprozess

Dieses Projekt wurde schrittweise entwickelt, um die Komplexität und Sicherheit systematisch zu erhöhen:

1.  **Phase 1 (Grundlogik):** Erstellung der Basis-Struktur (Dictionary) und Speicherung der Daten im JSON-Format.
2.  **Phase 2 (Authentifizierung):** Implementierung des Master-Logins. Umstellung von Klartext-Speicherung auf SHA-256 Hashing zum Schutz des Master-Passworts.
3.  **Phase 3 (Kryptografie):** Integration der Fernet-Verschlüsselung (AES-128), um die gesamte Datenbank-Datei unlesbar zu machen.
4.  **Phase 4 (Sicherheit & Key-Management):** Migration des Verschlüsselungs-Keys von einer lokalen Datei in die System-Umgebungsvariablen, um Schloss und Schlüssel physisch voneinander zu trennen.

---

## Über das Projekt
CyberVault dient als Demonstration für den sicheren Umgang mit sensiblen Daten. Es zeigt mein Verständnis für:
* **Kryptografische Konzepte** (Symmetrische Verschlüsselung & Hashing)
* **Dateisystem-Interaktion** (JSON & Binärdaten)
* **Umgebungskonfiguration** (Environment Variables)

* **Logging** (Audit-Trail in `access.log`)
