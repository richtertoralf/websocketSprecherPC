# websocketSprecherPC
Einfaches Beispiel für eine Datenübertragung per websocket und Python als Backendanwendung
```
Sender    ----------------->    Server    ----------------->    Empfänger (Browser)

sprecherPC_scrapy_parser.py 
(json_sender.py)  --------->    /var/www/html/server/websocket_server.py
                                          ----------------->    /var/www/html/index.html
```
## Installation des Servers (Ubuntu 22.04)
```
sudo apt update
sudo apt upgrade
# prüfen, ob Python3 vorhanden ist:
python3 --version
# Ausgabe: Python 3.10.12
sudo apt install python3-pip
sudo pip3 install fastapi uvicorn
sudo pip3 install websockets
sudo apt install nginx
mkdir /var/www/html/server
# in dieses Verzeichnis jetzt die Datei websocket_server.py einfügen
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html/
```
## Anwendung auf dem Server starten
```
python3 /var/www/html/server/websocket_server.py
# im Terminal werden Meldungen ausgegeben, wenn sich ein Client per Browser verbindet und wenn der Server Daten empfängt
```
## Empfänger startet Browser
```
http://<IP-Adresse des Servers>
```
## Daten senden (Sprecher-PC)
```
# Auf dem Windows-Client, der die Daten senden soll, muss vorab Python3 installiert werden,
# und dann im Terminal die Websocket-Erweiterung:
pip install websocket-client
# im Userverzeichnis einen Ordner anlegen
cd ~
mkdir Documents\parser_sprecher-pc
# dort dann dort die Datei   

# oder alternativ zur Simulation die Datei json_sender.py einfügen
# Das Skript json_sender.py sendet Daten im json-Format zum Server
# dann so das Skript starten:
PS C:\Users\toral\Documents\parser_sprecher-pc> python json_sender.py

Im Browser des Empfängers sollten jetzt die Daten im json-Format angezeigt werden.
```




