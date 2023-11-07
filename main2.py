import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import shutil
import os
from sync_archive import *
import psutil
import time
import subprocess

'''
def monitor():
    while True:
        service = psutil.win_service_get('Spooler')
        status = service.status()
        label_var_service = tk.Label(root, text=status + "1123")
        label_var_service.place(x=130, y=80)
        print(status)
        time.sleep(5)
     #   return status
'''
   
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

'''
# Ausgabe der extrahierten Werte
print(f"Source: {source}")
print(f"Destination: {dest}")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Logfile: {logfile}")
print(f"Servername: {servername}") '''

# functions
def info_box():
   tk.messagebox.showinfo(title="Info", message="Dieses Tool wurde von Cihan Tayiz programmiert. Es werden keinerlei Haftungen für die Auswirkungen übernommen.")

def copy_archive():
    shutil.copytree(source,dest)

def iis_reset():
    try:
        subprocess.call(["iisreset"], shell=True)
    except:
        print("Dienst konnte nicht neugestartet werden.")

# root window
root = tk.Tk()
root.title("CCW MigrationsTool")

# set windowsize
root.geometry("500x500")
root.minsize(width=400, height=400)
root.maxsize(width=600, height=600)

# define frames
frame1 = tk.Frame(root, border=10, bg="black")
frame1.grid(row=4, column=0)

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
label_service = tk.Label(root, text="Dienst Status: ")
btn_iis_reset = ttk.Button(root, text="IISRESET", command=lambda:iis_reset())


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
label_service.place(x=20, y=80)
btn_iis_reset.grid(row=2, column=0)


def get_service_status(service_name):
    service = psutil.win_service_get(service_name)
    return service.status()

def start_service():
    try:
        service = psutil.win_service_get("Spooler")
        subprocess.Popen(["net", "start", "Spooler"], shell=True)
        status_label.config(text="Dienst gestartet")
    except psutil.AccessDenied:
        status_label.config(text="Zugriff verweigert: Benötigt Administratorrechte")
    except Exception as e:
        status_label.config(text=f"Fehler beim Starten des Dienstes: {e}")

def stop_service():
    try:
        service = psutil.win_service_get("Spooler")
        subprocess.call(["net", "stop", "Spooler"], shell=True)
        status_label.config(text="Dienst gestoppt")
    except psutil.AccessDenied:
        status_label.config(text="Zugriff verweigert: Benötigt Administratorrechte")
    except Exception as e:
        status_label.config(text=f"Fehler beim Stoppen des Dienstes: {e}")


def update_status():
    status = get_service_status("Spooler")
    status_label.config(text=f"{status}")
    root.after(5000, update_status)  # Aktualisierung alle 5 Sekunden

status_label = tk.Label(root, text="")
status_label.place(x=130, y=80)

start_button = ttk.Button(root, text="Start", command=start_service)
start_button.place(x=250, y=80)

stop_button = ttk.Button(root, text="Stop", command=stop_service)
stop_button.place(x=350, y=80)

update_status()  # Erste Statusaktualisierung starten


# run
root.mainloop()

