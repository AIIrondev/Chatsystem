import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import sys
import webbrowser
import subprocess
import requests
import threading
import time


class DeploymentCenterApp:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.deploying = "Deploy"
        self.root.geometry("800x600")
        self.root.title("Deployment Center")
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        icon_image = Image.open(icon_path)
        self.icon = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(True, self.icon)
        self.main()
        self.root.mainloop()

    def main(self):
        self.frame = tk.Frame(self.root)
        self.frame.place(x=0, y=0, width=800, height=600)
        self.label = tk.Label(self.frame, text="Deployment Center", font=("Arial", 24))
        self.label.place(x=260, y=10)
        self.button_deploy = tk.Button(self.frame, text=self.deploying, font=("Arial", 12), command=self.deploy)
        self.button_deploy.place(x=200, y=300)
        self.label_api_online = tk.Label(self.frame, text="API: offline", font=("Arial", 12))
        self.label_api_online.place(x=200, y=350)
        self.label_web_online = tk.Label(self.frame, text="Web: offline", font=("Arial", 12))
        self.label_web_online.place(x=200, y=400)
        self.button_configure = tk.Button(self.frame, text="Configure", font=("Arial", 12), command=self.configure)
        self.button_configure.place(x=350, y=300)
        self.button_deployment = tk.Button(self.frame, text="Deployment Configuration", font=("Arial", 12), command=self.deployment_config)
        self.button_deployment.place(x=500, y=300)
        self.button_help = tk.Button(self.frame, text="Help", font=("Arial", 12), command=self.help)
        self.button_help.place(x=500, y=300)

    def configure(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.place(x=0, y=0, width=800, height=600)
        self.label = tk.Label(self.frame, text="Configure", font=("Arial", 24))
        self.label.place(x=300, y=10)
        self.label_api = tk.Label(self.frame, text="API Configuration", font=("Arial", 12))
        self.label_api.place(x=50, y=50)
        self.label_api_key = tk.Label(self.frame, text="API Key", font=("Arial", 12))
        self.label_api_key.place(x=50, y=100)
        self.entry_api_key = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_api_key.place(x=200, y=100)
        self.label_api_url = tk.Label(self.frame, text="API URL", font=("Arial", 12))
        self.label_api_url.place(x=50, y=150)
        self.entry_api_url = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_api_url.place(x=200, y=150)
        self.label_api_port = tk.Label(self.frame, text="API Port", font=("Arial", 12))
        self.label_api_port.place(x=50, y=200)
        self.entry_api_port = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_api_port.place(x=200, y=200)
        self.label_deployment = tk.Label(self.frame, text="Deployment Configuration", font=("Arial", 12))
        self.label_deployment.place(x=50, y=250)
        self.label_deployment_url = tk.Label(self.frame, text="Deployment URL", font=("Arial", 12))
        self.label_deployment_url.place(x=50, y=300)
        self.entry_deployment_url = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_deployment_url.place(x=200, y=300)
        self.label_deployment_port = tk.Label(self.frame, text="Deployment Port", font=("Arial", 12))
        self.label_deployment_port.place(x=50, y=350)
        self.entry_deployment_port = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_deployment_port.place(x=200, y=350)
        self.label_deployment_name = tk.Label(self.frame, text="Deployment Name", font=("Arial", 12))
        self.label_deployment_name.place(x=50, y=400)
        self.entry_deployment_name = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_deployment_name.place(x=200, y=400)
        self.label_deployment_secret = tk.Label(self.frame, text="Deployment Secret Key", font=("Arial", 12))
        self.label_deployment_secret.place(x=50, y=450)
        self.entry_deployment_secret = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_deployment_secret.place(x=200, y=450)
        self.button_save = tk.Button(self.frame, text="Save", font=("Arial", 12), command=self.save_config)
        self.button_save.place(x=50, y=500)
        self.button_back = tk.Button(self.frame, text="Back", font=("Arial", 12), command=self.back)
        self.button_back.place(x=150, y=500)

    def deployment_config(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.place(x=0, y=0, width=800, height=600)
        self.label = tk.Label(self.frame, text="Deployment Configuration", font=("Arial", 24))
        self.label.place(x=300, y=10)
        self.label_nginx = tk.Label(self.frame, text="Nginx Configuration", font=("Arial", 12))
        self.label_nginx.place(x=50, y=50)
        self.label_nginx_url = tk.Label(self.frame, text="Nginx URL", font=("Arial", 12))
        self.label_nginx_url.place(x=50, y=100)
        self.entry_nginx_url = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_nginx_url.place(x=200, y=100)
        self.label_nginx_port = tk.Label(self.frame, text="Nginx Port", font=("Arial", 12))
        self.label_nginx_port.place(x=50, y=150)
        self.entry_nginx_port = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_nginx_port.place(x=200, y=150)
        self.label_nginx_name = tk.Label(self.frame, text="Nginx Name", font=("Arial", 12))
        self.label_nginx_name.place(x=50, y=200)
        self.entry_nginx_name = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_nginx_name.place(x=200, y=200)
        self.label_firewall = tk.Label(self.frame, text="Firewall Configuration", font=("Arial", 12))
        self.label_firewall.place(x=50, y=250)
        self.label_firewall_url = tk.Label(self.frame, text="Firewall URL", font=("Arial", 12))
        self.label_firewall_url.place(x=50, y=300)
        self.entry_firewall_url = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_firewall_url.place(x=200, y=300)
        self.label_firewall_port1 = tk.Label(self.frame, text="Firewall Port1", font=("Arial", 12))
        self.label_firewall_port1.place(x=50, y=350)
        self.entry_firewall_port1 = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_firewall_port1.place(x=200, y=350)
        self.label_firewall_port2 = tk.Label(self.frame, text="Firewall Port", font=("Arial", 12))
        self.label_firewall_port2.place(x=50, y=400)
        self.entry_firewall_port2 = tk.Entry(self.frame, font=("Arial", 12))
        self.entry_firewall_port2.place(x=200, y=400)
        self.button_configure = tk.Button(self.frame, text="Save", font=("Arial", 12), command=self.save_config_deploy)
        self.button_configure.place(x=50, y=450)
        self.button_back = tk.Button(self.frame, text="Back", font=("Arial", 12), command=self.back)
        self.button_back.place(x=150, y=450)

    def back(self):
        self.frame.destroy()
        self.main()

    def save_config_deploy(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "conf", "nginx.conf"), "r") as f:
            nginx_conf = f.readlines()
            nginx_conf = [line.strip().split("=")[1] for line in nginx_conf]
        with open(os.path.join(os.path.dirname(__file__), "..", "conf", "firewall.conf"), "r") as f:
            firewall_conf = f.readlines()
            firewall_conf = [line.strip().split("=")[1] for line in firewall_conf]
        self.nginx_url = self.entry_nginx_url.get()
        self.nginx_port = self.entry_nginx_port.get()
        self.nginx_name = self.entry_nginx_name.get()
        self.firewall_url = self.entry_firewall_url.get()
        self.firewall_port1 = self.entry_firewall_port1.get()
        self.firewall_port2 = self.entry_firewall_port2.get()
        if self.nginx_url != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "nginx.conf"), "w") as f:
                f.write("host=" + self.nginx_url + "\n" + "port=" + nginx_conf[1] + "\n" + "name=" + nginx_conf[2])
        if self.nginx_port != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "nginx.conf"), "w") as f:
                f.write("host=" + nginx_conf[0] + "\n" + "port=" + self.nginx_port + "\n" + "name=" + nginx_conf[2])
        if self.nginx_name != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "nginx.conf"), "w") as f:
                f.write("host=" + nginx_conf[0] + "\n" + "port=" + nginx_conf[1] + "\n" + "name=" + self.nginx_name)
        if self.firewall_url != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "firewall.conf"), "w") as f:
                f.write("host=" + self.firewall_url + "\n" + "port1=" + firewall_conf[1] + "\n" + "port2=" + firewall_conf[2])
        if self.firewall_port1 != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "firewall.conf"), "w") as f:
                f.write("host=" + firewall_conf[0] + "\n" + "port1=" + self.firewall_port1 + "\n" + "port2=" + firewall_conf[2])
        if self.firewall_port2 != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "firewall.conf"), "w") as f:
                f.write("host=" + firewall_conf[0] + "\n" + "port1=" + firewall_conf[1] + "\n" + "port2=" + self.firewall_port2)

    def save_config(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "conf", "api.conf"), "r") as f:
            api_conf = f.readlines()
            api_conf = [line.strip().split("=")[1] for line in api_conf]
        with open(os.path.join(os.path.dirname(__file__), "..", "conf", "website.conf"), "r") as f:
            deployment_conf = f.readlines()
            deployment_conf = [line.strip().split("=")[1] for line in deployment_conf]
        self.api_key = self.entry_api_key.get()
        self.api_url = self.entry_api_url.get()
        self.api_port = self.entry_api_port.get()
        self.deployment_url = self.entry_deployment_url.get()
        self.deployment_port = self.entry_deployment_port.get()
        self.deployment_name = self.entry_deployment_name.get()
        self.deployment_key = self.entry_deployment_secret.get()
        if self.api_key != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "api.conf"), "w") as f:
                f.write("host=" + api_conf[0] + "\n" + "port=" + api_conf[1] + "\n" + "secret_key=" + self.api_key)
        if self.api_url != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "api.conf"), "w") as f:
                f.write("host=" + self.api_url + "\n" + "port=" + api_conf[1] + "\n" + "secret_key=" + api_conf[2])
        if self.api_port != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "api.conf"), "w") as f:
                f.write("host=" + api_conf[0] + "\n" + "port=" + self.api_port + "\n" + "secret_key=" + api_conf[2])
        if self.deployment_url != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "website.conf"), "w") as f:
                f.write("host=" + self.deployment_url + "\n" + "port=" + deployment_conf[1] + "\n" + "name=" + deployment_conf[2] + "\n" + "secret_key=" + deployment_conf[3])
        if self.deployment_port != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "website.conf"), "w") as f:
                f.write("host=" + deployment_conf[0] + "\n" + "port=" + self.deployment_port + "\n" + "name=" + deployment_conf[2] + "\n" + "secret_key=" + deployment_conf[3])
        if self.deployment_key != "":
            with open(os.path.join(os.path.dirname(__file__), "..", "conf", "website.conf"), "w") as f:
                f.write("host=" + deployment_conf[0] + "\n" + "port=" + deployment_conf[1] + "\n" + "name=" + self.deployment_name + "\n" + "secret_key=" + deployment_conf[3])

    def help(self):
        webbrowser.open("https://github.com/AIIrondev/Chatsystem")
    
    def deploy(self):
        if online_check.check_api() and online_check.check_deployment():
            self.running = True
        else:
            self.running = False
        if self.running:
            self.deploying = "Deploy"
            deploy.stop()
            self.label_api_online.config(text="API: ...waiting for Shutdown...")
            self.label_web_online.config(text="Web: ...waiting for Shutdown...")
            threading.Thread(target=self.check_online).start()
        else:
            self.deploying = "Stop"
            deploy.deploy()
            self.label_api_online.config(text="API: ...waiting for Start...")
            self.label_web_online.config(text="Web: ...waiting for Start...")
            threading.Thread(target=self.check_online).start()

    def check_online(self):
        time.sleep(5)
        if online_check.check_api():
            self.label_api_online.config(text="API: online")
        else:
            self.label_api_online.config(text="API: offline")
        if online_check.check_deployment():
            self.label_web_online.config(text="Web: online")
        else:
            self.label_web_online.config(text="Web: offline")
        if online_check.check_api() and online_check.check_deployment():
            self.deploying = "Stop"
            self.button_deploy.config(text=self.deploying)
        else:
            self.deploying = "Deploy"
            self.button_deploy.config(text=self.deploying)


class deploy_MongoDB:
    def __init__(self):
        pass

    def check_mongo_installed():
        if sys.platform == "win32":
            if os.path.exists("C:\\Program Files\\MongoDB\\Server\\4.4\\bin\\mongod.exe"):
                return True
            else:
                return False
        else:
            if os.system("which mongod") == 0:
                return True
            else:
                return False

    def install():
        if sys.platform == "win32":
            os.system("start /wait msiexec /i " + os.path.join(os.path.dirname(__file__), "mongodb", "mongodb-win32-x86_64-2012plus-4.4.6-signed.msi") + " /quiet")
        else:
            os.system("sudo apt-get install mongodb")

    def deploy():
        if sys.platform == "win32":
            subprocess.Popen(['cmd.exe', '/c', 'start', 'mongod'])
        else:
            subprocess.Popen(['mongod'])

    def stop():
        if sys.platform == "win32":
            os.system("taskkill /f /im mongod.exe")
        else:
            subprocess.Popen(['killall', 'mongod'])


class setup:
    def nginx(Port=80, Host="localhost"):
        subprocess.Popen(['sudo', 'touch', '/etc/nginx/sites-available/chatroom'])
        with open('/etc/nginx/sites-available/chatroom', 'w') as f:
            f.write("server {\n")
            f.write(f"    listen {Port};\n")
            f.write(f"    server_name {Host};\n")
            f.write("    location / {\n")
            f.write("        proxy_pass http://127.0.0.1:5000;\n")
            f.write("        proxy_set_header Host $host;\n")
            f.write("        proxy_set_header X-Real-IP $remote_addr;\n")
            f.write("        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n")
            f.write("    }\n")
            f.write("}\n")
        subprocess.Popen(['sudo', 'ln', '-s', '/etc/nginx/sites-available/chatroom', '/etc/nginx/sites-enabled/'])
        subprocess.Popen(['sudo', 'nginx', '-s', 'reload'])
    
    def firewall(Port1=80, Port2=5000):
        subprocess.Popen(['sudo', 'ufw', 'allow', str(Port1)])
        subprocess.Popen(['sudo', 'ufw', 'allow', str(Port2)])
        subprocess.Popen(['sudo', 'ufw', 'allow', 'ssh'])
        subprocess.Popen(['sudo', 'ufw', 'enable'])
        subprocess.Popen(['sudo', 'ufw', 'status'])
        subprocess.Popen(['sudo', 'ufw', 'status', 'verbose'])
    
    def fail2ban():
        subprocess.Popen(['sudo', 'systemctl', 'start', 'fail2ban'])
        subprocess.Popen(['sudo', 'systemctl', 'enable', 'fail2ban'])


class online_check:
    def check_api():
        with open(os.path.join(os.path.dirname(__file__), "..", "conf", "api.conf"), "r") as f:
            api_conf = f.readlines()
            api_conf = [line.strip().split("=")[1] for line in api_conf]
        try:
            response = requests.get(f"http://{api_conf[0]}:{api_conf[1]}/test_connection")
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def check_deployment():
        with open(os.path.join(os.path.dirname(__file__), "..", "conf", "website.conf"), "r") as f:
            deployment_conf = f.readlines()
            deployment_conf = [line.strip().split("=")[1] for line in deployment_conf]
        try:
            response = requests.get(f"http://{deployment_conf[0]}:{deployment_conf[1]}/test_connection")
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False

class deploy:
    def deploy():
        web_dir = os.path.join(os.path.dirname(__file__), "web")
        api_dir = os.path.join(os.path.dirname(__file__), "api")
        if sys.platform == "win32":
            subprocess.Popen(['cmd.exe', '/c', 'start', 'python', os.path.join(web_dir, "app.py")], cwd=web_dir)
            subprocess.Popen(['cmd.exe', '/c', 'start', 'python', os.path.join(api_dir, "api.py")], cwd=api_dir)
        else:
            subprocess.Popen(['gunicorn', '-w', '2', '-b', '127.0.0.1:4999', 'api:app'], cwd=api_dir)# , log_file=os.path.join(api_dir,"..", "..","log","api.log"
            subprocess.Popen(['gunicorn', '-w', '2', '-b', '127.0.0.1:5000', 'app:app'], cwd=web_dir) # =os.path.join(web_dir,"..", "..","log","api.log")

    def stop():
        if sys.platform == "win32":
            os.system("taskkill /f /im python.exe")
        else:
            subprocess.Popen(['killall', 'gunicorn'])


if __name__ == "__main__":
    root = tk.Tk()
    app = DeploymentCenterApp(root)
