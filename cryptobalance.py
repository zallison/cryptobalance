#!/usr/bin/env python
""" Retrieve and calculate crypto holdings """

# To the extent possible under law, Zachary Allison has waived all
# copyright and related or neighboring rights to
# cryptobalance.py. This work is published from: United States.


import json
import sys
import requests


# API ALLOWANCE
PROGRESS_BAR = 1
ALLOWANCE = 0


def read_data(data_file):
    """ Read the json file containing holdings info.
    See sample for more information on formatting """
    with open(data_file) as json_data:
        all_data = json.load(json_data)
        urls = all_data["urls"]
        holdings = all_data["holdings"]
        return urls, holdings


def read_all_prices(urls):
    """ Loop over each price pair and get their values """
    toolbar_width = len(urls)
    prices = {}
    if PROGRESS_BAR:
        sys.stderr.write("[%s]" % (" " * toolbar_width))
        sys.stderr.flush()
        sys.stderr.write("\b" * (toolbar_width+1))
    for k, url in urls.items():
        prices[k] = get_price(url)
        if PROGRESS_BAR:
            sys.stderr.write("-")
            sys.stderr.flush()
    if PROGRESS_BAR:
        sys.stdout.write("\n")
    return prices


def print_headers():
    """ Printer the header for the table """
    print("symbol\t   count\t    price\t\t    total")
    print("-" * 71)


def print_data(holdings, prices):
    """ Output the Data is a friendly table """
    total = 0
    row_format = "{}:\t{:8,.2f}\t{:13,.2f} [{:7,.4f}]\t{:13,.2f} [{:7,.4f}]"
    for accountname in sorted(holdings.keys()):
        account = holdings[accountname]
        if "pair" in account.keys():
            account["val"] = prices[account["pair"]]

        print(row_format.format(
            accountname,
            float(account["count"]),
            float(account["val"]), float(account["val"]) / prices["BTC-USD"],
            float(account["count"]) * float(account["val"]),
            float(account["count"]) *
            float(account["val"]) / prices["BTC-USD"]))
        total = total + float(account["count"]) * float(account["val"])
    print("-" * 71)
    total_format = "Total:\t\t\t\t{:29,.2f} [{:7,.4f}]"
    print(total_format.format(total, total / prices["BTC-USD"]))
    print("API Allowance Left: {}".format(ALLOWANCE))


def get_price(url):
    """ Get the price from a given URL """
    global ALLOWANCE
    source = ""
    try:
        source = requests.get(url).text
        source = json.loads(source)
        ALLOWANCE = source["allowance"]["remaining"]
    except:
        print("\nError loading {}:\n{}".format(url, source))
        return "0"
    return source["result"]["price"]


def main():
    """ Load the data, process it, and display the table """

    urls, holdings = read_data(sys.argv[1])

    prices = read_all_prices(urls)

    print_headers()

    print_data(holdings, prices)


if __name__ == "__main__":
    main()
