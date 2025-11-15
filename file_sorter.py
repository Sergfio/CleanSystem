import tkinter as tk
from tkinter import filedialog, messagebox, ttk # ttk ist neu für Tabs!
import os
import shutil
from datetime import datetime
import subprocess

class FileSorterApp:
    def __init__(self, master):
        self.master = master
        master.title("🖼️ System- & Datei-Optimierer")
        master.resizable(False, False)
        
        # --- Variablen für Sortierung ---
        self.source_dir = tk.StringVar(value="")
        self.sort_by_extension = tk.BooleanVar(value=True) 
        self.sort_by_date = tk.BooleanVar(value=False)
        self.date_granularity = tk.StringVar(value="Year")
        
        # Das Label für das Bereinigungsergebnis wird in setup_system_tab initialisiert
        self.cleanup_result_label = None 
        
        self.setup_widgets()
        
    def setup_widgets(self):
        """Erstellt die Tab-Struktur und ruft die Einrichtungsfunktionen für jeden Tab auf."""
        
        # 1. Notebook (Tab-Control) erstellen
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)
        
        # 2. Tabs erstellen
        self.tab_sorter = tk.Frame(self.notebook, padx=5, pady=5)
        self.tab_system = tk.Frame(self.notebook, padx=5, pady=5)
        
        self.notebook.add(self.tab_sorter, text="📁 Datei-Sortierung")
        self.notebook.add(self.tab_system, text="🧹 System-Wartung")
        
        # 3. Widgets für jeden Tab einrichten
        self.setup_sorter_tab(self.tab_sorter)
        self.setup_system_tab(self.tab_system)

    def setup_sorter_tab(self, tab):
        """Erstellt die Widgets für den Datei-Sorter Tab."""
        
        # Frame für die Verzeichnisauswahl
        dir_frame = tk.LabelFrame(tab, text="📁 1. Quellordner auswählen", padx=10, pady=10)
        dir_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(dir_frame, text="Pfad:").pack(side=tk.LEFT, padx=(0, 5))
        
        entry = tk.Entry(dir_frame, textvariable=self.source_dir, width=50, state='readonly')
        entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5))
        
        tk.Button(dir_frame, text="Durchsuchen...", command=self.browse_directory).pack(side=tk.LEFT)
        
        # Frame 2: Kriterien-Auswahl
        criteria_frame = tk.LabelFrame(tab, text="⚙️ 2. Sortierkriterien wählen", padx=10, pady=10)
        criteria_frame.pack(padx=10, pady=10, fill="x")
        
        # Checkbox: Sortieren nach Endung (z.B. JPG, PDF)
        tk.Checkbutton(criteria_frame, 
                       text="Nach Dateiendung sortieren (Ordnernamen in Großbuchstaben)", 
                       variable=self.sort_by_extension).pack(anchor="w")
        
        # Checkbox: Sortieren nach Datum
        tk.Checkbutton(criteria_frame, 
                       text="Nach Erstellungsdatum sortieren (erzeugt Unterordner)", 
                       variable=self.sort_by_date, 
                       command=self.toggle_date_options).pack(anchor="w", pady=(5, 0))

        # Datum-Granularität (Unteroptionen)
        self.date_options_frame = tk.Frame(criteria_frame, padx=20)
        
        tk.Label(self.date_options_frame, text="Datum-Detailgrad:").pack(side=tk.LEFT)
        
        granularity = [("Jahr (2025)", "Year"), ("Jahr/Monat (2025-11)", "Month"), ("Jahr/Monat/Tag (2025-11-15)", "Day")]
        for text, value in granularity:
            tk.Radiobutton(self.date_options_frame, 
                           text=text, 
                           variable=self.date_granularity, 
                           value=value).pack(side=tk.LEFT, padx=5)

        # Start-Button
        tk.Frame(tab, height=1, bg="gray").pack(fill="x", padx=10, pady=5)
        
        tk.Button(tab, 
                  text="🚀 Sortierung starten!", 
                  command=self.start_sorting, 
                  bg="green", fg="white", 
                  font=('Arial', 12, 'bold')).pack(pady=10)

        self.toggle_date_options() # Initial die Datums-Optionen ausblenden


    def setup_system_tab(self, tab):
        """Erstellt die Widgets für den System-Wartung Tab (NEU)."""
        
        # --- 1. Temp-Dateien Bereinigung ---
        temp_frame = tk.LabelFrame(tab, text="🧹 Temporäre Dateien bereinigen", padx=10, pady=10)
        temp_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(temp_frame, 
                 text="Analysiere und lösche temporäre Dateien, um Speicherplatz freizugeben.",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 10))
                 
        # Label für Analyse-Ergebnis (wird in self.cleanup_result_label gespeichert)
        self.cleanup_result_label = tk.Label(temp_frame, text="Status: Bereit zur Analyse.", fg="blue")
        self.cleanup_result_label.pack(anchor="w", pady=(5, 10))
        
        # Button zur Analyse und Bereinigung
        tk.Button(temp_frame, 
                  text="🔍 Analyse & Bereinigung starten", 
                  command=lambda: self.run_temp_cleaner(is_cleanup=False),
                  bg="#4A90E2", fg="white").pack(anchor="w", pady=(5, 0))
        
        # --- 2. Winget Upgrade ---
        winget_frame = tk.LabelFrame(tab, text="⬆️ Software-Updates (Winget)", padx=10, pady=10)
        winget_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(winget_frame, 
                 text="Führt 'winget upgrade --all' aus. Aktualisiert alle installierten Programme.\n(Kann Administratorrechte erfordern!)",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 10))
                 
        tk.Button(winget_frame, 
                  text="🚀 Winget Upgrade starten", 
                  command=self.run_winget_upgrade,
                  bg="#27AE60", fg="white").pack(anchor="w", pady=(5, 0))


    # --- Methoden für die Dateisortierung (Core) ---

    def browse_directory(self):
        """Öffnet einen Dialog zur Auswahl des Quellverzeichnisses."""
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir.set(directory)

    def toggle_date_options(self):
        """Zeigt oder versteckt die Datum-Granularitäts-Optionen."""
        if self.sort_by_date.get():
            self.date_options_frame.pack(anchor="w")
        else:
            self.date_options_frame.pack_forget()

    def start_sorting(self):
        """Überprüft die Eingaben und startet den Sortiervorgang."""
        source = self.source_dir.get()
        sort_ext = self.sort_by_extension.get()
        sort_date = self.sort_by_date.get()

        if not source or not os.path.isdir(source):
            messagebox.showerror("Fehler", "Bitte einen gültigen Quellordner auswählen.")
            return

        if not sort_ext and not sort_date:
            messagebox.showerror("Fehler", "Bitte mindestens ein Sortierkriterium (Dateiendung oder Datum) auswählen.")
            return

        confirm = messagebox.askyesno(
            "Achtung", 
            f"Soll die Sortierung im Ordner\n'{source}'\njetzt gestartet werden? \nDateien werden VERSCHOBEN."
        )
        
        if confirm:
            try:
                moved_count = self.process_files(source, sort_ext, sort_date, self.date_granularity.get())
                messagebox.showinfo("Erfolg", f"✅ Sortierung abgeschlossen! \n{moved_count} Dateien wurden verschoben.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def get_creation_date_info(self, file_path, granularity):
        """
        Gibt den Zeitstempel (Erstellungsdatum) der Datei zurück, 
        formatiert nach der gewählten Granularität (Year, Month, Day).
        """
        try:
            timestamp = os.path.getctime(file_path) 
            dt_object = datetime.fromtimestamp(timestamp)
        except OSError:
            return "UnknownDate"

        if granularity == "Year":
            return dt_object.strftime("%Y")
        elif granularity == "Month":
            return dt_object.strftime("%Y-%m")
        elif granularity == "Day":
            return dt_object.strftime("%Y-%m-%d")
        
        return "UnknownDate"

    def process_files(self, source_dir, sort_ext, sort_date, granularity):
        """
        Iteriert über alle Dateien, bestimmt den Zielpfad und verschiebt die Dateien.
        """
        moved_files_count = 0
        
        for item_name in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item_name)

            if os.path.isdir(source_path) or os.path.islink(source_path) or item_name == os.path.basename(__file__):
                continue

            target_folder_parts = []
            
            # A) Datum als oberste Hierarchieebene
            if sort_date:
                date_str = self.get_creation_date_info(source_path, granularity)
                target_folder_parts.append(date_str)
                
            # B) Dateiendung als Unterordner
            if sort_ext:
                extension = os.path.splitext(item_name)[1].lower().lstrip('.')
                if not extension:
                    extension = "NO_EXTENSION"
                
                target_folder_parts.append(extension.upper())

            if not target_folder_parts:
                continue 

            target_dir = os.path.join(source_dir, *target_folder_parts)
            
            # Zielordner erstellen
            os.makedirs(target_dir, exist_ok=True) 

            # Datei verschieben (inkl. Konfliktbehandlung)
            destination_path = os.path.join(target_dir, item_name)
            
            if os.path.exists(destination_path):
                base, ext = os.path.splitext(item_name)
                i = 1
                while os.path.exists(os.path.join(target_dir, f"{base}({i}){ext}")):
                    i += 1
                new_item_name = f"{base}({i}){ext}"
                destination_path = os.path.join(target_dir, new_item_name)

            shutil.move(source_path, destination_path)
            moved_files_count += 1
            
        return moved_files_count

    # --- Methoden für die System-Wartung (NEU) ---

    def run_winget_upgrade(self):
        """Führt das Winget-Upgrade für alle installierten Pakete aus."""
        # Sicherheitsfrage, da Admin-Rechte nötig sein können
        if not messagebox.askyesno("Upgrade bestätigen", "Soll Winget alle installierten Programme aktualisieren? Dies kann Administratorrechte erfordern."):
            return

        try:
            # Der Befehl, der alle Winget-Pakete aktualisiert
            result = subprocess.run(
                ["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements"],
                capture_output=True,
                text=True,
                check=True,
                shell=True
            )

            messagebox.showinfo("Winget Upgrade", f"Upgrade-Vorgang abgeschlossen! Details:\n{result.stdout[:500]}...")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Winget Fehler", f"Fehler bei winget:\n{e.stderr[:500]}...\nVersuchen Sie, das Tool als Administrator auszuführen.")

        except FileNotFoundError:
            messagebox.showerror("Winget Fehler", "Der Befehl 'winget' (Windows Package Manager) wurde nicht gefunden.")

    def clean_temp_files(self, dry_run=True):
        """
        Sucht temporäre Dateien in bekannten Verzeichnissen und meldet die Funde.
        Bei dry_run=False wird gelöscht.
        """
        temp_dirs = [
            os.environ.get('TEMP'),             # Lokale Benutzer-Temp-Dateien
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp') # System-Temp
        ]

        deleted_count = 0
        deleted_size = 0

        for temp_dir in temp_dirs:
            if not temp_dir or not os.path.exists(temp_dir):
                continue

            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)

                try:
                    if os.path.isfile(item_path):
                        item_size = os.path.getsize(item_path)
                        if not dry_run:
                            os.remove(item_path)
                            deleted_count += 1
                            deleted_size += item_size

                    elif os.path.isdir(item_path):
                        # Lösche leere Ordner oder rekursiv nicht-leere
                        if not os.listdir(item_path) and not dry_run:
                            os.rmdir(item_path)
                        elif not dry_run:
                            shutil.rmtree(item_path)

                except PermissionError:
                    continue
                except OSError:
                    continue
        
        size_mb = deleted_size / (1024 * 1024) if deleted_size > 0 else 0

        if dry_run:
            return f"🔍 Analyse abgeschlossen: {deleted_count} Elemente ({size_mb:.2f} MB) gefunden. Bereit zum Löschen."
        else:
            return f"✅ Bereinigung abgeschlossen: {deleted_count} Elemente ({size_mb:.2f} MB) gelöscht."

    def run_temp_cleaner(self, is_cleanup=False):
        """Startet die Analyse oder die eigentliche Bereinigung und fragt den Benutzer."""
        result = self.clean_temp_files(dry_run=not is_cleanup)
        
        if is_cleanup:
            # Nach der eigentlichen Bereinigung
            messagebox.showinfo("Bereinigung", result)
        else:
            # Nach der Analyse (dry-run)
            self.cleanup_result_label.config(text=result)
            
            if "0 Elemente" not in result:
                 if messagebox.askyesno("Bereinigung starten?", 
                                        f"Sollen die gefundenen Dateien jetzt endgültig gelöscht werden?\n{result}"):
                    # Starte die echte Bereinigung
                    self.run_temp_cleaner(is_cleanup=True)
            else:
                messagebox.showinfo("Bereinigung", "Keine temporären Dateien gefunden, die gelöscht werden müssen.")


# --- App starten ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()