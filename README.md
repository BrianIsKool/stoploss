# Binance Trading Bot with Telegram Notifications

This repository contains a trading bot that interacts with Binance's API, performs automated stop-loss orders based on market conditions, and sends notifications to a Telegram channel. The bot is built using Python, `binance` API, `telebot` (for Telegram notifications), and `asyncio` for asynchronous operation.

## Features

- **Real-time market tracking**: Fetches market data from Binance for symbols with USDT pairs.
- **Automated Stop-Loss Orders**: Automatically places stop-loss orders after a buy order is filled.
- **Telegram Notifications**: Sends notifications about stop-loss orders to a Telegram channel.
- **Dynamic precision**: Handles dynamic decimal precision for stop-loss order prices and quantities.

## Requirements

- Python 3.7+.
- Install the required Python libraries:
  ```bash
  pip install python-binance telebot asyncio
