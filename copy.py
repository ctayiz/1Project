import os
import shutil
import tkinter as tk
from tkinter import filedialog

def kopiere_neue_dateien(quelle, ziel):
    if not os.path.exists(ziel):
        os.makedirs(ziel)

    for root, _, files in os.walk(quelle):
        for file in files:
            quelle_dateipfad = os.path.join(root, file)
            ziel_dateipfad = os.path.join(ziel, os.path.relpath(quelle_dateipfad, quelle))

            if not os.path.exists(ziel_dateipfad):
                shutil.copy(quelle_dateipfad, ziel_dateipfad)
                print(f"Kopiere {quelle_dateipfad} nach {ziel_dateipfad}")

def choose_source_directory():
    quelle_verzeichnis = filedialog.askdirectory()
    quelle_entry.delete(0, tk.END)
    quelle_entry.insert(0, quelle_verzeichnis)

def choose_destination_directory():
    ziel_verzeichnis = filedialog.askdirectory()
    ziel_entry.delete(0, tk.END)
    ziel_entry.insert(0, ziel_verzeichnis)

def start_copy():
    quelle = quelle_entry.get()
    ziel = ziel_entry.get()
    kopiere_neue_dateien(quelle, ziel)

# GUI erstellen
root = tk.Tk()
root.title("Dateien kopieren")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Quellverzeichnis:").grid(row=0, column=0)
quelle_entry = tk.Entry(frame, width=50)
quelle_entry.grid(row=0, column=1)
quelle_button = tk.Button(frame, text="Auswählen", command=choose_source_directory)
quelle_button.grid(row=0, column=2)

tk.Label(frame, text="Zielverzeichnis:").grid(row=1, column=0)
ziel_entry = tk.Entry(frame, width=50)
ziel_entry.grid(row=1, column=1)
ziel_button = tk.Button(frame, text="Auswählen", command=choose_destination_directory)
ziel_button.grid(row=1, column=2)

start_button = tk.Button(frame, text="Start", command=start_copy)
start_button.grid(row=2, column=1)

root.mainloop()
