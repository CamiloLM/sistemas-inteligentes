from random import sample


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
            self.secret = "".join(sample("0123456789", 4))
            self.last = self.init()
        elif is_valid(percept):
            picas = calculate_picas(percept, self.secret)
            fijas = calculate_fijas(percept, self.secret)
            return {"picas": picas, "fijas": fijas}
        else:
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
        txt = ""
        for i in range(4):
            txt += str(self.last[i])
        return txt


class Environment:
    def __init__(self, white, black):
        self.white = white
        self.black = black

    def iniciar(self):
        white_guess = self.white.compute("iniciar")
        black_guess = self.black.compute("iniciar")
        white_turn = True
        while True:
            if white_turn:
                picas_fijas = self.black.compute(white_guess)
                print(f"\nBlanco adivina: {white_guess}")
                print(f"Picas: {picas_fijas['picas']} Fijas: {picas_fijas['fijas']}")
                if picas_fijas["fijas"] == 4:
                    print("\nEl ganador es el jugador blanco")
                    break
                white_guess = self.white.compute(picas_fijas)
            else:
                picas_fijas = self.white.compute(black_guess)
                print(f"\nNegro adivina: {black_guess}")
                print(f"Picas: {picas_fijas['picas']} Fijas: {picas_fijas['fijas']}")
                if picas_fijas["fijas"] == 4:
                    print("\nEl ganador es el jugador negro")
                    break
                black_guess = self.black.compute(picas_fijas)
            white_turn = not white_turn


if __name__ == "__main__":
    a1 = Agent()
    a2 = Agent()
    env = Environment(a1, a2)
    env.iniciar()

