import os
import shutil

def sync_folders(source, destination):
    try:
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            destination_path = os.path.join(destination, relative_path)

            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(destination_path, file)

                if os.path.exists(dest_file):
                    # Überprüfe die Änderungszeit und kopiere, wenn die Quelldatei neuer ist
                    if os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                        shutil.copy2(source_file, destination_path)
                        print(f"Kopiere {file} von {source} nach {destination}")
                else:
                    shutil.copy2(source_file, destination_path)
                    print(f"Kopiere {file} von {source} nach {destination}")

        print("Ordner erfolgreich synchronisiert.")
    except Exception as e:
        print(f"Fehler beim Synchronisieren der Ordner: {e}")

# Beispielaufruf
source_path = 'test'
destination_path = 'test2'
