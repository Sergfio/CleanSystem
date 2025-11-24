# 🤝 Mitwirken am System Optimizer

Wir freuen uns über dein Interesse, zum System Optimizer beizutragen! Jeder Beitrag – sei es Code, Dokumentation, Fehlerberichte oder Ideen – ist willkommen.

Dieses Dokument beschreibt die Richtlinien und den empfohlenen Workflow für Mitwirkende.

## 🐛 Fehler melden (Bug Reports)

Bitte nutze den **Issues-Tab** (Probleme), um Fehler zu melden.

1.  **Suche zuerst:** Überprüfe, ob der Fehler bereits gemeldet wurde.
2.  **Verwende die Vorlage:** Nutze das **Bug Report Template** (sobald eingerichtet) oder beschreibe den Fehler so detailliert wie möglich.
3.  **Wichtige Informationen:** Gib unbedingt an, welche **Version** du verwendest und welche **Schritte zur Reproduktion** des Fehlers notwendig sind.

## ✨ Ideen und Fragen

* **Ideen und Feature Requests:** Nutze den **Discussions-Tab** (Diskussionen) unter der Kategorie **"Ideas"**.
* **Allgemeine Fragen/Support:** Nutze den **Discussions-Tab** unter der Kategorie **"Q&A"**.

## 💻 Code beitragen (Pull Requests)

Wir verwenden den Standard **Fork-and-Feature-Branch-Workflow**.

### Voraussetzungen

1.  Stelle sicher, dass du die neueste Version von Python und Git installiert hast.
2.  Installiere die Abhängigkeiten: `pip install customtkinter`
3.  Halte dich an den **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)**.

### Empfohlener Workflow

1.  **Fork:** Erstelle eine **Fork** des Repositories auf deinem GitHub-Account.
2.  **Klonen:** Klone deine Fork lokal auf deinen Computer:
    ```bash
    git clone [https://github.com/](https://github.com/)[DEIN-GITHUB-NAME]/CleanSystem.git
    cd CleanSystem
    ```
3.  **Branch erstellen:** Erstelle einen neuen Feature-Branch. Verwende beschreibende Namen (z.B. `feat/winget-upgrade-fix` oder `docs/readme-update`).
    ```bash
    git checkout -b feature/neue-funktion
    ```
4.  **Codieren:** Implementiere deine Änderungen. Führe lokale Tests durch, um sicherzustellen, dass die GUI und die Funktionen stabil bleiben.
    * *Hinweis:* Achte darauf, dass dein Code im **Hintergrund (Threading)** läuft, wenn die Ausführung länger als 500 ms dauert (z.B. Duplikatssuche, Analyse).
5.  **Committen:** Committe deine Arbeit mit **prägnanten** und **klaren** Nachrichten. Wir bevorzugen [Conventional Commits] (z.B. `fix:`, `feat:`, `docs:`).
    ```bash
    git commit -m "feat: Implementierung einer neuen Funktion X"
    ```
6.  **Pushen:** Pushe deinen Branch zu deiner Fork auf GitHub.
    ```bash
    git push origin feature/neue-funktion
    ```
7.  **Pull Request (PR):** Erstelle einen Pull Request von deinem Feature-Branch zum **`main`**-Branch dieses Repositories.

---

## 🛡️ Sicherheitslücken

Bitte **melde Sicherheitslücken** nicht über den Issues-Tab, sondern folge unserer **[SECURITY.md](SECURITY.md)**-Richtlinie für eine vertrauliche Meldung.
