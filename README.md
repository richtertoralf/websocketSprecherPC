# websocketSprecherPC
Einfaches Beispiel für eine Datenübertragung per websocket und Python vom Sprecher-PC zum Server:  
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
# im Terminal werden Meldungen ausgegeben, wenn sich ein Client per Browser verbindet und welche Daten der Server empfängt
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
Dieses Skript, entwickelt in Python unter Verwendung der Scapy-Bibliothek, ermöglicht die Erkennung und Extraktion von Daten aus dem Netzwerkverkehr. Im Beispiel wird geziehlt nach Paketen zwischen einem PC auf dem Winlaufen (IP-Adresse '192.168.100.10') und einem PC, auf dem das Programm Sprecher-PC (IP Adresse '192.168.100.20') läuft, gesucht. Es wird eine konkrete Netzwerkschnittstelle abgehört. Da keine Angaben zum verwendeten Protokoll vorlag, wurde der Netzwerkverkehr mit Wireshark mitgeschnitten und dann von mir ein Parser entwickelt, der aus den Rohdaten nutzbare Daten extrahiert. Zum Sprecher-PC werden noch mehr Daten übertragen, als die ich in diesem Beispiel extrahiere.  
Das Skript ist so konzipiert, dass es kontinuierlich nach den angegebenen Netzwerkpaketen sucht und sie analysiert. Die analysierten und dann gefilterten und aufbereiteten Daten werden in Echtzeit über WebSocket an den Server gesendet, während sie auch auf der Konsole ausgegeben werden, um dem Entwickler einen Überblick über die verarbeiteten Daten zu geben.
#### Datenstruktur Winlaufen -> Sprecher-PC
Da mir keine Angaben zur Schnittstelle und zur Datenstruktur zur Verfügung standen, musste sehr aufwendig im Datenstrom gesucht werden.
```
Hexdump:
00e0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 71 00  ..............q.
00f0  7E 00 1F 73 71 00 7E 00 01 00 00 00 12 73 71 00  ~..sq.~......sq.
0100  7E 00 01 00 00 00 00 73 71 00 7E 00 01 00 00 00  ~......sq.~.....
0110  05 75 71 00 7E 00 23 00 00 00 07 74 00 01 31 74  .uq.~.#....t..1t
0120  00 02 36 37 74 00 0C 4C 4F 47 45 53 20 4D 61 72  ..67t..LOGES Mar
0130  67 69 74 71 00 7E 01 A8 71 00 7E 01 05 74 00 09  gitq.~..q.~..t..
0140  34 3A 33 30 3A 31 35 2E 39 74 00 09 30 3A 30 30  4:30:15.9t..0:00
0150  3A 30 30 2E 30 75 71 00 7E 00 23 00 00 00 07 74  :00.0uq.~.#....t
0160  00 01 32 74 00 02 36 38 74 00 10 42 52 4F 43 4B  ..2t..68t..BROCK
0170  4D 45 49 45 52 20 53 6F 66 69 65 71 00 7E 01 BC  MEIER Sofieq.~..
0180  71 00 7E 00 B8 74 00 09 34 3A 33 34 3A 35 31 2E  q.~..t..4:34:51.
0190  37 74 00 09 30 3A 30 34 3A 33 35 2E 38 75 71 00  7t..0:04:35.8uq.
01a0  7E 00 23 00 00 00 07 74 00 01 33 74 00 02 36 39  ~.#....t..3t..69
01b0  74 00 0B 45 56 41 4E 53 20 44 65 6E 6E 79 71 00  t..EVANS Dennyq.
01c0  7E 01 D6 71 00 7E 00 CC 74 00 09 34 3A 33 36 3A  ~..q.~..t..4:36:
01d0  35 37 2E 31 74 00 09 30 3A 30 36 3A 34 31 2E 32  57.1t..0:06:41.2
01e0  75 71 00 7E 00 23 00 00 00 07 74 00 01 34 74 00  uq.~.#....t..4t.
01f0  02 37 30 74 00 0F 52 C3 84 54 5A 20 53 69 67 69  .70t..R..TZ Sigi
0200  73 68 65 6C 6D 71 00 7E 01 F6 71 00 7E 00 29 74  shelmq.~..q.~.)t
0210  00 09 34 3A 33 39 3A 33 36 2E 34 74 00 09 30 3A  ..4:39:36.4t..0:
0220  30 39 3A 32 30 2E 35 75 71 00 7E 00 23 00 00 00  09:20.5uq.~.#...
0230  07 74 00 01 35 74 00 02 37 31 74 00 12 47 49 45  .t..5t..71t..GIE
0240  53 42 52 45 43 48 54 20 48 65 6E 64 72 69 6B 71  SBRECHT Hendrikq
0250  00 7E 02 1C 71 00 7E 00 29 74 00 09 34 3A 34 37  .~..q.~.)t..4:47
0260  3A 32 35 2E 33 74 00 09 30 3A 31 37 3A 30 39 2E  :25.3t..0:17:09.
0270  34 75 71 00 7E 00 23 00 00 00 07 74 00 01 36 74  4uq.~.#....t..6t
0280  00 02 37 32 74 00 0F 46 52 45 49 54 41 47 20 48  ..72t..FREITAG H
0290  65 6C 6C 6D 75 74 74 00 09 52 61 6D 6D 69 6E 67  ellmutt..Ramming
02a0  65 6E 71 00 7E 00 48 74 00 09 34 3A 35 36 3A 34  enq.~.Ht..4:56:4
02b0  38 2E 35 74 00 09 30 3A 32 36 3A 33 32 2E 36 71  8.5t..0:26:32.6q
02c0  00 7E 00 2C 71 00 7E 00 2D 71 00 7E 00 35        .~.,q.~.-q.~.5   
``` 
```
# gefilterter Datenstream
sq~sq~uq~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~q~uq~q~sq~sq~sq~uq~#t1t201tNEUMLLER Hansgntherq~q~nt4:28:07.1t0:00:00.0uq~#t2t200tVIETEN Kreszenzq~q~}t4:28:10.0t0:00:02.9uq~#t3t202tFROBSE Larsq~$q~)t4:30:55.3t0:02:48.2uq~#t4t203tLOHMEIER Heinzjrgenq~Dq~nt4:31:05.0t0:02:57.9uq~#t5t204tZINN Emmiq~jq~kt4:46:39.1t0:18:32.0uq~#t6t205tKLTZER rnbertq~q~1t5:02:49.8t0:34:42.7uq~#t7t206tREHBERG Liamq~q~t5:06:11.7t0:38:04.6uq~#t8t207tELSHOLZ Waltrautq~q~t5:07:04.0t0:38:56.9uq~#t9t208tRUPPELT Piusq~?q~Xt6:44:31.1t2:16:24.0uq~#t10t209tREUSS NeitharttAbtweilerq~t8:00:40.0t3:32:32.9q~!q~"q~*  
```
```
# daraus selektierte Daten im JSON-Format
[{'Rang': '1', 'Startnummer': '201', 'Name': 'NEUMLLERHansgnther', 'Laufzeit': '4:28:07.1', 'Rückstand': '0:00:00.0'}, {'Rang': '2', 'Startnummer': '200', 'Name': 'VIETENKreszenz', 'Laufzeit': '4:28:10.0', 'Rückstand': '0:00:02.9'}, {'Rang': '3', 'Startnummer': '202', 'Name': 'FROBSELars', 'Laufzeit': '4:30:55.3', 'Rückstand': '0:02:48.2'}, {'Rang': '4', 'Startnummer': '203', 'Name': 'LOHMEIERHeinzjrgen', 'Laufzeit': '4:31:05.0', 'Rückstand': '0:02:57.9'}, {'Rang': '5', 'Startnummer': '204', 'Name': 'ZINNEmmi', 'Laufzeit': '4:46:39.1', 'Rückstand': '0:18:32.0'}, {'Rang': '6', 'Startnummer': '205', 'Name': 'KLTZERArnbert', 'Laufzeit': '5:02:49.8', 'Rückstand': '0:34:42.7'}, {'Rang': '7', 'Startnummer': '206', 'Name': 'REHBERGLiam', 'Laufzeit': '5:06:11.7', 'Rückstand': '0:38:04.6'}, {'Rang': '8', 'Startnummer': '207', 'Name': 'ELSHOLZWaltraut', 'Laufzeit': '5:07:04.0', 'Rückstand': '0:38:56.9'}, {'Rang': '9', 'Startnummer': '208', 'Name': 'RUPPELTPius', 'Laufzeit': '6:44:31.1', 'Rückstand': '2:16:24.0'}, {'Rang': '10', 'Startnummer': '209', 'Name': 'REUSSNeithartt Abtweiler', 'Laufzeit': '8:00:40.0', 'Rückstand': '3:32:32.9'}]                                                                                                                                                                                    
```

#### Datenextraktion, -bereinigung, -strukturierung und versenden:
- Die empfangenen Netzwerkpakete werden analysiert und der Payload wird extrahiert.
- Nicht-ASCII-Zeichen und Leerzeichen werden aus den Rohdaten entfernt, um eine lesbarere Datenstruktur zu erstellen.
- Die Daten werden gemäß einem spezifischen Muster analysiert und in ein strukturierteres Format umgewandelt.
#### JSON-Formatierung und Übertragung:
- Die strukturierten Daten werden in das JSON-Format konvertiert, um sie später leichter verarbeiten zu können.
- Die JSON-Daten werden über eine WebSocket-Verbindung an einen entfernten Server gesendet.
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
###### Datenverarbeitung:  
- Die Rohdaten werden zuerst ins Hexadezimalformat konvertiert.
- Dann werden nicht druckbare Zeichen und '00'-Bytes entfernt, um sauberere Hex-Daten zu erhalten.
- Die Hex-Daten werden in ein UTF-8-Zeichenkette umgewandelt, wobei Nicht-ASCII-Zeichen ignoriert werden. Dies ist der Punkt, an dem die Daten für die weitere Verarbeitung bereit sind. Vermutlich verliere ich hier die deutschen Umlaute. Das muss nochmal überarbeitet werden.
- Die extrahierten Daten werden nach dem definierten Muster analysiert und in ein strukturiertes Format umgewandelt. Es wird gezielt nach Rang, Startnummer, Name, Laufzeit und Rückstand gesucht.
- Die Namen werden korrigiert, indem überflüssige Zeichen entfernt werden. Die Namen werden nicht unbedingt benötigt, da es aus dem Programm Winlaufen einen separaten Export der Starliste (Startlist.csv) gibt und daraus dann auf dem Server oder letztlich  der Frontendanwendung, Name, Verein, Nation, Altersklasse/Kategorie abgeglichen werden können.
##### Datenübertragung über WebSocket:
- Die strukturierten Daten werden in das JSON-Format konvertiert.
- Eine WebSocket-Verbindung wird zu einem entfernten Server (mit der angegebenen IP-Adresse und dem Port) hergestellt.
- Die JSON-Daten werden über die WebSocket-Verbindung an den Server gesendet.
##### Fehlerbehandlung:
Wenn ein Unicode-Decodierungsfehler auftritt, wird er erfasst und ignoriert, um die Programmausführung nicht zu unterbrechen. Das kann passieren, da zwischen dem Winlaufe und dem Sprecher-PC noch mehr Datenverkehr stattfindet, als von mir ausgewertet wird.
##### Ausgabe:
Während des gesamten Prozesses werden verschiedene Informationen, einschließlich der analysierten Daten, auf der Konsole ausgegeben.
### websocket_server.py
/var/www/html/server/websocket_server.py  
Dieses Python-Skript dient als einfacher WebSocket-Server, der auf ankommende Verbindungen lauscht und Nachrichten in Echtzeit an die verbundenen Clients weiterleitet.  
Akzuell findet hier keine Verarbeitung der Daten statt. Sinnvoll wäre aber eine Erfassung der daten in einer Datenbank, um bei Verbindungsproblemen trotzdem über einen Datenbestand zur Weiterverarbetung zu verfügen. Alternativ könnten die Daten aber auch auf den Clients in einer Frontendanwendung gespeichert werden.
Hier ist eine Beschreibung des Programms:
##### Importieren von Modulen:
- asyncio: Ein Framework, das es ermöglicht, asynchrone und parallele Codeausführung in Python zu implementieren.
- websockets: Eine Bibliothek, die eine asynchrone Schnittstelle für WebSocket-Kommunikation bereitstellt.
##### Initialisierung des WebSocket-Servers:
Das Skript initialisiert einen WebSocket-Server, der auf allen verfügbaren Netzwerkschnittstellen ('0.0.0.0') auf Port 8765 lauscht. Aktuell sind noch keinerlei Sicherheitsaspekte berücksichtigt. Eine Authentifizierung sollte mindestens noch eingebaut werden. Auch eine VPN-Verbindung wäre sinnvol.
##### Behandlung eingehender Verbindungen:
Die Funktion server(websocket, path) wird aufgerufen, wenn ein neuer Client eine WebSocket-Verbindung zum Server herstellt.
Der Server empfängt und sendet Nachrichten in einem asynchronen Kontext.
##### Verwaltung aktiver Verbindungen:
- Eine Liste namens connected_clients wird erstellt, um alle aktiven WebSocket-Verbindungen zu speichern.
- Wenn ein Client sich verbindet, wird seine WebSocket-Verbindung zur connected_clients-Liste hinzugefügt.
- Wenn eine Nachricht empfangen wird, wird die Nachricht an alle Clients in der connected_clients-Liste weitergeleitet.
- Wenn eine Verbindung geschlossen wird, wird sie aus der Liste entfernt.
Auch bei der Verbindung vom Client zum Server sind noch keine Sicherheitsaspekte berücksichtigt.
##### Serverstart und Endlosschleife:
- Der WebSocket-Server wird gestartet, indem die Funktion websockets.serve() aufgerufen wird.
- Die Ausführung des Servers wird mit asyncio.get_event_loop().run_until_complete() und asyncio.get_event_loop().run_forever() gesteuert.
- Der Server bleibt in einer Endlosschleife und wartet auf eingehende Verbindungen.
### index.html
/var/www/html/index.html
HTML-WebSocket-Datenanzeige:  
Dieses HTML-Dokument dient als WebSocket-Client, der sich mit einem WebSocket-Server verbindet, um empfangene Daten anzuzeigen. Dieses HTML-Skript ermöglicht es einem Benutzer, Daten in Echtzeit von einem WebSocket-Server zu empfangen und anzuzeigen, was besonders nützlich ist, wenn Echtzeitaktualisierungen von Serverdaten benötigt werden. Es bietet eine einfache Möglichkeit, WebSocket-Kommunikation in Webanwendungen zu integrieren und mit dem Server zu interagieren.  
Hier wird später die Logik, wie sie z.B. beim Sprecher-PC vorhanden ist, integriert.  
Außerdem erfolgt hier die Aufbereitung und Gestaltung der Daten, wie sie als Overlay für einen Livestream benötigt werden.  
##### HTML-Struktur:
Das Dokument enthält ein div-Element mit der ID data-container, die dazu verwendet wird, die empfangenen Daten anzuzeigen.
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
