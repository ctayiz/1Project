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
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)


label_servername = tk.Label(root, text="Servername:")
label_servername.place(x=20, y=20)

label_var_severname = tk.Label(root, text=servername)
label_var_severname.place(x=130, y=20)

label_source = tk.Label(root, text="Source:")
label_source.place(x=20, y=40)

label_var_source = tk.Label(root, text=source)
label_var_source.place(x=130, y=40)

label_dest = tk.Label(root, text="Destination:")
label_dest.place(x=20, y=60)

label_var_dest = tk.Label(root, text=dest)
label_var_dest.place(x=130, y=60)

btn_copy = ttk.Button(root, text="Go copy")
btn_copy.grid(row=3, column=0, sticky="nsew")

btn_destroy = ttk.Button (root, text="Cancel", command=root.destroy)
btn_destroy.grid(row=3, column=2, sticky="nsew")

btn_info = ttk.Button (root, text="Info", command=info_box)
btn_info.grid(row=3, column=1, sticky="nsew")

root.mainloop()

