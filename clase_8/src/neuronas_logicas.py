class ORNeuron:
    _or = [
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 1),
    ]
    def __init__(self, w1, w2, b, learning_rate=0.1):
        self.w1 = w1
        self.w2 = w2
        self.b = b
        self.learning_rate = learning_rate

    def escalon(self, z):
        """Función de activación escalón."""
        return 1 if z >= 0 else 0

    def neuron(self, x1, x2):
        """Calcula la salida de la neurona para la compuerta OR."""
        z = self.w1 * x1 + self.w2 * x2 + self.b
        return self.escalon(z)

    def learn(self):
        print("Entrenando la neurona para compuerta OR...")
        for epoca in range(10):
            error_total = 0
            print(f"--- Época {epoca + 1} ---")
            for x1, x2, y_real in self._or:
                y_pred = self.neuron(x1, x2)
                error = y_real - y_pred
                error_total += abs(error)

                self.w1 += self.learning_rate * error * x1
                self.w2 += self.learning_rate * error * x2
                self.b += self.learning_rate * error

                print(f" Entrada: ({x1}, {x2}) | Real: {y_real} | Pred: {y_pred} | Error: {error}")
            print(f" Error total: {error_total}")
            print(f" Parámetros actuales: w1={self.w1:.3f}, w2={self.w2:.3f}, b={self.b:.3f}\n")

            if error_total == 0:
                print(f"Entrenamiento completo. No hay errores, la neurona aprendió en {epoca + 1} épocas.")
                break


class NotNeuron:
    _not =[
        (0, 1),
        (1, 0),
    ]
    def __init__(self, w1, b, learning_rate=0.1):
        self.w1 = w1
        self.b = b
        self.learning_rate = learning_rate

    def escalon(self, z):
        """Función de activación escalón."""
        return 1 if z >= 0 else 0

    def neuron(self, x):
        """Calcula la salida de la neurona para la compuerta NOT."""
        z = self.w1 * x + self.b
        return self.escalon(z)

    def learn(self):
        print("Entrenando la neurona para compuerta NOT...")
        for epoca in range(20):
            error_total = 0
            print(f"--- Época {epoca + 1} ---")
            for x, y_real in self._not:

                y_pred = self.neuron(x)
                error = y_real - y_pred
                error_total += abs(error)

                self.w1 += self.learning_rate * error * x
                self.b += self.learning_rate * error

                print(f" Entrada: ({x}) | Real: {y_real} | Pred: {y_pred} | Error: {error}")
            print(f" Error total: {error_total}")
            print(f" Parámetros actuales: w1={self.w1:.3f}, b={self.b:.3f}\n")

            if error_total == 0:
                print(f"Entrenamiento completo. No hay errores, la neurona aprendió en {epoca + 1},epocas.")
                break

class OrNeuronTest:
    def test(self, neuron: ORNeuron):
        print("--- Probando neurona para compuerta OR ---")
        for x1, x2, y_real in neuron._or:
            y_pred = neuron.neuron(x1, x2)
            estado = "OK" if y_pred == y_real else "X"
            print(f" {estado} Entrada: ({x1}, {x2}) | Esperado: {y_real} | Predicho: {y_pred}")

class NotNeuronTest:
    def test(self, neuron: NotNeuron):
        print("--- Probando neurona para compuerta NOT ---")
        for x, y_real in neuron._not:
            y_pred = neuron.neuron(x)
            estado = "OK" if y_pred == y_real else "X"
            print(f" {estado} Entrada: ({x}) | Esperado: {y_real} | Predicho: {y_pred}")

def main():
    w1 = 0.5
    w2 = 0.5
    b = -0.7
    tasa_aprendizaje = 0.1
    not_neuron = NotNeuron(w1, b, tasa_aprendizaje)
    or_neuron = ORNeuron(w1, w2, b, tasa_aprendizaje)
    not_neuron.learn()
    or_neuron.learn()

    or_neuron_test = OrNeuronTest()
    or_neuron_test.test(or_neuron)

    not_neuron_test = NotNeuronTest()
    not_neuron_test.test(not_neuron)

if __name__ == "__main__":
    main()
