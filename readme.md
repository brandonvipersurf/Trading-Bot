Trading Bot
This project contains a trading bot that uses the Alpaca API for trading and FinBERT for sentiment analysis of news articles. The bot can backtest strategies using historical data from Yahoo Finance.

Prerequisites
Before you begin, ensure you have met the following requirements:

- You have installed Python 3.7 or higher.
- [You have an Alpaca account and API credentials.](https://app.alpaca.markets/signup) 
- You have an internet connection to install the required libraries and interact with the APIs.
- Docker installed (Optional)
# Installation
Clone the repo:  
`git clone https://github.com/brandonvipersurf/Trading-Bot.git`  
[Create your Alpca Account and get your API Keys](https://scribehow.com/shared/Create_Alpaca_Account_and_Generate_API_Keys__N6jrgemVRu6lLP7EGiSxEA)  
Set your Keys as Environment Variables
```
echo "export API_KEY = 'your_alpaca_api_key'" >> ~/.bashrc
echo "export API_SECRET = 'your_alpaca_api_secret'" >> ~/.bashrc
```

## Traditional  
- Install python 3.7  
- Install the required libraries:
```bash
pip install -r requirements.txt
```
## Docker
- Install Docker
- Run following commands:
```
docker compose build
```

# Usage
To run the trading bot, execute the following command:  
Docker: `docker compose run app`  
bash: `python tradingbot.py` 

The bot will backtest the strategy using historical data and output the results.

## Files  
tradingbot.py: Contains the main trading bot logic.  
finbert_utils.py: Contains utility functions for sentiment analysis using FinBERT.  

## License
This project is licensed under the MIT License - see the LICENSE file for details.
