# cryptobalance


**** This API is no longer available ****

Tired of adding up your crypto earnings by hand?

Using the cryptowat.ch api it grabs the current price and shows you
the current price, value, and total value.

Just setup a json file containing your holdings and which URLs to use.

For example:

    {
        "holdings": {
            "BTC": { "count": 12.25, "pair": "BTC-USD" },
            "ETH": { "count": 500.21, "pair": "ETH-USD" },
            "LTC": { "count": 10.1, "pair": "LTC-USD" },
            "BCH": { "count": 9.5, "pair": "BCH-USD" },
            "XMR": { "count": 300.5, "pair": "XMR-USD" }
        },
        "urls": {
            "BTC-USD": "https://api.cryptowat.ch/markets/gdax/btcusd/price",
            "ETH-USD": "https://api.cryptowat.ch/markets/gdax/ethusd/price",
            "LTC-USD": "https://api.cryptowat.ch/markets/gdax/ltcusd/price",
            "BCH-USD": "https://api.cryptowat.ch/markets/bitfinex/bchusd/price",
            "XMR-USD": "https://api.cryptowat.ch/markets/bitfinex/xmrusd/price"
        }
    }


run it:

    python cryptobalance.py my-stuff.json

and the output:

    symbol     count            price               total
    -----------------------------------------------------
    BCH:        9.50             3,194.60       30,348.70
    BTC:       12.25            17,084.78      209,288.55
    ETH:      500.21               799.00      399,667.79
    LTC:       10.10               331.04        3,343.50
    XMR:      300.50               388.41      116,717.21
    -----------------------------------------------------
    Total:                                     759,365.75
    API Allowance Left: 7923719973
