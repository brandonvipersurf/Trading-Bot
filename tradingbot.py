from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment
import os

API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
BASE_URL = os.environ["API_URL"]

class RebalancingMLTrader(Strategy):
    def initialize(self, symbol="SPY", cash_at_risk=0.5, target_allocation=0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.cash_at_risk = cash_at_risk
        self.target_allocation = target_allocation
        self.api = REST(base_url=os.environ["API_URL"], key_id=os.environ["API_KEY"], secret_key=os.environ["API_SECRET"])

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity

    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime("%Y-%m-%d"), three_days_prior.strftime("%Y-%m-%d")

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment

    def rebalance_portfolio(self):
        portfolio_value = self.get_portfolio_value()
        target_value = portfolio_value * self.target_allocation
        current_price = self.get_last_price(self.symbol)
        current_position = self.get_position(self.symbol)
        current_value = current_position.quantity * current_price if current_position else 0

        if current_value < target_value:
            # Buy more to reach target allocation
            quantity_to_buy = (target_value - current_value) // current_price
            if quantity_to_buy > 0:
                order = self.create_order(
                    self.symbol,
                    quantity_to_buy,
                    "buy",
                    type="market"
                )
                self.submit_order(order)
        elif current_value > target_value:
            # Sell excess to reach target allocation
            quantity_to_sell = (current_value - target_value) // current_price
            if quantity_to_sell > 0:
                order = self.create_order(
                    self.symbol,
                    quantity_to_sell,
                    "sell",
                    type="market"
                )
                self.submit_order(order)

    def on_trading_iteration(self):
        probability, sentiment = self.get_sentiment()
        print(f"Sentiment Analysis - Probability: {probability}, Sentiment: {sentiment}")

        # Perform rebalancing in each trading iteration
        self.rebalance_portfolio()

# Set up the backtest
start_date = datetime(2023, 12, 15)
end_date = datetime(2023, 12, 31)

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True,
}

broker = Alpaca(ALPACA_CREDS)

strategy = RebalancingMLTrader(
    name="RebalancingMLTrader",
    broker=broker,
    parameters={"symbol": "SPY", "cash_at_risk": 0.5, "target_allocation": 0.5}
)

strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol": "SPY", "cash_at_risk": 0.5, "target_allocation": 0.5})
