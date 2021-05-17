import pandas
import numpy as np
import plotly.graph_objects as pg

CSV_PATH = r".\wig20.csv"
RANGE = 1000

class MACD:
    def __init__(self, csv, n):
        self.data = []
        self.MACD = []
        self.SIGNAL = []
        self.csvToVector(csv, n)
        self.calculate(self.data)

    def calculate(self, input):
        self.MACD.clear()
        for i in range(len(input)):
            if not i - 26 < 0:
                self.MACD.append(self.ema(12, input, i) - self.ema(26, input, i))
            else:
                self.MACD.append(0.0)

        self.SIGNAL.clear()
        for i in range(len(input)):
            if not i - 9 < 0:
                self.SIGNAL.append(self.ema(9, self.MACD, i))
            else:
                self.SIGNAL.append(0.0)

    def csvToVector(self, csv, n):
        self.data.clear()
        for i in range(n):
            self.data.append((float(csv["Najnizszy"][i]) + float(csv["Najwyzszy"][i])) / 2)

    def ema(self, n, inp, p0):
        numerator = inp[p0]
        denominator = 1
        alpha = 1 - (2 / (n + 1))
        factor = 1
        for i in range(1, n + 1):
            factor *= alpha
            if p0 - i >= 0:
                numerator += inp[p0 - i] * factor
                denominator += factor
            else:
                break;
        return numerator / denominator

def simulate(macd, capital):
    quantity = 0
    for i in range(1, len(macd.MACD)):
        if macd.MACD[i] < macd.SIGNAL[i] and macd.MACD[i - 1] >= macd.SIGNAL[i - 1] and quantity != 0:
            capital = quantity * macd.data[i]
            quantity = 0;
        elif macd.MACD[i] > macd.SIGNAL[i]  and macd.MACD[i - 1] <= macd.SIGNAL[i - 1] and capital != 0:
            quantity = capital / macd.data[i]
            capital = 0;
    if capital == 0:
        capital = quantity * macd.data[i]
    return capital

csv = pandas.read_csv(CSV_PATH)
macd_ind = MACD(csv, RANGE)
x = np.arange(len(macd_ind.data))

fig = pg.Figure()
fig.add_trace(pg.Scatter(x=x, y=macd_ind.MACD, name='MACD', line=dict(color='firebrick', width=2)))
fig.add_trace(pg.Scatter(x=x, y=macd_ind.SIGNAL, name='SIGNAL', line=dict(color='royalblue', width=2)))
fig.update_layout(
    title="Wykres wskaźnika MACD",
    xaxis_title="Dni od daty początkowej",
    yaxis_title="Cena",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
fig.show()

fig2 = pg.Figure()
fig2.add_trace(pg.Scatter(x=x, y=macd_ind.data, name='cena', line=dict(color='brown', width=2)))
fig2.update_layout(
    title="Notowania",
    xaxis_title="Dni od daty początkowej",
    yaxis_title="Kurs",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
fig2.show()

print("SYMULACJA\n\nPoczątkowy kapitał: 1000\nKońcowy kapitał: ", simulate(macd_ind, 1000))