from scapy.all import *
import re
import json
import websocket

def clean_data(data):
    # Entferne Leerzeichen und nicht-ASCII-Zeichen
    cleaned_data = re.sub(r'\s+|[^\x00-\x7F]+', '', data)
    return cleaned_data

def parse_data(data):
    cleaned_data = clean_data(data)
    pattern = r'#t(\d+)t(\d+)t(.*?)t(\d+:\d{1,2}:\d{1,2}\.\d+)t(\d+:\d{1,2}:\d{1,2}\.\d+)'
    matches = re.findall(pattern, cleaned_data)
    parsed_data = []
    for idx, match in enumerate(matches, start=1):
        rank, start_number, name, runtime, delay = match
        parsed_data.append({
            # "Datensatz": idx,
            "Rang": rank,
            "Startnummer": start_number,
            "Name": name,
            "Laufzeit": runtime,
            "Rückstand": delay
        })
    return parsed_data

def correct_names(parsed_data):
    for data in parsed_data:
        # Schneide alles ab dem Zeichen ~ ab, wenn es vorkommt
        if '~' in data['Name']:
            data['Name'] = data['Name'].split('~')[0]
        # Füge zwischen vorkommenden Großbuchstaben und Kleinbuchstaben Leerzeichen ein
        data['Name'] = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', data['Name'])
        # Entferne das 'q' am Ende des Namens
        data['Name'] = data['Name'].rstrip('q')
    return parsed_data


def packet_callback(packet):
    if IP in packet and packet[IP].src == '192.168.100.10' and packet[IP].dst == '192.168.100.20' and TCP in packet and packet[TCP].flags & 0x08:
        raw_data = bytes(packet[TCP].payload)  # Rohdaten als Bytes erhalten
        
        # Konvertiere Bytes in ein Hex-Format
        hex_data = raw_data.hex()

        try:
            ascii_text = bytes.fromhex(hex_data).decode('utf-8', errors='ignore')
            winlaufen_data = ''.join([char for char in ascii_text if char.isprintable() and ord(char) < 128])
            print(winlaufen_data)
            parsed_data = parse_data(winlaufen_data)
            corrected_data = correct_names(parsed_data)

            for data in corrected_data:
                # print(f"Datensatz {data['Datensatz']}:")
                print(f"Rang: {data['Rang']}")
                print(f"Startnummer: {data['Startnummer']}")
                print(f"Name: {data['Name']}")
                print(f"Laufzeit: {data['Laufzeit']}")
                print(f"Rückstand: {data['Rückstand']}")
                print()

            print(parsed_data)

             # Speichern des Arrays in einer Datei namens "parsed_data.json"
            with open('parsed_data.json', 'w') as json_file:
                json.dump(parsed_data, json_file)

            # WebSocket-Verbindung öffnen und Daten senden
            ws = websocket.WebSocket()
            try:
                ws.connect("ws://192.168.10.211:8765")
                json_data = json.dumps(parsed_data)
                ws.send(json_data)
            except Exception as e:
                print(f"Fehler bei der WebSocket-Verbindung: {e}")
            finally:
                ws.close()

        except UnicodeDecodeError as e:
            print(f"Fehler beim Decodieren des Pakets: {e}")
            pass  # Wenn ein Fehler auftritt, ignoriere diesen Paket

# Erfasse eingehenden Verkehr auf einer bestimmten Schnittstelle (z.B. "Ethernet")
sniff(iface="Ethernet", prn=packet_callback, store=0)
