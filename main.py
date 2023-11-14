import tkinter as tk
import tkinter.messagebox as messagebox
from ttkbootstrap.constants import *
import ttkbootstrap  as tb
import socket
import psutil
import subprocess
import time
import threading
import os
import logging
import xml.etree.ElementTree as ET
import shutil
from sync_archive import *

root = tb.Window(themename="superhero")
root.title("CCW Tool by Cihan")
root.geometry("800x500")

frame = tb.Frame(root)
frame.grid(row=0, column=0)

frame_jobs = tb.Frame(root)
frame_jobs.grid(row=1, column=0)


# xml config 

# Pfad zur XML-Datei
file_path = 'config.xml'

# XML-Datei einlesen
tree = ET.parse(file_path)
rootxml = tree.getroot()

# Parameter unter <copy_archive> extrahieren
copy_archive = rootxml.find('tasks/copy_archive')
server = rootxml.find('server')

source_folder = copy_archive.find('source').text
destination_folder = copy_archive.find('destination').text
credentials = copy_archive.find('credentials').text
username = copy_archive.find('username').text
password = copy_archive.find('password').text
logfile = copy_archive.find('logfile').text
drive_letter = copy_archive.find('drive_letter').text

# Beispielaufruf
root_folder = '1'
old_string = 'CCWallesneuyesmate'
new_string = 'CCW01'

# functions

def iis_reset():
    try:
        subprocess.call(["iisreset"], shell=True)
    except:
        print("Dienst konnte nicht neugestartet werden.")

def iis_start():
    try:
        subprocess.run(['issreset', '/start'], check=True)
    except:
        print("Dienst konnte nicht neugestartet werden.")

def iis_stop():
    try:
        subprocess.run(['issreset', '/stop'], check=True)
    except:
        print("Dienst konnte nicht neugestartet werden.")

def check_copy(credentials,source_folder,destination_folder,username,password, drive_letter):
    result = messagebox.askokcancel("Bestätigung", "Sind Sie sicher, dass Sie den Job starten möchten?")
    if result:
        if (credentials == 'false'):
            copy_files(source_folder, destination_folder)
        else:
            subprocess.run(['net', 'use', f'{drive_letter}:', f'{source_folder}', f'{password}', f'/USER:{username}'], check=True)
            time.sleep(5)
            logging.info(f'Netzlaufwerk {source_folder} erfolgreich verbunden als Laufwerk {drive_letter}:')
            sync_folders(source_folder, destination_folder, 'copy.log')
            #copy_files_with_credentials(source_folder, destination_folder, username, password, drive_letter)
            # Netzlaufwerk trennen, nachdem der Kopiervorgang abgeschlossen ist
            time.sleep(3)
            subprocess.run(['net', 'use', f'{drive_letter}:', '/DELETE'], check=True)
    else:
        print("Vorgang abgebrochen!")


def copy_files(source_folder, destination_folder):
    # Sicherstellen, dass die Zielordner existiert
    os.makedirs(destination_folder, exist_ok=True)

    # Iterieren Sie über alle Dateien im Quellordner
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        # Überprüfen, ob die Datei im Zielordner nicht existiert
        if not os.path.exists(destination_path):
            try:
                # Kopieren Sie die Datei in den Zielordner
                shutil.copy2(source_path, destination_path)
                print(f'Kopiert: {filename}')
            except Exception as e:
                print(f'Fehler beim Kopieren von {filename}: {e}')



# Konfigurieren Sie das Logging-Modul nach Bedarf
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def replace_string_in_files(root_folder, old_string, new_string):
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Öffnen Sie die Datei im Lese- und Schreibmodus
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Überprüfen Sie, ob der alte String in der Datei vorhanden ist
            if old_string in file_content:
                # Ersetzen Sie den alten String durch den neuen String
                updated_content = file_content.replace(old_string, new_string)

                # Öffnen Sie die Datei im Schreibmodus und schreiben Sie den aktualisierten Inhalt
                with open(file_path, 'w') as file:
                    file.write(updated_content)

                # Protokollieren Sie die Änderung mit dem Logging-Modul
                logging.info(f'Geändert: {file_path}')


def confirm_and_execute():
    # Bestätigungsabfrage zeigen
    result = messagebox.askokcancel("Bestätigung", "Sind Sie sicher, dass Sie den Job starten möchten?")

    if result:
        # Benutzer hat "OK" geklickt, führen Sie die Funktion aus
        replace_string_in_files(root_folder, old_string, new_string)
        print('Job erfolgreich abgeschlossen.')
        logging.info('Job erfolgreich abgeschlossen.')
    else:
        print('Job abgebrochen.')
        logging.warning('Job abgebrochen.')

def get_service_status(service_name):
    try:
        service = psutil.win_service_get(service_name)
        return service.status()
    except:
        # print("Dienste wurden nicht gefunden!")
        logging.error("Dienste wurden nicht gefunden!")

def update_status(var_service_names):
    for var_service_name in var_service_names:
        status = get_service_status(var_service_name)
        if status == "running":
            print(f"{var_service_name} Dienst ist {status}")
            exec(f"lb_{var_service_name}_var.config(text='{status}')")
        elif status == "stopped":
            print(f"{var_service_name} Dienst ist {status}")
            exec(f"lb_{var_service_name}_var.config(text='{status}')")
            
    root.after(3000, lambda: update_status(var_service_names))  # Aktualisierung alle 3 Sekunden

def check_process_existence(process_name, label_var):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            lb_GEDicom_var.config(text="running")
            return

    lb_GEDicom_var.config(text="not running")   

def update_status_dicom():
    global lb_GEDicom_var  # Global deklarieren, um auf das Label zuzugreifen
    check_process_existence('GEDicomServer.exe', lb_GEDicom_var)
    root.after(3000, update_status_dicom)  # Überprüfung alle 3 Sekunden

process_name = 'GEDicomServer.exe'

# array´s
var_service_names = ['GEServiceController', 'GECardConv']

# server_info = tb.LabelFrame(frame, bootstyle="info")
server_info = tb.Label(frame)
server_info.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

# dienst_status = tb.LabelFrame(frame, bootstyle="info")
dienst_status = tb.Label(frame)
dienst_status.grid(row=0, column=1, sticky="ew", padx=20, pady=20)

lb_serverinfo = tb.Label(server_info, text="Serverinformationen", font=('Verdana',8,'bold','underline'))
lb_serverinfo.grid(row=0, column=0, sticky="ew")

lb_dienste = tb.Label(dienst_status, text="Dienste und Prozesse", font=('Verdana',8,'bold','underline'))
lb_dienste.grid(row=0, column=0, sticky="ew")

lb_hostname = tb.Label(server_info, text="Hostname:")
lb_hostname.grid(row=1, column=0, sticky="ew")

lb_hostname_var = tb.Label(server_info, text=socket.gethostname())
lb_hostname_var.grid(row=1, column=1, sticky="ew")

lb_fqdn = tb.Label(server_info, text="FQDN:")
lb_fqdn.grid(row=2, column=0, sticky="ew")

lb_fqdn_var = tb.Label(server_info, text=socket.getfqdn())
lb_fqdn_var.grid(row=2, column=1, sticky="ew")

lb_ip_address = tb.Label(server_info, text="IP-Adresse:")
lb_ip_address.grid(row=3, column=0, sticky="ew")

lb_ip_address_var = tb.Label(server_info, text=socket.gethostbyname(socket.gethostname()))
lb_ip_address_var.grid(row=3, column=1, sticky="ew")

lb_gesc = tb.Label(dienst_status, text="GEServiceController")
lb_gesc.grid(row=1, column=0, sticky="ew", padx=4)

lb_gecardcov = tb.Label(dienst_status, text="GECardConv")
lb_gecardcov.grid(row=2, column=0, sticky="ew", padx=4)

lb_GECardConv_var = tb.Label(dienst_status, text="")
lb_GECardConv_var.grid(row=2, column=1, sticky="ew", padx=4)

lb_dicomserver = tb.Label(dienst_status, text="DicomServer")
lb_dicomserver.grid(row=3, column=0, sticky="ew", padx=4)

lb_GEServiceController_var = tb.Label(dienst_status, text="")
lb_GEServiceController_var.grid(row=1, column=1, sticky="ew", padx=4)

lb_GEDicom_var = tb.Label(dienst_status, text="")
lb_GEDicom_var.grid(row=3, column=1, sticky="ew", padx=4)

# start frame jobs
lb_jobs = tb.Label(frame_jobs, text="JOBS/TASKS")
lb_jobs.grid(row=0, column=0)

lb_searchreplace = tb.Label(frame_jobs, text="Search and Replace")
lb_searchreplace.grid(row=1, column=0, sticky="W", padx=20)

btn_seandre = tb.Button(frame_jobs, text="Go", command=confirm_and_execute)
btn_seandre.grid(row=1, column=1, sticky="e")

lb_copyarchive = tb.Label(frame_jobs, text="COPY Archive")
lb_copyarchive.grid(row=2, column=0, sticky="W", padx=20, pady=10)

btn_copyarchive = tb.Button(frame_jobs, text="Go", command=lambda:check_copy(credentials,source_folder,destination_folder,username,password, drive_letter))
btn_copyarchive.grid(row=2, column=1, sticky="e", pady=10)

lb_iis_reset = tb.Label(frame_jobs, text="IIS Tool")
lb_iis_reset.grid(row=3, column=0, sticky="W", padx=20, pady=10)

btn_iis_reset = tb.Button(frame_jobs, text="Reset", command=iis_reset)
btn_iis_reset.grid(row=3, column=1, sticky="e", pady=10)

btn_iis_start = tb.Button(frame_jobs, text="Start", command=iis_start)
btn_iis_start.grid(row=3, column=2, sticky="e", pady=10, padx=10)

btn_iis_stop = tb.Button(frame_jobs, text="Stop", command=iis_stop)
btn_iis_stop.grid(row=3, column=3, sticky="e", pady=10, padx=10)

update_status(var_service_names)
update_status_dicom()


root.mainloop()