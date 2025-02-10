# **Chat Room Application**

Dieses Projekt ist eine private Chatroom-Anwendung, die es Benutzern ermöglicht, in Echtzeit zu kommunizieren. Die Anwendung basiert auf Flask, MongoDB und einem React-Frontend und kann auf einem Ubuntu-Server bereitgestellt werden.

---

## **Inhalt**
- [Ziel](#ziel)
- [Server-Setup](#server-setup)
  - [Linux (Ubuntu)](#linux-ubuntu)
  - [Windows](#windows)
  - [Datenbank (MongoDB)](#datenbank-mongodb)
- [Client-Setup](#client-setup)
  - [Webanwendung](#webanwendung)
  - [Mobile App](#mobile-app)
- [Installation](#installation)
  - [Linux-Installation](#linux-installation)
  - [Windows-Installation](#windows-installation)
- [SSL-Zertifikat mit Let's Encrypt](#ssl-zertifikat-mit-lets-encrypt)
- [Firewall und Sicherheit](#firewall-und-sicherheit)
- [Nutzung](#nutzung)
- [Lizenz](#lizenz)

---

## **Ziel**

Das Ziel dieses Projekts ist die einfache Bereitstellung und Verwaltung eines Chat-Systems. Du kannst einen alten Computer oder einen Server nutzen, um die Software zu starten und zu konfigurieren.

---

## **Server-Setup**

### **Linux (Ubuntu)**

Der Server läuft am besten unter **Ubuntu Server**. Die Hauptkomponenten sind:
- **Flask (Backend)**
- **MongoDB (Datenbank)**
- **NGINX (Reverse Proxy, optional)**

**Installation:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx -y
```

### **Windows**

Auf Windows kann der Server ebenfalls mit Python und MongoDB gestartet werden. Die Einrichtung erfolgt manuell.

### **Datenbank (MongoDB)**

MongoDB speichert die Chat-Nachrichten. Installation auf Ubuntu:
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install mongodb-org -y
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## **Client-Setup**

### **Webanwendung**

Die Web-App ist mit React entwickelt und läuft über Flask.
```bash
cd client
npm install
npm run build
```

### **Mobile App**

Falls eine mobile App existiert, wird sie als separate Anwendung bereitgestellt.

---

## **Installation**

### **Linux-Installation**
Speichere folgendes Skript als `install_chatroom.sh` und führe es aus:
```bash
#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv mongodb-org -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python3 app.py > /dev/null 2>&1 &
echo "Chatroom-Server läuft auf http://$(hostname -I | awk '{print $1}'):5000"
```
**Berechtigungen setzen und ausführen:**
```bash
chmod +x install_chatroom.sh
sudo ./install_chatroom.sh
```

### **Windows-Installation**
1. **Python installieren** ([Download](https://www.python.org/downloads/))
2. **MongoDB installieren** ([Download](https://www.mongodb.com/try/download/community))
3. **Flask starten:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## **SSL-Zertifikat mit Let's Encrypt**

### **1. Certbot installieren**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### **2. NGINX konfigurieren**
Erstelle eine Datei:
```bash
sudo nano /etc/nginx/sites-available/chatroom
```
Füge Folgendes ein:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Aktivieren und NGINX neustarten:
```bash
sudo ln -s /etc/nginx/sites-available/chatroom /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

### **3. SSL-Zertifikat abrufen**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### **4. Automatische Verlängerung einrichten**
```bash
sudo certbot renew --dry-run
```
Falls erfolgreich, einen Cronjob hinzufügen:
```bash
sudo crontab -e
```
Füge hinzu:
```
0 3 * * * certbot renew --quiet && systemctl reload nginx
```

---

## **Firewall und Sicherheit**

https://certbot.eff.org/instructions?ws=nginx&os=snap

### **Firewall konfigurieren (UFW)**
```bash
sudo ufw allow 22/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### **Fail2Ban installieren** (Schutz gegen Brute-Force-Angriffe)
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban --now
```

---

## **Nutzung**

1. **Starte den Server:**
```bash
python3 app.py
```
2. **Zugriff über den Browser:**
```
http://yourdomain.com
```

---

## **Lizenz**

Dieses Projekt steht unter der **Apache 2.0 Lizenz**. Siehe die Datei [LICENSE](LICENSE) für weitere Details.

