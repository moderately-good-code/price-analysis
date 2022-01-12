#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 14:30:08 2021

@author: moderately-good-code
"""

# METHODS FROM HERE ARE NOW DEPRECATED AND DELETED.
# SCRAPE DATA VIA yfinance INSTEAD.

# Coins on Kraken and coinmarketcap.com
KRAKEN_COINS_CMC = ["Bitcoin", "Ethereum", "Ripple", "Tether USD", "Cardano",
                "Polkadot", "Uniswap", "Litecoin", "Chainlink",
                "Bitcoin Cash", "Lumen", "Filecoin", "USD Coin", "TRON",
                "Dogecoin", "EOS", "Monero", "Tezos", "Cosmos", "Aave",
                "Kusama", "Algorand", "Dai", "Dash", "Compound",
                "Synthetix", "Ethereum Classic", "Zcash", "The Graph",
                "Basic Attention Token", "Waves", "Yearn Finance",
                "Decentraland", "ICON", "Qtum", "OMG Network", "Siacoin",
                "Flow", "Lisk", "OCEAN Token", "Cuve DAO Token", "Nano",
                "Kyber Network", "Storj", "Augur", "Augur v2",
                "Energy Web Token", "Aragon", "Kava", "Keep Network",
                "Balancer", "Orchid", "Gnosis", "Enzyme Finance",
                "PAX Gold", "tBTC",
                # alternative names from scraped data:
                "XRP", "Tether", "Stellar" # or is this a different tether?]
                ]

# Coins on Kraken and Yahoo Finance
KRAKEN_COINS_YF = ["BTC", "ETH", "XRP", "USDT", "ADA", "DOT1", "UNI3",
                   "LTC", "LINK", "BCH", "XLM", "FIL", "USDC", "TRX",
                   "EOS", "XMR", "XTZ", "ATOM1", "AAVE", "KSM", "ALGO",
                   "DASH", "COMP", "SNX", "ETC", "ZEC", "BAT", "WAVES",
                   "YFI", "MANA", "ICX", "QTUM", "SC", "KAVA", "NANO",
                   "CRV", "OMG", "STORJ", "KNC", "LSK", "REP", "OXT",
                   "EWT", "ANT", "MLN", "GNO", "DOGE", "ZRX", "1INCH",
                   "GHST", "ANKR", "REPV2", "AXS", "BADGER", "BNT",
                   "BAND", "BNC", "CTSI", "CHZ", "CQT", "CRV", "DYDX",
                   "ENJ", "INJ", "KAR", "LPT", "LRC", "MKR", "MINA",
                   "MIR", "MOVR", "OGN", "OXY", "PAXG", "PERP", "PHA",
                   "MATIC", "REN", "RARI", "RAY", "SDN", "SOL", "SUSHI",
                   "SAND", "WBTC", "SHIB"]
                   # No Dai, The Graph, Flow, Keep, Ocean, Balancer,
                   # Augur v2, Ethereum 2, PAX Gold or tBTC on YF? :(
