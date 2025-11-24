import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from datetime import datetime
import subprocess
import hashlib
import winreg # NEU: Für den Zugriff auf die Windows Registry

class FileSorterApp:
    def __init__(self, master):
        self.master = master
        master.title("🖼️ System- & Datei-Optimierer")
        
        # --- Variablen für Sortierung ---
        self.source_dir = tk.StringVar(value="")
        self.sort_by_extension = tk.BooleanVar(value=True) 
        self.sort_by_date = tk.BooleanVar(value=False)
        self.date_granularity = tk.StringVar(value="Year")
        
        # Variablen für GUI-Elemente (werden in setup_widgets initialisiert)
        self.cleanup_result_label = None 
        self.status_label = None
        self.progress_bar = None
        
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

        self.toggle_date_options()
        
        # --- Fortschrittsanzeige ---
        progress_frame = tk.LabelFrame(tab, text="✅ Sortierungsstatus", padx=10, pady=10)
        progress_frame.pack(padx=10, pady=10, fill="x")

        self.status_label = tk.Label(progress_frame, text="Warte auf Start...", anchor="w")
        self.status_label.pack(fill="x", pady=(0, 5))

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate", length=400)
        self.progress_bar.pack(fill="x")
        # ----------------------------------------


    def setup_system_tab(self, tab):
        """Erstellt die Widgets für den System-Wartung Tab."""
        
        # --- 1. Temp-Dateien Bereinigung ---
        temp_frame = tk.LabelFrame(tab, text="🧹 Temporäre Dateien bereinigen", padx=10, pady=10)
        temp_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(temp_frame, 
                 text="Analysiere und lösche temporäre Dateien, um Speicherplatz freizugeben.",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 10))
                 
        self.cleanup_result_label = tk.Label(temp_frame, text="Status: Bereit zur Analyse.", fg="blue")
        self.cleanup_result_label.pack(anchor="w", pady=(5, 10))
        
        tk.Button(temp_frame, 
                  text="🔍 Analyse & Bereinigung starten", 
                  command=lambda: self.run_temp_cleaner(is_cleanup=False),
                  bg="#4A90E2", fg="white").pack(anchor="w", pady=(5, 0))
        
        # --- 2. Winget Upgrade ---
        winget_frame = tk.LabelFrame(tab, text="⬆️ Software-Updates (Winget)", padx=10, pady=10)
        winget_frame.pack(padx=10, fill="x", pady=(10, 0))
        
        tk.Label(winget_frame, 
                 text="Führt 'winget upgrade --all' aus. Aktualisiert alle installierten Programme.\n(Kann Administratorrechte erfordern!)",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 10))
                 
        tk.Button(winget_frame, 
                  text="🚀 Winget Upgrade starten", 
                  command=self.run_winget_upgrade,
                  bg="#27AE60", fg="white").pack(anchor="w", pady=(5, 0))
                  
        # --- 3. Duplikatssuche ---
        duplicate_frame = tk.LabelFrame(tab, text="🔍 Doppelte Dateien finden", padx=10, pady=10)
        duplicate_frame.pack(padx=10, fill="x", pady=(10, 0))

        tk.Label(duplicate_frame, 
                 text="Sucht im gewählten Ordner nach identischen Inhalten (SHA256 Hash).",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 5))
                 
        tk.Button(duplicate_frame, 
                  text="▶️ Duplikatssuche starten", 
                  command=self.start_duplicate_search, 
                  bg="#FFC300").pack(anchor="w", pady=(5, 0))

        # --- 4. Ungültige Verknüpfungen ---
        shortcut_frame = tk.LabelFrame(tab, text="🔗 Ungültige Verknüpfungen finden", padx=10, pady=10)
        shortcut_frame.pack(padx=10, fill="x", pady=(10, 0))

        tk.Label(shortcut_frame, 
                 text="Sucht nach kaputten '.lnk'-Dateien, deren Ziel nicht mehr existiert.",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 5))
                 
        tk.Button(shortcut_frame, 
                  text="▶️ Suche starten & bereinigen", 
                  command=self.find_invalid_shortcuts, 
                  bg="#FF8C00", fg="white").pack(anchor="w", pady=(5, 0))
                  
        # --- 5. Autostart-Verwaltung (NEU) ---
        autostart_frame = tk.LabelFrame(tab, text="⏱️ Autostart-Programme", padx=10, pady=10)
        autostart_frame.pack(padx=10, fill="x", pady=(10, 0))

        tk.Label(autostart_frame, 
                 text="Listet Programme auf, die beim Start geladen werden, und öffnet den Task Manager zur Deaktivierung.",
                 justify=tk.LEFT).pack(anchor="w", pady=(0, 5))
                 
        tk.Button(autostart_frame, 
                  text="▶️ Autostart prüfen & verwalten", 
                  command=self.manage_autostart, 
                  bg="#FF3333", fg="white").pack(anchor="w", pady=(5, 0))


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

        # VOR dem Start den Fortschritt zurücksetzen
        self.progress_bar["value"] = 0
        self.status_label.config(text="Vorbereitung...")
        self.master.update()
        
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

            # Nach Abschluss den Status auf Endzustand setzen
            self.status_label.config(text="Sortierung abgeschlossen.")
            self.progress_bar["value"] = self.progress_bar["maximum"] if self.progress_bar["maximum"] > 0 else 0
            self.master.update()


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
        Iteriert über alle Dateien, bestimmt den Zielpfad, verschiebt die Dateien 
        und aktualisiert den Fortschrittsbalken.
        """
        # 1. Alle zu verarbeitenden Dateien im Voraus zählen
        all_items = os.listdir(source_dir)
        files_to_process = [
            item for item in all_items 
            if not os.path.isdir(os.path.join(source_dir, item)) and 
               not os.path.islink(os.path.join(source_dir, item)) and
               item != os.path.basename(__file__)
        ]
        total_files = len(files_to_process)
        
        if total_files == 0:
            return 0 # Nichts zu tun

        # Progress Bar einrichten
        self.progress_bar["maximum"] = total_files
        self.progress_bar["value"] = 0
        self.status_label.config(text=f"Starte Sortierung von {total_files} Dateien...")
        self.master.update()

        moved_files_count = 0
        
        for index, item_name in enumerate(files_to_process):
            source_path = os.path.join(source_dir, item_name)

            # --- Fortschritt aktualisieren (Feedback) ---
            self.status_label.config(text=f"Verarbeite Datei {index + 1}/{total_files}: {item_name}")
            self.progress_bar["value"] = index + 1
            self.master.update() # Wichtig: Aktualisiert die GUI sofort
            # -------------------------------------------

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
        
    # --- Methoden für die Duplikatssuche ---
    
    def hash_file(self, filepath):
        """Berechnet den SHA256-Hash einer Datei, blockweise für große Dateien."""
        BLOCKSIZE = 65536 # 64 KB
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            return hasher.hexdigest()
        except Exception:
            return None

    def find_duplicates(self, source_dir):
        """Durchsucht den Ordner nach Dateien mit identischem Inhalt."""
        
        if not os.path.isdir(source_dir):
            return "Fehler: Ungültiger Pfad."
            
        hashes = {}
        duplicates_found = 0
        
        # Gehe rekursiv durch alle Ordner
        for dirpath, dirnames, filenames in os.walk(source_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                
                if os.path.islink(filepath) or filename == os.path.basename(__file__):
                    continue
                
                file_hash = self.hash_file(filepath)
                
                if file_hash:
                    if file_hash in hashes:
                        hashes[file_hash].append(filepath)
                        duplicates_found += 1
                    else:
                        hashes[file_hash] = [filepath]

        duplicate_sets = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        
        if not duplicate_sets:
            return "Keine doppelten Dateien gefunden."

        message = f"✅ {duplicates_found} Duplikate in {len(duplicate_sets)} Sets gefunden.\n\n"
        
        # Ausgabe der ersten 5 Duplikat-Sets
        i = 0
        for h, paths in duplicate_sets.items():
            if i >= 5:
                message += f"\n... und {len(duplicate_sets) - 5} weitere Sets."
                break
            message += f"Set {i+1} ({len(paths)} Duplikate):\n"
            for p in paths[1:]: 
                message += f"  - {p}\n"
            i += 1
             
        return message

    def start_duplicate_search(self):
        """Startet die Duplikatssuche und zeigt das Ergebnis an."""
        source = filedialog.askdirectory(title="Ordner für Duplikatssuche wählen")
        
        if source:
            messagebox.showinfo("Duplikatssuche gestartet", f"Suche nach Duplikaten in: {source}. Dies kann bei großen Ordnern dauern.")
            
            result_message = self.find_duplicates(source)
            
            messagebox.showinfo("Duplikatsergebnisse", result_message)
        else:
            messagebox.showwarning("Abgebrochen", "Duplikatssuche wurde abgebrochen.")

    # --- Methoden für die System-Wartung ---

    def run_winget_upgrade(self):
        """Führt das Winget-Upgrade für alle installierten Pakete aus."""
        if not messagebox.askyesno("Upgrade bestätigen", "Soll Winget alle installierten Programme aktualisieren? Dies kann Administratorrechte erfordern."):
            return

        try:
            result = subprocess.run(
                ["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements"],
                capture_output=True,
                text=True,
                check=True,
                shell=True,
                encoding="utf-8"
            )

            messagebox.showinfo("Winget Upgrade", f"Upgrade-Vorgang abgeschlossen! Details:\n{result.stdout[:500]}...")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Winget Fehler", f"Fehler bei winget:\n{e.stderr[:500]}...\nVersuchen Sie, das Tool als Administrator auszuführen.")

        except FileNotFoundError:
            messagebox.showerror("Winget Fehler", "Der Befehl 'winget' (Windows Package Manager) wurde nicht gefunden.")
        except UnicodeDecodeError:
            messagebox.showerror("Kodierungsfehler", "Fehler beim Lesen der Winget-Ausgabe.")


    def clean_temp_files(self, dry_run=True):
        """
        Sucht temporäre Dateien in bekannten Verzeichnissen und meldet die Funde.
        """
        temp_dirs = [
            os.environ.get('TEMP'), 
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
            messagebox.showinfo("Bereinigung", result)
        else:
            self.cleanup_result_label.config(text=result)
            
            if "0 Elemente" not in result:
                 if messagebox.askyesno("Bereinigung starten?", 
                                        f"Sollen die gefundenen Dateien jetzt endgültig gelöscht werden?\n{result}"):
                    self.run_temp_cleaner(is_cleanup=True)
            else:
                messagebox.showinfo("Bereinigung", "Keine temporären Dateien gefunden, die gelöscht werden müssen.")

    def find_invalid_shortcuts(self):
        """
        Sucht rekursiv nach ungültigen .lnk-Dateien, indem PowerShell 
        verwendet wird, um deren Zielpfade zu prüfen.
        """
        source_dir = filedialog.askdirectory(title="Ordner für die Suche nach ungültigen Verknüpfungen wählen")
        if not source_dir:
            return

        invalid_shortcuts = []
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith('.lnk'):
                    filepath = os.path.join(root, file)
                    
                    powershell_command = (
                        f"powershell -ExecutionPolicy Bypass -Command \"$link = Get-Item -LiteralPath '{filepath}' -ErrorAction SilentlyContinue; "
                        f"if ($link.Target -eq $null) {{ Write-Host 'INVALID' }} else {{ Write-Host 'VALID' }}\""
                    )
                    
                    try:
                        result = subprocess.run(
                            powershell_command, 
                            capture_output=True, 
                            text=True, 
                            check=True, 
                            encoding="utf-8"
                        )
                        
                        if 'INVALID' in result.stdout.strip().upper():
                            invalid_shortcuts.append(filepath)
                            
                    except Exception as e:
                        print(f"Fehler bei Verknüpfung {filepath}: {e}")
                        continue
        
        if not invalid_shortcuts:
            messagebox.showinfo("Ergebnis", "Keine ungültigen Verknüpfungen gefunden.")
            return

        message = f"✅ {len(invalid_shortcuts)} ungültige Verknüpfungen gefunden:\n\n"
        
        message += "\n".join(invalid_shortcuts[:10])
        if len(invalid_shortcuts) > 10:
             message += f"\n... und {len(invalid_shortcuts) - 10} weitere."

        messagebox.showinfo("Ungültige Verknüpfungen", message)
        
        if messagebox.askyesno("Löschen bestätigen", f"Sollen {len(invalid_shortcuts)} ungültige Verknüpfungen jetzt gelöscht werden?"):
            deleted_count = 0
            for shortcut in invalid_shortcuts:
                try:
                    os.remove(shortcut)
                    deleted_count += 1
                except Exception:
                    continue
            messagebox.showinfo("Löschung abgeschlossen", f"Es wurden {deleted_count} ungültige Verknüpfungen gelöscht.")

    # --- NEUE FUNKTION: Autostart-Verwaltung ---

    def get_autostart_entries(self):
        """Liest Autostart-Einträge aus HKLM und HKCU."""
        entries = []
        
        # 1. Benutzer-spezifische Einträge (HKEY_CURRENT_USER)
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                     r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                     0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, type = winreg.EnumValue(reg_key, i)
                    entries.append({'name': name, 'path': value, 'key': 'HKCU'})
                    i += 1
                except OSError:
                    break # Ende der Liste
            winreg.CloseKey(reg_key)
        except Exception:
            pass
            
        # 2. Systemweite Einträge (HKEY_LOCAL_MACHINE)
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                     r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                     0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, type = winreg.EnumValue(reg_key, i)
                    entries.append({'name': name, 'path': value, 'key': 'HKLM'})
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(reg_key)
        except Exception:
            pass
            
        return entries
        
    def manage_autostart(self):
        """Öffnet ein neues Fenster zur Verwaltung der Autostart-Programme."""
        autostart_entries = self.get_autostart_entries()
        
        if not autostart_entries:
            messagebox.showinfo("Autostart", "Keine konfigurierbaren Autostart-Einträge in der Registry gefunden.")
            return

        # Zeige die Einträge in einer Meldung an
        entry_list = "\n".join([f"[{e['key']}] {e['name']}" for e in autostart_entries[:10]]) # Zeige nur die ersten 10
        
        message = f"Gefundene Autostart-Einträge ({len(autostart_entries)} insgesamt):\n\n"
        message += entry_list
        if len(autostart_entries) > 10:
             message += f"\n... und {len(autostart_entries) - 10} weitere."
        
        messagebox.showinfo("Autostart-Einträge", message)
        
        # Biete an, den Task Manager zu öffnen
        if not messagebox.askyesno("Autostart verwalten", "Möchtest du nun die Windows-Einstellungen (Task Manager) öffnen, um die Programme manuell zu deaktivieren?"):
            return
            
        # Öffne Task Manager > Autostart (Funktioniert ab Win 8)
        subprocess.run(["taskmgr", "/0 /startup"], check=False)


# --- App starten ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()