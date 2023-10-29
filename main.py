import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import shutil
import os
from sync_archive import *

# Pfad zur XML-Datei
file_path = 'config.xml'

# XML-Datei einlesen
tree = ET.parse(file_path)
root = tree.getroot()

# Parameter unter <copy_archive> extrahieren
copy_archive = root.find('tasks/copy_archive')
server = root.find('server')

source = copy_archive.find('source').text
dest = copy_archive.find('destination').text
username = copy_archive.find('username').text
password = copy_archive.find('password').text
logfile = copy_archive.find('logfile').text

servername = server.find('name').text

# Ausgabe der extrahierten Werte
print(f"Source: {source}")
print(f"Destination: {dest}")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Logfile: {logfile}")
print(f"Servername: {servername}")

# functions
def info_box():
   tk.messagebox.showinfo(title="Info", message="Dieses Tool wurde von Cihan Tayiz programmiert. Es werden keinerlei Haftungen für die Auswirkungen übernommen.")

def copy_archive():
    shutil.copytree(source,dest)

# root window
root = tk.Tk()
root.title("CCW MigrationsTool")

# set windowsize
root.geometry("400x400")
root.minsize(width=400, height=400)
root.maxsize(width=600, height=600)

# define a grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# set variable
source_path = source
destination_path = dest
log_file_path = logfile

# widgets
label_servername = tk.Label(root, text="Servername:")
label_var_severname = tk.Label(root, text=servername, border=1)
label_source = tk.Label(root, text="Source:")
label_var_source = tk.Label(root, text=source)
label_dest = tk.Label(root, text="Destination:")
label_var_dest = tk.Label(root, text=dest)
btn_copy = ttk.Button(root, text="START COPY", command=lambda:sync_folders(source_path, destination_path, log_file_path))
btn_destroy = ttk.Button (root, text="Cancel", command=root.destroy)
btn_info = ttk.Button (root, text="Info", command=info_box)

# place a widget
label_servername.place(x=20, y=20)
label_var_severname.place(x=130, y=20)
label_source.place(x=20, y=40)
label_var_source.place(x=130, y=40)
label_dest.place(x=20, y=60)
label_var_dest.place(x=130, y=60)
btn_copy.grid(row=3, column=0, sticky="nsew")
btn_destroy.grid(row=3, column=2, sticky="nsew")
btn_info.grid(row=3, column=1, sticky="nsew")

# run
root.mainloop()

