# 🖼️ System Optimizer (v1.0)

Ein kompaktes, plattformübergreifendes Desktop-Tool zur effektiven Verwaltung und Bereinigung deines Windows-Systems und deiner Dateisammlungen.

---

## ✨ Features

Der System Optimizer kombiniert wichtige Wartungs- und Sortierfunktionen in einer einzigen, benutzerfreundlichen Oberfläche (GUI).

### 📁 Datei-Sortierung

Organisiere unübersichtliche Ordner schnell und präzise:

* **Sortierung nach Dateiendung:** Erstellt Unterordner basierend auf der Dateierweiterung (`.JPG`, `.PDF`, `.DOCX`).
* **Sortierung nach Erstellungsdatum:** Organisiert Dateien hierarchisch nach Jahr, Jahr/Monat oder Jahr/Monat/Tag.
* **Konfliktlösung:** Benennt doppelte Dateinamen automatisch um (`Datei(1).txt`).

### 🧹 System-Wartung

Halte dein Windows-System sauber und aktuell:

* **Temporäre Dateien:** Analysiert und bereinigt temporäre Systemdateien, um Speicherplatz freizugeben.
* **Ungültige Verknüpfungen (LNK):** Scannt ausgewählte Verzeichnisse nach defekten Desktop- oder Startmenü-Verknüpfungen, deren Ziel nicht mehr existiert, und bietet eine Option zur direkten Löschung.
* **Software-Upgrade:** Führt den Befehl `winget upgrade --all` aus, um alle installierten Anwendungen (über den Windows Package Manager) mit einem Klick zu aktualisieren.

### 🔍 Duplikate finden

Sucht rekursiv in einem gewählten Verzeichnis nach **echten Inhaltsduplikaten** mithilfe des SHA-256 Hash-Verfahrens.

---

## 🚀 Installation & Start

### A) Für Endbenutzer (Empfohlen)

Die einfachste Methode ist die Verwendung des Installationsprogramms. Es ist keine separate Python-Installation erforderlich.

1.  Lade die Datei **`SystemOptimizer_Setup.exe`** von der [Hier Link zum Download einfügen, z.B. GitHub-Release] herunter.
2.  Führe die `SystemOptimizer_Setup.exe` aus.
3.  Folge den Anweisungen. Das Programm wird im Startmenü installiert und kann dort gestartet werden.

### B) Für Entwickler (Aus dem Quellcode)

Wenn du das Programm aus dem Quellcode ausführen oder weiterentwickeln möchtest:

1.  **Repository klonen:**
    ```bash
    git clone [DEIN GIT REPO URL]
    cd SystemOptimizer
    ```
2.  **Abhängigkeiten installieren:**
    ```bash
    python -m pip install -r requirements.txt
    ```
    *(Hinweis: Das Skript benötigt keine externen Bibliotheken außer den Standardbibliotheken, nutzt aber `subprocess` für Winget und PowerShell-Aufrufe unter Windows.)*
3.  **Starten:**
    ```bash
    python file_sorter.py
    ```

---

## 💻 Technologien

* **Hauptsprache:** Python 3.x
* **GUI-Framework:** `tkinter`
* **Verpackung:** `PyInstaller` (für die EXE-Datei)
* **Installer-Erstellung:** `Inno Setup` (für die Setup-Datei)
* **Systemfunktionen:** `os`, `shutil`, `hashlib`, `subprocess` (für PowerShell/Winget-Aufrufe)

---

## 📄 Lizenz

Dieses Projekt steht unter der [Hier Lizenz einfügen, z.B. MIT License].