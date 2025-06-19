import websocket
import json
import time
import random

class DerivBot:
    def __init__(self, token, strategy, stake, martingale_factor, max_consecutive_losses, max_loss, target_profit):
        self.token = token
        self.strategy = strategy
        self.stake = float(stake)
        self.initial_stake = float(stake)
        self.martingale_factor = float(martingale_factor)
        self.max_consecutive_losses = int(max_consecutive_losses)
        self.max_loss = float(max_loss)
        self.target_profit = float(target_profit)
        self.consecutive_losses = 0
        self.total_profit = 0.0
        self.current_contract_id = None
        self.history = []
        self.ws = None
        self.running = False

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("wss://ws.binaryws.com/websockets/v3?app_id=1089")
        self.ws.send(json.dumps({ "authorize": self.token }))
        self.running = True

    def subscribe_ticks(self):
        self.ws.send(json.dumps({ "ticks": "R_100" }))

    def get_last_digits(self, count=8):
        digits = []
        while len(digits) < count and self.running:
            msg = json.loads(self.ws.recv())
            if "tick" in msg:
                digit = int(str(msg["tick"]["quote"])[-1])
                digits.append(digit)
        return digits

    def meets_strategy(self, digits):
        below_3 = [d for d in digits if d < 3]
        above_3 = [d for d in digits if d > 3]

        if self.strategy == "0 Absoluto":
            return len(above_3) == 8
        elif self.strategy == "4 Acima":
            return len(below_3) >= 4
        elif self.strategy == "4 Plus":
            threshold = random.randint(2, 7)
            return len(below_3) >= threshold
        return False

    def place_bet(self):
        proposal = {
            "buy": 1,
            "price": self.stake,
            "parameters": {
                "amount": self.stake,
                "basis": "stake",
                "contract_type": "DIGITOVER",
                "currency": "USD",
                "duration": 1,
                "duration_unit": "t",
                "symbol": "R_100",
                "barrier": 3
            }
        }
        self.ws.send(json.dumps({ "proposal": proposal["parameters"], "subscribe": 1 }))
        while True:
            response = json.loads(self.ws.recv())
            if "proposal" in response:
                buy_req = {
                    "buy": response["proposal"]["id"],
                    "price": self.stake
                }
                self.ws.send(json.dumps(buy_req))
            elif "buy" in response:
                self.current_contract_id = response["buy"]["contract_id"]
                break

    def check_result(self):
        while self.running:
            response = json.loads(self.ws.recv())
            if "profit_table" in response:
                contract = response["profit_table"]["transactions"][0]
                profit = float(contract["sell_price"]) - float(contract["buy_price"])
                self.total_profit += profit
                self.consecutive_losses = 0 if profit > 0 else self.consecutive_losses + 1
                self.history.append({
                    "entry": self.stake,
                    "result": "WIN" if profit > 0 else "LOSS",
                    "profit": profit
                })
                self.stake = self.initial_stake if profit > 0 else self.stake * self.martingale_factor
                break

    def run(self):
        self.connect()
        self.subscribe_ticks()
        while self.running:
            if self.consecutive_losses >= self.max_consecutive_losses or self.total_profit <= -self.max_loss or self.total_profit >= self.target_profit:
                self.running = False
                break

            digits = self.get_last_digits()
            if self.meets_strategy(digits):
                self.place_bet()
                self.check_result()
                time.sleep(1)

        self.ws.close()