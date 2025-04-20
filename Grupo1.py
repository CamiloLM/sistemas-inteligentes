from itertools import permutations
from random import choice


class AgentePicasFijas:
    def __init__(self):
        self.secret_number = None
        self.guess = None
        self.picas = 0
        self.fijas = 0
        self.posibilities = [
            "".join(map(str, perm)) for perm in permutations("0123456789", 4)
        ]

    def generate_number(self):
        return choice(self.posibilities)

    def count_picas_fijas(self, guess):
        picas = sum(
            1
            for i in range(4)
            if guess[i] in self.secret_number and guess[i] != self.secret_number[i]
        )
        fijas = sum(1 for i in range(4) if guess[i] == self.secret_number[i])
        return picas, fijas

    def compute(self, percepcion):
        if percepcion == "B" or percepcion == "N":
            # Crea su numero secreto
            self.secret_number = self.generate_number()
            # Crea su intento
            self.guess = self.generate_number()
            self.posibilities.remove(self.guess)
            return "L"

        elif percepcion == "L":
            return self.guess

        elif "," in percepcion:
            self.picas, self.fijas = map(int, percepcion.split(","))

            if self.fijas != 4:
                self.guess = self.generate_number()
            return "L"

        elif percepcion.isdigit():
            picas, fijas = self.count_picas_fijas(percepcion)
            return f"{picas},{fijas}"

    def reset_game(self):
        self.__init__(self)


class Environment:
    def __init__(self, blanco, negro):
        self.blanco = blanco
        self.negro = negro
        self.turno = "B"
        self.winner = None

    def start(self):
        # Verifica que los dos agentes esten listos para jugar
        if self.blanco.compute("B") == "L" and self.negro.compute("N") == "L":
            print("El juego ha iniciado")
            while self.winner is None:
                # Juega los turnos del agente blanco y negro
                if self.turno == "B":
                    print("Turno de blanco")
                    guess = self.blanco.compute("L")
                    print(f"Blanco adivina: {guess}")
                    picas_fijas = self.negro.compute(guess)
                    print(f"Negro responde: {picas_fijas}")
                    if picas_fijas == "0,4":
                        self.winner = "B"
                    self.negro.compute(picas_fijas)
                    self.turno = "N"
                else:
                    print("Turno de Negro")
                    guess = self.negro.compute("L")
                    print(f"Negro adivina: {guess}")
                    picas_fijas = self.blanco.compute(guess)
                    print(f"Blanco responde: {picas_fijas}")
                    if picas_fijas == "0,4":
                        self.winner = "N"
                    self.blanco.compute(picas_fijas)
                    self.turno = "B"
        else:
            print("Hay un error el juego no puede comenzar")

    def get_winner(self):
        if self.winner == "B":
            print("El ganador es el Blanco")
        elif self.winner == "N":
            print("El ganador es el Negro")
        else:
            print("Hay un error")


if __name__ == "__main__":
    agente_1 = AgentePicasFijas()
    agente_2 = AgentePicasFijas()
    print("=" * 50)
    print("Primer juego: Agente 1 con Blancas")
    game_1 = Environment(agente_1, agente_2)
    game_1.start()
    game_1.get_winner()
    print("=" * 50)
    print("Segundo juego: Agente 2 con Blancas")
    agente_1.reset_game()
    agente_2.reset_game()
    game_2 = Environment(agente_2, agente_1)
    game_2.start()
    game_2.get_winner()
