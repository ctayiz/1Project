import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import shutil
import os
from sync_archive import *

# config.xml einlesen
tree = ET.parse("config.xml")
config = tree.getroot()

# source = config.find("source").text
servername = config[0][0].text
source = config[1][0][0].text
dest = config[1][0][1].text
username = config[1][0][2].text
password = config[1][0][3].text

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

# widgets
label_servername = tk.Label(root, text="Servername:")
label_var_severname = tk.Label(root, text=servername)
label_source = tk.Label(root, text="Source:")
label_var_source = tk.Label(root, text=source)
label_dest = tk.Label(root, text="Destination:")
label_var_dest = tk.Label(root, text=dest)
btn_copy = ttk.Button(root, text="Go copy", command=lambda:sync_folders(source_path, destination_path))
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

