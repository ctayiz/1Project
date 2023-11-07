import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap  as tb
import socket
import psutil
import subprocess
import time
import threading

root = tb.Window(themename="superhero")
root.title("CCW Tool by Cihan")
root.geometry("600x300")

frame = tb.Frame(root)
frame.pack()

# functions

def get_service_status(service_name):
    try:
        service = psutil.win_service_get(service_name)
        return service.status()
    except:
        print("Dienste wurden nicht gefunden!")

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

process_name = 'Greenshot.exe'

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

update_status(var_service_names)
update_status_dicom()


root.mainloop()