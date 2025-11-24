# 🖼️ System Optimizer (v1.2 - Modern UI Release)

Ein kompaktes, professionelles Desktop-Tool zur effektiven Verwaltung und Bereinigung deines Windows-Systems und deiner Dateisammlungen.

---

## ✨ Features & Verbesserungen

### 💻 Benutzeroberfläche & Stabilität (NEU)

* **Modernes Design:** Vollständige Umstellung auf **Customtkinter (CTk)** für eine moderne, ästhetische Oberfläche mit Unterstützung für **Dark/Light Mode**.
* **Keine Blockaden:** Lange Prozesse wie Duplikatssuche und Temporärdateien-Bereinigung laufen im **Hintergrund (Multithreading)**. Die grafische Oberfläche bleibt jederzeit reaktionsschnell.
* **Zuverlässiger Start:** Behebung aller kritischen Fehler im Zusammenhang mit Multithreading und Pfad-Referenzen.

### 📁 Datei-Sortierung

Organisiere unübersichtliche Ordner schnell und präzise:

* **Sortierung nach Dateiendung** und **Erstellungsdatum** (nach Jahr/Monat/Tag).
* **Fortschrittsanzeige** für volle Transparenz während des Sortiervorgangs.

### 🧹 System-Wartung

Halte dein Windows-System sauber und aktuell:

* **Temporäre Dateien:** Analysiert und bereinigt temporäre Systemdateien, um Speicherplatz freizugeben.
* **Ungültige Verknüpfungen (LNK):** Scannt ausgewählte Verzeichnisse nach defekten Verknüpfungen und bietet eine Option zur direkten Löschung.
* **Autostart-Verwaltung:** Listet Programme aus der Registry auf, die beim Hochfahren starten, und verweist direkt auf den Windows Task Manager zur Deaktivierung.
* **Software-Upgrade (Winget):** Führt den Befehl `winget upgrade --all` aus, um alle installierten Anwendungen zu aktualisieren.

### 🔍 Duplikate finden

Sucht rekursiv in einem gewählten Verzeichnis nach **echten Inhaltsduplikaten** mithilfe des SHA-256 Hash-Verfahrens.

---

## 🚀 Installation & Start

### A) Für Endbenutzer (Empfohlen)

Die einfachste Methode ist die Verwendung des Installationsprogramms (Setup-Datei). Es ist keine separate Python-Installation erforderlich.

1.  Lade die Datei **`SystemOptimizer_Setup.exe`** von der [Hier Link zum aktuellen GitHub-Release einfügen] herunter.
2.  Führe die `SystemOptimizer_Setup.exe` aus und folge den Anweisungen.
3.  Das Programm wird im Startmenü installiert und kann dort gestartet werden.

### B) Für Entwickler (Aus dem Quellcode)

Wenn du das Programm aus dem Quellcode ausführen möchtest:

1.  **Repository klonen** und in das Verzeichnis wechseln.
2.  **Abhängigkeiten installieren:** Das Projekt erfordert `customtkinter` (für das Design).
    ```bash
    python -m pip install customtkinter
    ```
3.  **Starten:**
    ```bash
    python file_sorter.py
    ```

---

## 💻 Technologien

* **Hauptsprache:** Python 3.x
* **GUI-Framework:** `Customtkinter` (CTk)
* **Verpackung:** `PyInstaller` (EXE) & `Inno Setup` (Installer)
* **Systemfunktionen:** `winreg` (Registry-Zugriff), `subprocess` (Winget/PowerShell-Aufrufe), `threading` (Asynchrone Ausführung).

---

## 📄 Lizenz

Dieses Projekt steht unter der [Hier Lizenz einfügen, z.B. MIT License].
