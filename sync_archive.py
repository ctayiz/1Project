import os
import shutil
from datetime import datetime

def sync_folders(source, destination, log_file):
    try:
        with open(log_file, 'a') as log:
            log.write(f"=============\nSynchronisierung gestartet am {datetime.now()}\n")
            for root, dirs, files in os.walk(source):
                relative_path = os.path.relpath(root, source)
                destination_path = os.path.join(destination, relative_path)

                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)

                for file in files:
                    source_file = os.path.join(root, file)
                    dest_file = os.path.join(destination_path, file)

                    if os.path.exists(dest_file):
                        if os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                            shutil.copy2(source_file, destination_path)
                            log.write(f"Kopiere {file}\n")
                    else:
                        shutil.copy2(source_file, destination_path)
                        log.write(f"Kopiere {file}\n")

            log.write(f"Synchronisierung abgeschlossen {datetime.now()}\n")
        print("Ordner erfolgreich synchronisiert. Logdatei erstellt.")
    except Exception as e:
        print(f"Fehler beim Synchronisieren der Ordner: {e}")

