from random import choice, sample, shuffle


class AgentePicasFijas:
    def __init__(self):
        self.secret_number = None
        self.guess = None
        self.picas = 0
        self.fijas = 0
        self.historial = []
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.confirmed = []

    def generate_number(self):
        return "".join(sample(self.numbers, 4))

    def count_picas_fijas(self, guess, aim=None):
        aim = aim or self.secret_number
        picas = sum(1 for i in range(4) if guess[i] in aim and guess[i] != aim[i])
        fijas = sum(1 for i in range(4) if guess[i] == aim[i])
        return picas, fijas

    def remplace_one_number(self):
        guess_list = list(self.guess)

        replace = choice([num for num in self.numbers if num not in guess_list])

        for i in range(4):
            if guess_list[i] not in self.confirmed:
                guess_list[i] = replace
                break

        return "".join(guess_list)

    def swap_index(self, i, j):
        guess_list = list(self.guess)
        guess_list[i], guess_list[j] = guess_list[j], guess_list[i]
        return "".join(guess_list)

    def confirm_numer(self, number):
        if number not in self.confirmed:
            self.confirmed.append(number)

    def compute(self, percepcion):
        if percepcion == "B" or percepcion == "N":
            # Crea su numero secreto
            self.secret_number = self.generate_number()
            # Crea su intento inicial
            self.guess = self.generate_number()
            return "L"

        elif percepcion == "L":
            return self.guess

        elif "," in percepcion:
            self.picas, self.fijas = map(int, percepcion.split(","))
            self.historial.append((self.guess, (self.picas, self.fijas)))

            # Caso 1: Ninguno de los digitos adivinados estan en el número
            if self.picas + self.fijas == 0:
                self.numbers = [num for num in self.numbers if num not in self.guess]
                self.guess = self.generate_number()

            # Caso 2: Se hace una adivinanza mediocre
            elif self.picas + self.fijas <= 2:
                # Tomo al azar dos digitos del intento
                old_part = sample(list(self.guess), 2)
                # Tomo al azar dos digitos no probados
                available = [d for d in self.numbers if d not in old_part]
                new_part = sample(available, 2)
                # Creo un nuevo intento que deberia ser mejor
                new_guess = old_part + new_part
                shuffle(new_guess)
                self.guess = "".join(new_guess)

            # Caso 3: Falta un digito correcto
            elif self.picas + self.fijas == 3:
                if len(self.historial) > 1:
                    last_guess = self.historial[-2][0]
                    last_total = self.historial[-2][1][0] + self.historial[-2][1][1]
                    new_total = self.picas + self.fijas

                    for i in range(4):
                        if last_guess[i] != self.guess[i]:
                            break
                    if new_total > last_total:
                        self.confirm_numer(self.guess[i])
                        self.numbers.remove(last_guess[i])
                    elif new_total < last_total:
                        self.confirm_numer(last_guess[i])
                        self.numbers.remove(self.guess[i])
                        self.historial.pop()
                        self.guess = last_guess
                self.guess = self.remplace_one_number()

            # Caso 4: Los digitos no estan ordenados
            elif self.picas + self.fijas == 4 and self.fijas != 4:
                print("here")
                if len(self.historial) == 1:
                    i, j = sample(range(4), 2)
                    self.guess = self.swap_index(i, j)
                else:
                    last_guess = self.historial[-2][0]
                    last_fijas = self.historial[-2][1][1]

                    if self.fijas > last_fijas:
                        # Si las fijas mejoraron, conservamos esta versión y probamos otro intercambio
                        i, j = sample(range(4), 2)
                        self.guess = self.swap_index(i, j)
                    else:
                        # Si las fijas empeoraron, volvemos al intento anterior y probamos otro swap distinto
                        self.historial.pop()
                        self.guess = last_guess
                        i, j = sample(range(4), 2)
                        self.guess = self.swap_index(i, j)
            return "L"

        elif percepcion.isdigit():
            picas, fijas = self.count_picas_fijas(percepcion)
            return f"{picas},{fijas}"

    def reset_game(self):
        self.__init__()


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
                print()
                # Juega los turnos del agente blanco y negro
                if self.turno == "B":
                    print("Turno de blanco")
                    guess = self.blanco.compute("L")
                    print(f"Blanco adivina: {guess}")
                    picas_fijas = self.negro.compute(guess)
                    print(f"Negro responde: {picas_fijas}")
                    if picas_fijas == "0,4":
                        self.winner = "B"
                    self.blanco.compute(picas_fijas)
                    # self.turno = "N"
                else:
                    print("Turno de Negro")
                    guess = self.negro.compute("L")
                    print(f"Negro adivina: {guess}")
                    picas_fijas = self.blanco.compute(guess)
                    print(f"Blanco responde: {picas_fijas}")
                    if picas_fijas == "0,4":
                        self.winner = "N"
                    self.negro.compute(picas_fijas)
                    self.turno = "B"
        else:
            print("Hay un error el juego no puede comenzar")

    def get_winner(self):
        if self.winner == "B":
            print("El ganador es el Blanco")
        elif self.winner == "N":
            print("El ganador es el Negro")
        else:
            print("No hay un ganador")


if __name__ == "__main__":
    agente_1 = AgentePicasFijas()
    agente_2 = AgentePicasFijas()
    print("=" * 50)
    print("Primer juego: Agente 1 con Blancas")
    game_1 = Environment(agente_1, agente_2)
    game_1.start()
    game_1.get_winner()
    # print("=" * 50)
    # print("Segundo juego: Agente 2 con Blancas")
    # agente_1.reset_game()
    # agente_2.reset_game()
    # game_2 = Environment(agente_2, agente_1)
    # game_2.start()
    # game_2.get_winner()
