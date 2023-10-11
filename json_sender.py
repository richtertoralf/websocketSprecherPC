import json
import websocket
from datetime import datetime

# Aktuelle Uhrzeit als Zeichenfolge im Format "Jahr-Monat-Tag Stunde:Minute:Sekunde"
aktuelle_uhrzeit = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

data = {
  "Wettkampf-ID": "20230929_0001",
  "Wettkampf-Name": "Oberhofer Skihallensprint 2023",
  "Kategorie-ID": "categoryId",
  "Kategorie-Name": "Schülerinnen U12",
  "gesendet": aktuelle_uhrzeit,
  "Live-Ergebnisse": [
    {
      "Rang": 1,
      "Startnummer": 17,
      "Laufzeit": "3:34:56.8",
      "Rückstand": "0:00:00.0"
    },
    {
      "Rang": 2,
      "Startnummer": 16,
      "Laufzeit": "3:35:20.6",
      "Rückstand": "0:00:23.8"
    },
    {
      "Rang": 3,
      "Startnummer": 15,
      "Laufzeit": "3:35:42.9",
      "Rückstand": "0:00:46.1"
    },
    {
      "Rang": 4,
      "Startnummer": 14,
      "Laufzeit": "3:35:59.5",
      "Rückstand": "0:01:02.7"
    },
    {
      "Rang": 5,
      "Startnummer": 18,
      "Laufzeit": "4:45:17.4",
      "Rückstand": "1:10:20.6"
    }
  ]
}

ws = websocket.WebSocket()
ws.connect("ws://192.168.178.102:8765")  # IP-Adresse des Ubuntu-Servers

json_data = json.dumps(data)
ws.send(json_data)

ws.close()
