import tkinter as tk
import os
import webbrowser

class DeploymentCenterApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Deployment Center")
        # self.root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
        self.main()
        self.root.mainloop()

    def main(self):
        self.frame = tk.Frame(self.root)
        self.frame.place(x=0, y=0, width=800, height=600)

        self.label = tk.Label(self.frame, text="Deployment Center", font=("Arial", 24))
        self.label.place(x=260, y=10)
        self.button_deploy = tk.Button(self.frame, text="Deploy", font=("Arial", 12), command=self.deploy)
        self.button_deploy.place(x=200, y=300)
        self.label_deploy_value = tk.Label(self.frame, text="OFF", font=("Arial", 12))
        self.label_deploy_value.place(x=200, y=350)
        self.button_configure = tk.Button(self.frame, text="Configure", font=("Arial", 12), command=self.configure)
        self.button_configure.place(x=350, y=300)
        self.button_help = tk.Button(self.frame, text="Help", font=("Arial", 12), command=self.help)
        self.button_help.place(x=500, y=300)

    def deploy(self):
        if self.label_deploy_value.cget("text") == "ON":
            self.label_deploy_value.config(text="OFF")
            self.running = False
        else:
            self.label_deploy_value.config(text="ON")
            self.running = True

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

    def back(self):
        self.frame.destroy()
        self.main()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = DeploymentCenterApp(root)