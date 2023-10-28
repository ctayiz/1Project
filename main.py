import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import shutil
import os

# config.xml einlesen
tree = ET.parse("config.xml")
config = tree.getroot()

# source = config.find("source").text
servername = config[0][0].text
source = config[1][0][0][0].text
dest = config[1][0][0][1].text



def info_box():
   tk.messagebox.showinfo(title="Info", message="Dieses Tool wurde von Cihan Tayiz programmiert. Es werden keinerlei Haftungen für die Auswirkungen übernommen.")

def print_entry_input():
    print(entry1.get())

def copy_archive(source, dest):
    # Überprüfe, ob das Zielverzeichnis existiert, falls nicht, erstelle es
    if not os.path.exists(dest):
        os.makedirs(dest)

    # Durchsuche die Quellordnerstruktur nach Dateien
    for root, _, files in os.walk(source):
        for file in files:
            quelle_dateipfad = os.path.join(root, file)
            ziel_dateipfad = os.path.join(dest, os.path.relpath(quelle_dateipfad, source))

            # Überprüfe, ob die Datei im Zielordner existiert, andernfalls kopiere sie
            if not os.path.exists(ziel_dateipfad):
                shutil.copy(quelle_dateipfad, ziel_dateipfad)
                print(f"Kopiere {quelle_dateipfad} nach {ziel_dateipfad}")

    # copy_archive(quelle_verzeichnis, ziel_verzeichnis)

root = tk.Tk()
root.title("CCW MigrationsTool")
# set windowsize
root.geometry("400x400")
root.minsize(width=400, height=400)
root.maxsize(width=600, height=600)


label1 = tk.Label(root, text="MigrationsTool")
label1.pack()

label_servername = tk.Label(root, text="Servername: " + servername)
label_servername.pack()

label_source = tk.Label(root, text="Source: " + source)
label_source.pack()

label_dest = tk.Label(root, text="Destination: " + dest)
label_dest.pack()

btn_copy = tk.Button(root, text="Go copy", command=copy_archive *arg: copy_archive(quelle_verzeichnis, ziel_verzeichnis))
btn_copy.pack()

btn_destroy = ttk.Button (root, text="Cancel", command=root.destroy)
btn_destroy.pack(side="bottom")

btn_info = ttk.Button (root, text="Info", padding=10, command=info_box)
btn_info.pack(side="bottom")

root.mainloop()

