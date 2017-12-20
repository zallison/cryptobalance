#!/usr/bin/env python

# To the extent possible under law, Zachary Allison has waived all
# copyright and related or neighboring rights to
# cryptobalance.py. This work is published from: United States.

import json
import sys
import requests


# API Allowance
allowance = 0
progress_bar = 1


def read_data(data_file):
    with open(data_file) as json_data:
        d = json.load(json_data)
        urls = d["urls"]
        holdings = d["holdings"]
        return urls, holdings


def read_all_prices(urls):
    toolbar_width = len(urls)
    prices = {}
    if progress_bar:
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))
    for k, url in urls.iteritems():
        prices[k] = get_price(url)
        if progress_bar:
            sys.stdout.write("-")
            sys.stdout.flush()
    if progress_bar:
        sys.stdout.write("\n")
    return prices


def print_headers():
    print("symbol\t   count\t    price\t\ttotal")
    print("-----------------------------------------------------")


def print_data(holdings, prices):
    total = 0
    for accountname in sorted(holdings.iterkeys()):
        account = holdings[accountname]
        if "pair" in account.keys():
            account["val"] = prices[account["pair"]]
        print("{}:\t{:8,.2f}\t{:13,.2f}\t{:13,.2f}".format(
            accountname,
            float(account["count"]),
            float(account["val"]),
            float(account["count"]) * float(account["val"])))
        total = total + float(account["count"]) * float(account["val"])
    print("-----------------------------------------------------")
    print("Total:\t\t\t\t{:21,.2f}".format(total))
    print("API Allowance Left: {}".format(allowance))


def get_price(url):
    global allowance
    source = ""
    try:
        source = requests.get(url).text
        source = json.loads(source)
        allowance = source["allowance"]["remaining"]
    except:
        print("\nError loading {}:\n{}".format(url, source))
        return "0"
    return source["result"]["price"]


def main():
    urls, holdings = read_data(sys.argv[1])

    prices = read_all_prices(urls)

    print_headers()

    print_data(holdings, prices)


if __name__ == "__main__":
    main()
