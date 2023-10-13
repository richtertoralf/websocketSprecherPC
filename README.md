# websocketSprecherPC
Einfaches Beispiel für eine Datenübertragung per websocket und Python als Backendanwendung
```
Sender    ----------------->    Server    ----------------->    Empfänger
Sprecher-PC                     z.B. Ubuntu 22.04               beliebiger Browser

| Winlaufen sendet Daten
| an Sprecher-PC

| Netzwerksniffer und Parser
| läuft auf dem Sprecher-PC
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
# im Terminal werden Meldungen ausgegeben, wenn sich ein Client per Browser verbindet und welche der Server Daten empfängt
```
## Empfänger startet Browser
```
http://<IP-Adresse des Servers>
Für den Test reicht es, die IP Adresse oder Domain des Servers im Browser einzugeben.
```
## Daten senden (Sprecher-PC)
```
# Auf dem Windows-Client, der die Daten senden soll, muss vorab Python3 installiert werden,
# und dann im Terminal die Websocket-Erweiterung:
pip install websocket-client
# im Userverzeichnis einen Ordner anlegen
cd ~
mkdir Documents\parser_sprecher-pc
# dort dann dort die Datei sprecherPC_scrapy_parser.py einfügen.
# dann so das Skript starten:
PS C:\Users\toral\Documents\parser_sprecher-pc> python sprecherPC_scrapy_parser.py
# Alternativ kann zur Simulation, wenn kein Winlaufen und Sprecher-PC zur Verfügung stehen,
# auch die die Datei json_sender.py verwendet werden.
# Das Skript json_sender.py sendet Daten im json-Format zum Server.

Im Browser des Empfängers sollten jetzt die Daten im json-Format angezeigt werden.
```

## Details zu den Programmen
### sprecherPC_scrapy_parser.py
Dieses Skript, entwickelt in Python unter Verwendung der Scapy-Bibliothek, ermöglicht die Extraktion von Daten aus dem Netzwerkverkehr. Es ist speziell für den Empfang von Paketen zwischen einem PC auf dem Winlaufen (IP-Adresse '192.168.100.10') und einem PC, auf dem das Programm Sprecher-PC (IP Adresse '192.168.100.20') läuft. Es wird eine spezifizierte Netzwerkschnittstelle abgehört. Da keine Angaben zum verwendeten Protokoll vorlag, wurde der Netzwerkverkehr mit Wireshark mitgeschnitten und dann ein Parser entwickelt, der aus den Rohdaten nutzbare Daten extrahiert.  
Das Skript ist so konzipiert, dass es kontinuierlich nach den angegebenen Netzwerkpaketen sucht und sie analysiert. Die analysierten und korrigierten Daten werden in Echtzeit über WebSocket an den Server gesendet, während sie auch auf der Konsole ausgegeben werden, um dem Entwickler einen Überblick über die verarbeiteten Daten zu geben.

#### Datenextraktion, -bereinigung, -strukturierung und versenden:
Die empfangenen Netzwerkpakete werden analysiert und der Payload wird extrahiert.
Nicht-ASCII-Zeichen und Leerzeichen werden aus den Rohdaten entfernt, um eine klare, lesbare Datenstruktur zu erstellen.
Die Daten werden gemäß einem spezifischen Muster analysiert und in ein strukturiertes Format umgewandelt.
Die extrahierten Daten werden aufbereitet, insbesondere Namen werden von überflüssigen Zeichen befreit und in ein gut lesbares Format gebracht.
JSON-Formatierung und Übertragung:
Die strukturierten Daten werden in das JSON-Format konvertiert, um sie besser zu verarbeiten.
Die JSON-Daten werden über eine WebSocket-Verbindung an einen entfernten Server gesendet.
#### Infos zum Programmablauf:
##### Import von Modulen:
Das Skript beginnt mit dem Import von verschiedenen Python-Bibliotheken:
- scapy.all: Die Hauptbibliothek, die für das Erfassen und Analysieren von Netzwerkverkehr verwendet wird.
- re: Die regulären Ausdrücke werden verwendet, um bestimmte Muster in den Daten zu finden und zu extrahieren.
- json: Wird verwendet, um die Daten in das JSON-Format zu konvertieren.
- websocket: Diese Bibliothek ermöglicht die WebSocket-Kommunikation.
##### Definition von Hilfsfunktionen:
- clean_data(data): Entfernt Leerzeichen und nicht-ASCII-Zeichen aus den Daten.
- parse_data(data): Analysiert die sauberen Daten anhand eines spezifischen Musters und extrahiert Rang, Startnummer, Name, Laufzeit und Rückstand.
- correct_names(parsed_data): Bereinigt die Namen in den analysierten Daten, indem überflüssige Zeichen entfernt und Leerzeichen hinzugefügt werden.
- Packet Callback-Funktion: Die Funktion packet_callback(packet) wird definiert, um aufgerufen zu werden, wenn ein neues Netzwerkpaket empfangen wird.
##### Programmablauf:
- Es wird überprüft, ob das Paket die gewünschten Kriterien erfüllt: IP-Quell- und Zieladressen sowie spezifische TCP-Flags.
- Der Payload des TCP-Pakets wird als Rohdaten extrahiert.  
Datenverarbeitung:  
- Die Rohdaten werden zuerst in Hexadezimalformat konvertiert.
- Dann werden nicht druckbare Zeichen und '00'-Bytes entfernt, um saubere Hex-Daten zu erhalten.
- Die Hex-Daten werden in ein UTF-8-Zeichenkette umgewandelt, wobei Nicht-ASCII-Zeichen ignoriert werden. Dies ist der Punkt, an dem die Daten für die weitere Verarbeitung bereit sind.
- Die extrahierten Daten werden nach dem definierten Muster analysiert und in ein strukturiertes Format umgewandelt.
- Die Namen werden korrigiert, indem überflüssige Zeichen entfernt und Leerzeichen hinzugefügt werden.
##### Datenübertragung über WebSocket:
- Die strukturierten Daten werden in das JSON-Format konvertiert.
- Eine WebSocket-Verbindung wird zu einem entfernten Server (mit der angegebenen IP-Adresse und dem Port) hergestellt.
- Die JSON-Daten werden über die WebSocket-Verbindung an den Server gesendet.
##### Fehlerbehandlung:
Wenn ein Unicode-Decodierungsfehler auftritt, wird er erfasst und ignoriert, um die Programmausführung nicht zu unterbrechen.
##### Ausgabe:
Während des gesamten Prozesses werden verschiedene Informationen, einschließlich der analysierten Daten, auf der Konsole ausgegeben.

### websocket_server.py
/var/www/html/server/websocket_server.py  
Dieses Python-Skript dient als einfacher WebSocket-Server, der auf ankommende Verbindungen lauscht und Nachrichten in Echtzeit an die verbundenen Clients weiterleitet.  

Hier ist eine Beschreibung des Programms:
##### Importieren von Modulen:
- asyncio: Ein Framework, das es ermöglicht, asynchrone und parallele Codeausführung in Python zu implementieren.
- websockets: Eine Bibliothek, die eine asynchrone Schnittstelle für WebSocket-Kommunikation bereitstellt.
##### Initialisierung des WebSocket-Servers:
Das Skript initialisiert einen WebSocket-Server, der auf allen verfügbaren Netzwerkschnittstellen ('0.0.0.0') auf Port 8765 lauscht.
##### Behandlung eingehender Verbindungen:
Die Funktion server(websocket, path) wird aufgerufen, wenn ein neuer Client eine WebSocket-Verbindung zum Server herstellt.
Der Server empfängt und sendet Nachrichten in einem asynchronen Kontext.
##### Verwaltung aktiver Verbindungen:
- Eine Liste namens connected_clients wird erstellt, um alle aktiven WebSocket-Verbindungen zu speichern.
- Wenn ein Client sich verbindet, wird seine WebSocket-Verbindung zur connected_clients-Liste hinzugefügt.
- Wenn eine Nachricht empfangen wird, wird die Nachricht an alle Clients in der connected_clients-Liste weitergeleitet.
- Wenn eine Verbindung geschlossen wird, wird sie aus der Liste entfernt.
##### Serverstart und Endlosschleife:
- Der WebSocket-Server wird gestartet, indem die Funktion websockets.serve() aufgerufen wird.
- Die Ausführung des Servers wird mit asyncio.get_event_loop().run_until_complete() und asyncio.get_event_loop().run_forever() gesteuert.
- Der Server bleibt in einer Endlosschleife und wartet auf eingehende Verbindungen.

### index.html
/var/www/html/index.html
HTML-WebSocket-Datenanzeige:  
Dieses HTML-Dokument dient als WebSocket-Client, der sich mit einem WebSocket-Server verbindet, um empfangene Daten anzuzeigen. Dieses HTML-Skript ermöglicht es einem Benutzer, Daten in Echtzeit von einem WebSocket-Server zu empfangen und anzuzeigen, was besonders nützlich ist, wenn Echtzeitaktualisierungen von Serverdaten benötigt werden. Es bietet eine einfache Möglichkeit, WebSocket-Kommunikation in Webanwendungen zu integrieren und mit dem Server zu interagieren.  
Hier wird später die Logik, wie sie z.B. beim Sprecher-PC vorhanden ist, integriert.  
Außerdem erfolgt hier die Aufbereitung und Gestaltung der daten, wie sie als Overlay für einen Livestream benötigt werden.  

##### HTML-Struktur:
Das Dokument enthält eine div-Element mit der ID data-container, die dazu verwendet wird, die empfangenen Daten anzuzeigen.
##### JavaScript-Code:
Das JavaScript-Skript erstellt eine WebSocket-Verbindung zum Server mit der Adresse ws://192.168.10.211:8765.  
- socket.onmessage: Diese Funktion wird ausgeführt, wenn eine Nachricht vom Server empfangen wird. Die empfangenen Daten werden aus dem JSON-Format geparst und im data-container-Element angezeigt.
- socket.onclose: Diese Funktion wird aufgerufen, wenn die Verbindung geschlossen wird. Sie gibt Informationen zum Schließgrund aus, sei es ein regulärer Schließvorgang oder ein abrupter Abbruch.
- socket.onerror: Diese Funktion wird ausgeführt, wenn ein Fehler während der Verbindung auftritt. Der Fehler wird in der Konsole angezeigt.  
##### Programmablauf:
- Die HTML-Seite wird geladen und das JavaScript-Skript wird aktiviert.
- Ein WebSocket wird erstellt und eine Verbindung zum Server unter der angegebenen IP-Adresse und dem Port hergestellt.
- Wenn eine Nachricht vom Server empfangen wird, wird sie geparst und im data-container-Element angezeigt.
- Wenn die Verbindung geschlossen wird, werden entsprechende Informationen in der Konsole ausgegeben.
- Wenn ein Fehler während der Verbindung auftritt, wird die Fehlermeldung ebenfalls in der Konsole angezeigt.
