# sysdoc_core.py

import os
import math
import shutil # Für das Löschen ganzer Verzeichnisse

def format_bytes(size_bytes):
    """Formatiert eine Byte-Zahl in eine lesbare Größe (KB, MB, GB)."""
    if size_bytes == 0:
        return "0 Bytes"
    
    # Basen für die Umrechnung (1024)
    i = int(math.floor(math.log(size_bytes, 1024)))
    # Einheiten: Bytes, KB, MB, GB, TB, PB
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    
    return f"{s} {units[i]}"

def get_dir_size(path):
    """Berechnet rekursiv die Gesamtgröße aller Dateien in einem Verzeichnis (in Bytes)."""
    total_size = 0
    if not os.path.exists(path):
        return total_size
        
    for dirpath, dirnames, filenames in os.walk(path, followlinks=False):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Fehlerbehandlung für unzugängliche Dateien/Pfade (z.B. Berechtigungen)
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                continue
    return total_size

def run_analysis(gui_instance):
    """
    Führt die Berechnung der Junk-Dateien durch und meldet das Ergebnis an die GUI.
    """
    
    # Junk-Pfade definieren (Windows-spezifisch)
    junk_paths = [
        # %TEMP% Verzeichnis des Benutzers
        os.path.join(os.environ.get('TEMP', 'C:\\Temp')),
        # Windows Temp-Ordner (erfordert oft Admin-Rechte)
        "C:\\Windows\\Temp",
        # Pre-fetch Ordner
        "C:\\Windows\\Prefetch"
    ]
    
    total_junk_size = 0
    
    for path in junk_paths:
        size = get_dir_size(path)
        total_junk_size += size
            
    # Ergebnis anzeigen (muss im Haupt-GUI-Thread passieren!)
    gui_instance.master.after(0, lambda: gui_instance.display_analysis_results(total_junk_size))


def execute_system_cleanup(gui_instance):
    """
    Führt die eigentliche Löschung von Junk-Dateien und Ordnern durch.
    """
    
    junk_paths = [
        os.path.join(os.environ.get('TEMP', 'C:\\Temp')),
        "C:\\Windows\\Temp",
        "C:\\Windows\\Prefetch"
    ]
    
    deleted_count = 0
    total_freed_size = 0
    
    for path in junk_paths:
        if os.path.exists(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                try:
                    # Versuche, die Größe zu berechnen, bevor wir löschen
                    item_size = get_dir_size(item_path) if os.path.isdir(item_path) else os.path.getsize(item_path)
                    
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        total_freed_size += item_size
                        deleted_count += 1
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        total_freed_size += item_size
                        deleted_count += 1
                        
                except PermissionError:
                    # Ignoriere Dateien, die in Benutzung sind
                    print(f"Zugriff verweigert oder Datei in Benutzung: {item_path}")
                except Exception as e:
                    print(f"Fehler beim Löschen von {item_path}: {e}")

    # Ergebnis an die GUI zurückmelden
    gui_instance.master.after(0, lambda: gui_instance.display_cleanup_success(deleted_count, total_freed_size))