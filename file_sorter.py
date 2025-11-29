# file_sorter.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading 

# NEU: Importiere die Kernlogik
import sysdoc_core 

# --- 1. FARB- UND STYLING-KONSTANTEN ---
BG_COLOR = "#2C323D"    # Hintergrundfarbe
NAV_COLOR = "#292E36"   # Navigationsleisten-Hintergrund
BUTTON_ACTIVE = "#0078d4" # Aktiver Button-Hintergrund (Blau)
TEXT_COLOR = "#CCCCCC"  # Haupt-Textfarbe
CARD_COLOR = "#2B2F35"  # Karten-Hintergrund

class SystemOptimizerApp:
    def __init__(self, master):
        self.master = master
        master.title("SysDoc Tool")
        master.configure(bg=BG_COLOR)
        master.minsize(600, 400) # Mindestgröße

        # Aktuellen, ausgewählten Navigationspunkt speichern
        self.current_view = tk.StringVar(value="Systemreinigung") # Initialansicht geändert

        # --- 2. Styling-Anpassungen ---
        style = ttk.Style()
        style.theme_use('clam') 

        style.configure('Nav.TButton', 
                        font=('Segoe UI', 12, 'bold'),
                        background=NAV_COLOR,
                        foreground=TEXT_COLOR,
                        relief='flat',
                        padding=[15, 15])
        style.map('Nav.TButton',
                  background=[('active', "#912a2a")],
                  foreground=[('disabled', '#aaaaaa')])

        style.configure('Active.Nav.TButton',
                        background=BUTTON_ACTIVE,
                        foreground=CARD_COLOR)


        # --- 3. Haupt-Layout-Frames ---
        self.nav_frame = tk.Frame(master, width=200, bg=NAV_COLOR)
        self.nav_frame.pack(side="left", fill="y")
        
        self.content_frame = tk.Frame(master, bg=BG_COLOR, padx=30, pady=30)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # --- 4. Navigation (Linke Seitenleiste) ---
        self.create_nav_bar()

        # --- 5. Initialansicht anzeigen ---
        self.show_view("Systemreinigung")


    def create_nav_buttons(self, items):
        """Erstellt eine Reihe von Navigationsbuttons (Hilfsfunktion)."""
        for text, icon in items:
            # Wenn auf "Systemreinigung" geklickt wird, soll die Analyse starten
            if text == "Systemreinigung":
                command_func = self.action_system_cleanup
            else:
                command_func = lambda t=text: self.show_view(t)
                
            button = ttk.Button(self.nav_frame, 
                                text=f"{icon} {text}", 
                                style='Nav.TButton', 
                                command=command_func)
            button.pack(fill='x', pady=5, padx=10)


    def create_nav_bar(self):
        """Erstellt die Kopfzeile und die Navigationsbuttons in der linken Leiste."""
        
        # Kopfzeile (Symbol und Text)
        header_label = tk.Label(self.nav_frame, 
                                text="SysDoc Tool", 
                                font=('Segoe UI', 11, 'bold'), 
                                bg=NAV_COLOR, 
                                fg=TEXT_COLOR,
                                pady=10, padx=5) 
        header_label.pack(fill='x')
        
        tk.Frame(self.nav_frame, height=1, bg='#e0e0e0').pack(fill='x', padx=10, pady=5)

        # --- HAUPTFUNKTIONEN (Optimierung) ---
        tk.Label(self.nav_frame, text="OPTIMIERUNG", font=('Segoe UI', 9, 'bold'), 
                 bg=NAV_COLOR, fg="#888888", anchor='w', padx=20).pack(fill='x', pady=(10, 5))
                 
        nav_items_main = [
            ("Analyse", "🔎"), 
            ("Systemreinigung", "🗑️"),
            ("Driver upgrade", "💿"), 
            ("Software Upgrade", "🔄"),
            ("Deinstallieren der Apps", "❌")
        ]
        # KORRIGIERT: self.create_nav_buttons anstelle von self.create_nav.buttons
        self.create_nav_buttons(nav_items_main)


        # --- TRENNLINIE & DATEIMANAGEMENT ---
        tk.Frame(self.nav_frame, height=1, bg='#e0e0e0').pack(fill='x', padx=10, pady=10)
        
        tk.Label(self.nav_frame, text="DATEI-TOOLS", font=('Segoe UI', 9, 'bold'), 
                 bg=NAV_COLOR, fg="#888888", anchor='w', padx=20).pack(fill='x', pady=(0, 5))
                 
        nav_items_file = [
            ("Dateisuche und Sortierung", "🗂️")
        ]
        self.create_nav_buttons(nav_items_file)


        # --- TRENNLINIE & TOOL-VERWALTUNG ---
        spacer = tk.Frame(self.nav_frame, bg=NAV_COLOR)
        spacer.pack(fill='both', expand=True) 

        tk.Frame(self.nav_frame, height=1, bg='#e0e0e0').pack(side='bottom', fill='x', padx=10, pady=10)

        nav_items_admin = [
            ("Login/Register", "👤"),
            ("Kontakt", "📧"),
            ("Einstellungen", "⚙️")
        ]
        
        for text, icon in reversed(nav_items_admin):
            button = ttk.Button(self.nav_frame, 
                                text=f"{icon} {text}", 
                                style='Nav.TButton', 
                                command=lambda t=text: self.show_view(t))
            button.pack(side='bottom', fill='x', pady=5, padx=10)


    def show_view(self, view_name):
        """Aktualisiert den Inhalt des rechten Frames basierend auf der Auswahl in der Navigation."""
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.current_view.set(view_name)
        
        if view_name == "Systemreinigung" or view_name == "Analyse":
            # Startet die Analyse direkt, wenn man auf den Button klickt
            self.action_system_cleanup() 
        else:
            # Platzhalter für andere Ansichten
            tk.Label(self.content_frame, 
                     text=f"🏗️ Ansicht: {view_name} wird entwickelt...", 
                     font=('Segoe UI', 12, 'bold'), 
                     bg=BG_COLOR, 
                     fg=TEXT_COLOR).pack(pady=100)
            
        self.update_nav_button_styles()


    def update_nav_button_styles(self):
        """Stellt sicher, dass der aktuell ausgewählte Button blau hervorgehoben wird."""
        
        for widget in self.nav_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                # Prüfe nur Buttons, die auch in nav_items_main/file/admin definiert sind
                try:
                    button_text = widget.cget('text').split(' ', 1)[1] 
                except IndexError:
                    continue
                
                if button_text == self.current_view.get():
                    widget.configure(style='Active.Nav.TButton')
                else:
                    widget.configure(style='Nav.TButton')


    # --- KERN-LOGIK (AUFRUFE) ---

    def action_system_cleanup(self):
        """Startet die Systemanalyse in einem separaten Thread."""
        
        self.current_view.set("Systemreinigung") 
        self.update_nav_button_styles()
        
        self.show_analysis_view() 
        
        # Startet die Analyse im Core-Modul
        self.analysis_thread = threading.Thread(target=sysdoc_core.run_analysis, args=(self,))
        self.analysis_thread.start()

    
    def show_analysis_view(self):
        """Erstellt die Benutzeroberfläche für die laufende Analyse."""
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, 
                 text="Systemanalyse läuft...", 
                 font=('Segoe UI', 12, 'bold'), 
                 bg=BG_COLOR, 
                 fg=TEXT_COLOR).pack(pady=20)
        
        self.status_label = tk.Label(self.content_frame, 
                                     text="🔎 Scanne temporäre Dateien...", 
                                     font=('Segoe UI', 12), 
                                     bg=BG_COLOR, 
                                     fg="#666666")
        self.status_label.pack(pady=10)
        
        self.result_label = tk.Label(self.content_frame, 
                                     text="Berechnung läuft im Hintergrund...", 
                                     font=('Segoe UI', 14, 'italic'), 
                                     bg=BG_COLOR, 
                                     fg="#0078d4")
        self.result_label.pack(pady=50)


    def display_analysis_results(self, size_bytes):
        """Zeigt das Endergebnis der Analyse an."""
        
        formatted_size = sysdoc_core.format_bytes(size_bytes)
        
        self.status_label.configure(text="✅ Analyse abgeschlossen.")
        self.result_label.configure(text=f"Potenziell freizugebender Speicherplatz: \n\n {formatted_size}", 
                                    font=('Segoe UI', 14, 'bold'),
                                    fg="#28a745") 
        
        cleanup_button = ttk.Button(self.content_frame, 
                                    text=f"Jetzt {formatted_size} bereinigen", 
                                    style='Active.Nav.TButton', 
                                    command=lambda: self.execute_cleanup(size_bytes))
        cleanup_button.pack(pady=30)
        
        if size_bytes == 0:
            cleanup_button.configure(text="Nichts zu bereinigen gefunden!", state='disabled')


    def execute_cleanup(self, size_bytes):
        """Startet die tatsächliche Löschfunktion im Core-Modul in einem separaten Thread."""
        
        # UI-Feedback, dass die Löschung läuft
        self.result_label.configure(text=f"🗑️ Bereinigung läuft...", fg="#ffc107", font=('Segoe UI', 14, 'bold'))
        
        # Löschvorgang im Hintergrund-Thread starten
        cleanup_thread = threading.Thread(target=sysdoc_core.execute_system_cleanup, args=(self,))
        cleanup_thread.start()


    def display_cleanup_success(self, deleted_count, total_freed_size):
        """Zeigt das Endergebnis der erfolgreichen Bereinigung an."""
        
        formatted_size = sysdoc_core.format_bytes(total_freed_size)
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(self.content_frame, 
                 text="Bereinigung abgeschlossen!", 
                 font=('Segoe UI', 14, 'bold'), 
                 bg=BG_COLOR, 
                 fg="#28a745").pack(pady=40)
                 
        tk.Label(self.content_frame,
                 text=f"✅ {formatted_size} Speicherplatz freigegeben.\n"
                      f"({deleted_count} Dateien und Ordner gelöscht.)",
                 font=('Segoe UI', 14),
                 bg=BG_COLOR,
                 fg=TEXT_COLOR,
                 justify=tk.CENTER).pack(pady=20)


    # --- Platzhalter für andere Funktionen (Diese brauchen noch Implementierung) ---

    def action_clear_browser(self):
        messagebox.showinfo("Browserverlauf", "Platzhalter: Browserdaten werden gelöscht.")

    def action_clean_registry(self):
        messagebox.showwarning("Registry", "Platzhalter: Registry wird bereinigt.")
        
    def action_update_software(self):
        messagebox.showinfo("Software", "Platzhalter: Software wird aktualisiert.")
        
    def action_analyse(self):
         messagebox.showinfo("Analyse", "Platzhalter: Detaillierte Systemanalyse.")


# --- 7. Hauptausführung des Programms ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemOptimizerApp(root)
    root.mainloop()