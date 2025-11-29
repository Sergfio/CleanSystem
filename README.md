# 🖼️ SysDoc Tool

A compact, professional desktop tool for effective management and cleanup of your Windows system and file collections.

---

## ✨ Features & Improvements

### 💻 User Interface & Stability (NEW)

* **Modern Design:** Complete switch to **Customtkinter (CTk)** for a modern, aesthetic interface with **Dark/Light Mode** support.
* **Non-Blocking:** Long-running processes like duplicate search and temporary file cleanup operate in the **background (Multithreading)**. The GUI remains responsive at all times.
* **Reliable Startup:** Fixes for all critical errors related to multithreading and path references.

### 📁 File Sorting

Organize cluttered folders quickly and precisely:

* Sorting by **file extension** and **creation date** (by year/month/day).
* **Progress Indicator** for full transparency during the sorting process.

### 🧹 System Maintenance

Keep your Windows system clean and up to date:

* **Temporary Files:** Analyzes and cleans temporary system files to free up disk space.
* **Invalid Shortcuts (LNK):** Scans selected directories for broken shortcuts and offers a direct deletion option.
* **Startup Management:** Lists programs from the Registry that start upon boot-up, and directly links to the Windows Task Manager for deactivation.
* **Software Upgrade (Winget):** Executes the command `winget upgrade --all` to update all installed applications.

### 🔍 Duplicate Finder

Recursively searches a chosen directory for **true content duplicates** using the SHA-256 hashing method.

---

## 🇩🇪 Deutsche Version

Hier finden Sie die deutsche Beschreibung des Tools.

---

## 🚀 Installation & Start (Installation & Startup)

### A) For End Users (Recommended) / Für Endbenutzer (Empfohlen)

The easiest method is using the installer (setup file). No separate Python installation is required.

1.  Download the file **`SystemOptimizer_Setup.exe`** from the [Insert link to the current GitHub release here] release page.
2.  Execute `SystemOptimizer_Setup.exe` and follow the instructions.
3.  The program will be installed in the Start Menu and can be launched from there.

### B) For Developers (From Source Code) / Für Entwickler (Aus dem Quellcode)

If you wish to run the program from source code:

1.  **Clone the repository** and change into the directory.
2.  **Install dependencies:** The project requires `customtkinter` (for the design).
    ```bash
    python -m pip install customtkinter
    ```
3.  **Start:**
    ```bash
    python file_sorter.py
    ```

---

## 💻 Technologies

* **Main Language:** Python 3.x
* **GUI Framework:** `Customtkinter` (CTk)
* **Packaging:** `PyInstaller` (EXE) & `Inno Setup` (Installer)
* **System Functions:** `winreg` (Registry access), `subprocess` (Winget/PowerShell calls), `threading` (Asynchronous execution).

---

## 📄 License

This project is licensed under the [MIT License].