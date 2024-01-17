import tkinter as tk
from tkinter import font
from subprocess import Popen
import subprocess
import os
import pwd

# Change to the home folder
os.chdir(os.path.expanduser("~"))

# Check sudo privileges
print("Checking sudo privileges")
try:
    subprocess.run(['sudo', '-v'], check=True)
    print("Sudo credentials authenticated.")
except subprocess.CalledProcessError:
    print("Failed to verify sudo credentials.")
    exit(1)

# Define the groups of clients
ec_group = ("geth", "besu", "nethermind")
cc_group = ("teku", "nimbus", "prysm", "lighthouse")

# Define the groups of clients - capitalized
ec_cap = ("Geth", "Besu", "Nethermind")
cc_cap = ("Teku", "Nimbus", "Prysm", "Lighthouse")

# Check if a user exists
def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

# Initialize Tkinter root
root = tk.Tk()
root.title("Validator Controller")
root.configure(background="#282C34")
root.geometry("1600x800")

# Initialize the StringVar objects
execution_update_var = tk.StringVar()
consensus_update_var = tk.StringVar()
mevboost_var = tk.StringVar()

# Set default values based on user existence
def set_default_values():
    # Check and set default for execution client
    for client in ec_group:
        if user_exists(client):
            execution_update_var.set(client.capitalize())
            break

    # Check and set default for consensus client
    for client in cc_group:
        username_to_check = client
        if client == "prysm":
            username_to_check = "prysmbeacon"
        elif client == "lighthouse":
            username_to_check = "lighthousebeacon"

        if user_exists(username_to_check):
            consensus_update_var.set(client.capitalize())
            break

    # Check and set default for MEV-Boost
    if user_exists('mevboost'):
        mevboost_var.set('On')
    else:
        mevboost_var.set('Off')

# Set default values
set_default_values()

def start_clients():
    execution_client = execution_update_var.get().lower()
    consensus_client = consensus_update_var.get().lower()
    mevboost_option = mevboost_var.get().lower()

    # Start the selected execution client
    if execution_client in ec_group:
        print(f"Starting {execution_client}...")
        Popen(['sudo', 'systemctl', 'start', execution_client])

    # Start the selected consensus client
    if consensus_client == "prysm":
        Popen(['sudo', 'systemctl', 'start', 'prysmbeacon'])
        Popen(['sudo', 'systemctl', 'start', 'prysmvalidator'])
    elif consensus_client == "lighthouse":
        Popen(['sudo', 'systemctl', 'start', 'lighthousebeacon'])
        Popen(['sudo', 'systemctl', 'start', 'lighthousevalidator'])
    elif consensus_client in cc_group:
        Popen(['sudo', 'systemctl', 'start', consensus_client])

    # Start MEV-Boost if selected
    if mevboost_option == "on":
        print("Starting MEV-Boost...")
        Popen(['sudo', 'systemctl', 'start', 'mevboost'])

def stop_clients():
    def stop_service(service_name):
        print(f"Attempting to stop {service_name}...")
        process = subprocess.Popen(['sudo', 'systemctl', 'stop', service_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print(f"Successfully stopped {service_name}")
        else:
            print(f"Failed to stop {service_name}. Error: {stderr.decode().strip()}")

    # Stop all execution clients
    for client in ec_group:
        stop_service(client)

    # Stop all consensus clients
    for client in cc_group:
        if client == "prysm":
            stop_service('prysmbeacon')
            stop_service('prysmvalidator')
        elif client == "lighthouse":
            stop_service('lighthousebeacon')
            stop_service('lighthousevalidator')
        else:
            stop_service(client)

    # Always stop MEV-Boost
    print("Stopping MEV-Boost...")
    stop_service('mevboost')

def show_journals():
    execution_client = execution_update_var.get().lower()
    consensus_client = consensus_update_var.get().lower()
    mevboost_option = mevboost_var.get().lower()
    
    if execution_client in ec_group:
        os.system(f"nohup gnome-terminal -- journalctl -fu {execution_client} &")

    if consensus_client == "prysm":
        os.system("nohup gnome-terminal -- journalctl -fu prysmbeacon &")
        os.system("nohup gnome-terminal -- journalctl -fu prysmvalidator &")
    elif consensus_client == "lighthouse":
        os.system("nohup gnome-terminal -- journalctl -fu lighthousebeacon &")
        os.system("nohup gnome-terminal -- journalctl -fu lighthousevalidator &")
    elif consensus_client in cc_group:
        os.system(f"nohup gnome-terminal -- journalctl -fu {consensus_client} &")

    # Show MEV-Boost logs if it was on
    if mevboost_option == "on":
        os.system("nohup gnome-terminal -- journalctl -fu mevboost &")

def service_file_exists(service_name):
    return os.path.exists(f"/etc/systemd/system/{service_name}.service")

def edit_service_file():
    execution_client = execution_update_var.get().lower()
    consensus_client = consensus_update_var.get().lower()
    mevboost_option = mevboost_var.get().lower()
    
    if execution_client in ec_group and service_file_exists(execution_client):
        os.system(f"nohup gnome-terminal -- sudo nano /etc/systemd/system/{execution_client}.service &")

    if consensus_client in cc_group:
        if consensus_client == "prysm" and service_file_exists('prysmbeacon'):
            os.system("nohup gnome-terminal -- sudo nano /etc/systemd/system/prysmbeacon.service &")
            if service_file_exists('prysmvalidator'):
                os.system("nohup gnome-terminal -- sudo nano /etc/systemd/system/prysmvalidator.service &")
        elif consensus_client == "lighthouse" and service_file_exists('lighthousebeacon'):
            os.system("nohup gnome-terminal -- sudo nano /etc/systemd/system/lighthousebeacon.service &")
            if service_file_exists('lighthousevalidator'):
                os.system("nohup gnome-terminal -- sudo nano /etc/systemd/system/lighthousevalidator.service &")
        elif service_file_exists(consensus_client):
            os.system(f"nohup gnome-terminal -- sudo nano /etc/systemd/system/{consensus_client}.service &")

    # For MEV-Boost
    mevboost_option = mevboost_var.get().lower()
    if mevboost_option == "on" and service_file_exists('mevboost'):
        os.system("nohup gnome-terminal -- sudo nano /etc/systemd/system/mevboost.service &")

label_font = font.nametofont("TkDefaultFont").copy()
label_font.config(size=20)

# Dropdown for Execution Client
execution_update_label = tk.Label(root, text="Execution Client:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
execution_update_label.grid(column=0, row=0, padx=30, pady=15, sticky='e')
execution_update_menu = tk.OptionMenu(root, execution_update_var, *ec_cap)
execution_update_menu.config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=label_font, takefocus=True)
execution_update_menu["menu"].config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=label_font)
execution_update_menu.grid(column=1, row=0, padx=30, pady=15, ipadx=40, ipady=10)

# Dropdown for Consensus Client
consensus_update_label = tk.Label(root, text="Consensus Client:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
consensus_update_label.grid(column=0, row=1, padx=30, pady=15, sticky='e')
consensus_update_menu = tk.OptionMenu(root, consensus_update_var, *cc_cap)
consensus_update_menu.config(bg="#FF9800", fg="#FFFFFF", activebackground="#FFA726", activeforeground="#FFFFFF", font=label_font, takefocus=True)
consensus_update_menu["menu"].config(bg="#FF9800", fg="#FFFFFF", activebackground="#FFA726", activeforeground="#FFFFFF", font=label_font)
consensus_update_menu.grid(column=1, row=1, padx=30, pady=15, ipadx=40, ipady=10)

# Dropdown for MEV-Boost On/Off
mevboost_label = tk.Label(root, text="MEV-Boost On/Off:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
mevboost_label.grid(column=0, row=2, padx=30, pady=15, sticky='e')
mevboost_options = ('On', 'Off')
mevboost_menu = tk.OptionMenu(root, mevboost_var, *mevboost_options)
mevboost_menu.config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font, takefocus=True)
mevboost_menu["menu"].config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font)
mevboost_menu.grid(column=1, row=2, padx=30, pady=15, ipadx=40, ipady=10)

# Journals button (top left)
journals_button = tk.Button(root, text="Journals", command=show_journals, bg="#6C757D", fg="#FFFFFF", activebackground="#5A6268", activeforeground="#FFFFFF", font=label_font, takefocus=True)
journals_button.grid(column=0, row=3, padx=30, pady=20)

# Service Files button (bottom left)
service_files_button = tk.Button(root, text="Service Files", command=edit_service_file, bg="#6C757D", fg="#FFFFFF", activebackground="#5A6268", activeforeground="#FFFFFF", font=label_font, takefocus=True)
service_files_button.grid(column=0, row=4, padx=30, pady=20)

# Start button (top right)
start_button = tk.Button(root, text="Start All", command=start_clients, bg="#282C34", fg="#FFFFFF", activebackground="#28A745", activeforeground="#FFFFFF", font=label_font, takefocus=True)
start_button.grid(column=1, row=3, padx=30, pady=10)

# Stop button (bottom right)
stop_button = tk.Button(root, text="Stop All", command=stop_clients, bg="#282C34", fg="#FFFFFF", activebackground="#DC3545", activeforeground="#FFFFFF", font=label_font, takefocus=True)
stop_button.grid(column=1, row=4, padx=30, pady=10)

root.mainloop()

