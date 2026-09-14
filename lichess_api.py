import requests
import json

class MotorLichess:
    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}
        self.game_id = None

    def retar_bot(self, fen, nivel=3):
        url = "https://lichess.org/api/challenge/ai"
        datos = {"level": nivel, "color": "white", "fen": fen}
        
        respuesta = requests.post(url, headers=self.headers, data=datos)
        if respuesta.status_code == 201:
            self.game_id = respuesta.json()["id"]
            return True
        return False

    def hacer_jugada(self, origen, destino):
        jugada_uci = f"{origen}{destino}"
        url = f"https://lichess.org/api/board/game/{self.game_id}/move/{jugada_uci}"
        requests.post(url, headers=self.headers)

    def esperar_respuesta_bot(self):
        url = f"https://lichess.org/api/board/game/stream/{self.game_id}"
        respuesta = requests.get(url, headers=self.headers, stream=True)
        
        for linea in respuesta.iter_lines():
            if linea:
                evento = json.loads(linea.decode('utf-8'))
                if evento.get("type") == "gameState":
                    movimientos = evento["moves"].split()
                    return movimientos[-1]
