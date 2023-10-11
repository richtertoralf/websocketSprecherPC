import asyncio
import websockets

# Liste, um aktive WebSocket-Verbindungen zu speichern
connected_clients = []

async def server(websocket, path):
    print("Ein Client hat sich verbunden")

    try:
        # Fügen Sie die aktuelle Verbindung zur Liste hinzu
        connected_clients.append(websocket)

        async for message in websocket:
            print(f"Empfangene Daten: {message}")
            # Hier können Sie die empfangenen Daten nach Belieben verarbeiten

            # Nachricht an alle Clients senden
            for client in connected_clients:
                if client.open:
                    await client.send(message)
    except Exception as e:
        print(f"Fehler beim Handhaben der Verbindung: {e}")
    finally:
        print("Verbindung geschlossen")
        # Entfernen Sie die Verbindung aus der Liste, wenn sie geschlossen wird
        connected_clients.remove(websocket)

start_server = websockets.serve(server, '0.0.0.0', 8765)  # 0.0.0.0 bedeutet, dass der Server auf allen verfügbaren Schnittstellen lauscht

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
