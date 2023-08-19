import sys
import requests
import matplotlib.pyplot as plt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CryptoGraphApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qua Kripto")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        coin_buttons = ["bitcoin", "ethereum", "binancecoin", "cardano", "solana", "ripple", "polkadot", "dogecoin", "avalanche", "chainlink"]
        self.coin_buttons = []

        for coin_symbol in coin_buttons:
            button = QPushButton(coin_symbol.capitalize())
            button.clicked.connect(lambda _, coin=coin_symbol: self.show_graph(coin))
            self.coin_buttons.append(button)
            self.layout.addWidget(button)

        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(10000)  # 10 seconds interval

        self.current_coin = "bitcoin"
        self.update_graph()

    def fetch_crypto_data(self, symbol):
        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days=1"
        response = requests.get(url)
        data = response.json()
        prices = [(entry[0], entry[1]) for entry in data['prices']]
        return prices

    def show_graph(self, coin_symbol):
        self.current_coin = coin_symbol
        self.update_graph()

    def update_graph(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.set_title(f"{self.current_coin.capitalize()} Grafiği (Son 24 Saat)")
        ax.set_xlabel("Saat")
        ax.set_ylabel("Miktar (USD)")

        prices = self.fetch_crypto_data(self.current_coin)
        timestamps, values = zip(*prices)
        ax.plot(timestamps, values, label=f"{self.current_coin.capitalize()} Ücreti")
        ax.legend()

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoGraphApp()
    window.show()
    sys.exit(app.exec_())
