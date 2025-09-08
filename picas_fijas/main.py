import numpy as np
import random

def calculate_picas(n1, n2):
    P = 0
    for i in range(4):
        for j in range(4):
            if i != j:
                if n1[i] == n2[j]:
                    P += 1
    return P


def calculate_fijas(n1, n2):
    F = 0
    for i in range(4):
        if n1[i] == n2[i]:
            F += 1
    return F


def is_valid(number):
    return len(number) == 4 and number.isdigit() and len(set(number)) == 4


class Agent:
    def __init__(self):
        self.options = []
        self.last = None
        self.secret = None

    def ask(self):
        return self.options[len(self.options) // 2]

    def init(self):
        self.option = []
        for i in range(10):
            for j in range(10):
                if j != i:
                    for k in range(10):
                        if k != i and k != j:
                            for l in range(10):
                                if l != i and l != j and l != k:
                                    self.options.append([i, j, k, l])
        return self.ask()

    def compute(self, percept):
        if percept == "iniciar":
            self.secret = "".join(random.sample("0123456789", 4))
            self.last = self.init()
        elif isinstance(percept, str) and is_valid(percept):
            picas = calculate_picas(percept, self.secret)
            fijas = calculate_fijas(percept, self.secret)
            return {"picas": picas, "fijas": fijas}
        elif isinstance(percept, dict) and "picas" in percept and "fijas" in percept:
            F = percept["fijas"]
            if F == 4:
                return "Soy un dios en picas y fijas"
            P = percept["picas"]
            opt = []
            for i in range(len(self.options)):
                P2 = calculate_picas(self.last, self.options[i])
                F2 = calculate_fijas(self.last, self.options[i])
                if P == P2 and F == F2:
                    opt.append(self.options[i])
            self.options = opt
            if len(self.options) == 0:
                return "Usuario tramposo no me diste la información correcta. Humano tenia que ser"
            self.last = self.ask()
        else:
            raise ValueError("Mensaje inválido para el Agente")
        txt = ""
        for i in range(4):
            txt += str(self.last[i])
        return txt

class AgentV2:
    def __init__(self, tabla_file="tabla.npy"):
        self.candidates = []
        for i in range(10):
            for j in range(10):
                if j != i:
                    for k in range(10):
                        if k != i and k != j:
                            for l in range(10):
                                if l != i and l != j and l != k:
                                    self.candidates.append(f"{i}{j}{k}{l}")

        # Cargar la tabla precalculada
        self.table = np.load(tabla_file)

        # Mapa de indices
        self.idx_map = {c: i for i, c in enumerate(self.candidates)}

        self.options = self.candidates.copy()
        self.last = None
        self.secret = None

    def lookup(self, guess, secret):
        gi, si = self.idx_map[guess], self.idx_map[secret]
        return tuple(self.table[gi, si])

    def best_guess(self):
        """Devuelve el intento que minimiza el peor caso"""
        best = None
        best_score = float("inf")

        for guess in self.options:
            partitions = {}
            gi = self.idx_map[guess]

            for secret in self.options:
                si = self.idx_map[secret]
                p, f = self.table[gi, si]
                partitions[(p, f)] = partitions.get((p, f), 0) + 1

            worst_case = max(partitions.values())
            if worst_case < best_score:
                best_score = worst_case
                best = guess

        return best, best_score

    def compute(self, percept):
        if percept == "iniciar":
            self.secret = "".join(random.sample("0123456789", 4))
            self.last = "0123"
            return self.last

        elif isinstance(percept, str) and is_valid(percept):
            p, f = self.lookup(percept, self.secret)
            return {"picas": p, "fijas": f}

        elif isinstance(percept, dict) and "picas" in percept and "fijas" in percept:
            p, f = percept["picas"], percept["fijas"]

            # Filtrar candidatos que generen las mismas picas y fijas
            self.options = [c for c in self.options if self.lookup(self.last, c) == (p, f)]

            if len(self.options) == 0:
                raise ValueError("Usuario tramposo no me diste la información correcta.")

            if len(self.options) == 1:
                self.last = self.options[0]
                return self.last

            # Busca la mejor suposición usando minimax
            guess, _ = self.best_guess()
            self.last = guess
            return guess

        else:
            raise ValueError("Mensaje inválido para el Agente")



class Environment:
    def __init__(self, agt1, agt2):
        self.white = agt1
        self.black = agt2
        self.turn = 1
        self.ganador = None

    def iniciar(self):
        white_guess = self.white.compute("iniciar")
        black_guess = self.black.compute("iniciar")

        while True:
            print(f"\n--- Turno {self.turn} ---")

            # Juega blanco
            picas_fijas = self.black.compute(white_guess)
            print(f"\nBlanco adivina: {white_guess}")
            print(f"Picas: {picas_fijas['picas']} Fijas: {picas_fijas['fijas']}")
            if picas_fijas["fijas"] == 4:
                self.ganador = self.white
                break
            white_guess = self.white.compute(picas_fijas)

            # Juega negro
            picas_fijas = self.white.compute(black_guess)
            print(f"\nNegro adivina: {black_guess}")
            print(f"Picas: {picas_fijas['picas']} Fijas: {picas_fijas['fijas']}")
            if picas_fijas["fijas"] == 4:
                self.ganador = self.black
                break
            black_guess = self.black.compute(picas_fijas)

            self.turn += 1

        print("\n--- RESULTADO FINAL ---")
        print(f"Ganador: {self.ganador.__class__.__name__}")
        print(f"Secreto de {self.white.__class__.__name__}: {self.white.secret}")
        print(f"Secreto de {self.black.__class__.__name__}: {self.black.secret}")



if __name__ == "__main__":
    a1 = Agent()
    a2 = AgentV2()
    env = Environment(a1, a2)
    env.iniciar()

