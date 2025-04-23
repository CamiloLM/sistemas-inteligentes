from random import choice, sample, shuffle

class AgentePicasFijas:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.secret_number = None
        self.guess = None
        self.picas = 0
        self.fijas = 0
        self.historial = []
        self.numbers = set("0123456789")
        self.confirmed = []
        self.confirmed_pos = [None] * 4
        self.turn_count = 0

    def generate_number(self):
        if len(self.numbers) >= 4:
            return "".join(sample(list(self.numbers), 4))
        must = list(self.confirmed)
        needed = 4 - len(must)
        pool = set("0123456789") - set(must)
        extras = sample(list(pool), needed)
        new_guess = must + extras
        shuffle(new_guess)
        return "".join(new_guess)

    def count_picas_fijas(self, guess, aim=None):
        aim = aim or self.secret_number
        p = sum(1 for i in range(4) if guess[i] in aim and guess[i] != aim[i])
        f = sum(1 for i in range(4) if guess[i] == aim[i])
        return p, f

    def generate_next_guess(self):
        known_digits = [d for d in self.confirmed if d not in self.confirmed_pos]
        rest = list(self.numbers - set(known_digits))
        needed = 4 - len(self.confirmed)
        extra = sample(rest, needed)
        guess = self.confirmed + extra
        shuffle(guess)
        return "".join(guess)

    def compute(self, percepcion: str) -> str:
        if percepcion == 'L':
            self.turn_count += 1

        if percepcion == "B" or percepcion == "N":
            self.reset_game()
            self.secret_number = self.generate_number()
            self.guess = self.generate_number()
            return "L"

        if percepcion == "L":
            return self.guess

        if percepcion.isdigit() and len(percepcion) == 4:
            p, f = self.count_picas_fijas(percepcion)
            return f"{p},{f}"

        if "," in percepcion:
            p, f = map(int, percepcion.split(","))
            self.historial.append((self.guess, (p, f)))
            total = p + f

            if total == 0:
                self.numbers -= set(self.guess)
                self.guess = self.generate_number()

            elif total == 1:
                candidates = []
                for i in range(4):
                    trial = list(self.guess)
                    trial[i] = choice(list(self.numbers - set(self.guess)))
                    trial_str = "".join(trial)
                    p2, f2 = self.count_picas_fijas(trial_str)
                    if p2 + f2 < total:
                        candidates.append(self.guess[i])
                if candidates:
                    self.confirmed.append(candidates[0])
                self.guess = self.generate_number()

            elif total == 2:
                for i in range(4):
                    trial = list(self.guess)
                    original = trial[i]
                    trial[i] = choice(list(self.numbers - set(trial)))
                    trial_str = "".join(trial)
                    p2, f2 = self.count_picas_fijas(trial_str)
                    if p2 + f2 < total:
                        self.confirmed.append(original)
                        break
                self.guess = self.generate_number()

            elif total == 3:
                for i in range(4):
                    trial = list(self.guess)
                    original = trial[i]
                    trial[i] = choice(list(self.numbers - set(trial)))
                    trial_str = "".join(trial)
                    p2, f2 = self.count_picas_fijas(trial_str)
                    if p2 + f2 < total:
                        self.confirmed.append(original)
                        break
                self.guess = self.generate_number()

            elif total == 4:
                self.guess = self.generate_number()
                p, f = self.count_picas_fijas(self.guess)
                if f == 4:
                    return ""  # found

            return "L"
        return ""


class Environment:
    def __init__(self, blanco, negro, games=1):
        self.blanco = blanco
        self.negro = negro
        self.games = games

    def start(self):
        for g in range(1, self.games + 1):
            print(f"\nJuego {g}:")
            self.blanco.compute("B")
            self.negro.compute("N")
            print("El juego ha iniciado")
            turno = "B"
            winner = None
            while not winner:
                if turno == "B":
                    guess = self.blanco.compute("L")
                    feedback = self.negro.compute(guess)
                    if feedback == "0,4":
                        winner = "Blanco"
                    self.blanco.compute(feedback)
                    turno = "N"
                else:
                    guess = self.negro.compute("L")
                    feedback = self.blanco.compute(guess)
                    if feedback == "0,4":
                        winner = "Negro"
                    self.negro.compute(feedback)
                    turno = "B"
            print(f"Ganador: {winner} en {self.blanco.turn_count + self.negro.turn_count} turnos")


if __name__ == "__main__":
    games = int(input("Número de juegos a simular: "))
    a1 = AgentePicasFijas()
    a2 = AgentePicasFijas()
    env = Environment(a1, a2, games=games)
    env.start()
