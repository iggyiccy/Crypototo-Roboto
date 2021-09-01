# Project_2

Trading Bot Features:

- **top 10 coins prediction**
- **shitcoins prediction**

## My Idea

### Back End

#### generate_signals

    exsiting:
    > moving average

    my suggestion:
    > [Facebook's Prophet](https://research.fb.com/prophet-forecasting-at-scale/)
    > [Whale Alert's API](https://whale-alert.io)
    > [Deep Reinforcement Learning - Deep Q-learning](https://github.com/pskrunner14/trading-bot)
    > [TradingView's API or Chart Data Extractor](https://github.com/jchao01/TradingView-data-scraper)

#### execute_trade_strategy

    my suggestion:
    > Choose Risk Level

### Database

> local environment for now

### Front End

> CLI application
> Dash application
> Kibana with Elasticsearch
> Telegram Chat Bot

## Get Start

1. create a new conda environment for this project & activate it

```
conda create -n project python=3.7 anaconda -y
conda activate project
```

2. install variables

```
pip install ccxt
pip install yfinance
pip install dash_core_components
pip install dash_bootstrap_components
pip install dash
pip install pandas
pip install python-dotenv
pip install numpy //check if it is version 1.20.2
pip install matplotlib.pyplot //check if it is version 3.4.2
```

3. Run the Dash Application

```
cd project_2
python App.py
```

```
conda install gcc
```
