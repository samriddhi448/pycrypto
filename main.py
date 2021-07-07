import requests
import json
from tkinter import *

pycrypto = Tk()
pycrypto.title("My Crpto Protfolio")
pycrypto.iconbitmap('favicon.ico')

def font_color(amount):
    if amount >= 0:
        return "green"
    else:
        return "red"

def my_portfolio():
    api_request = requests.get(
    "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=1555d7a9-2cbc-4c7d-88a1-de83f1f7948f")

    api = json.loads(api_request.content)
   

    coins =[{
        "symbol": "BTC",
        "amount_owned": 2,
        "price_per_coin": 3500,
    },
    {
        "symbol": "ADA",
        "amount_owned": 100,
        "price_per_coin": 2.05

    },
    {
        "symbol": "ETH",
        "amount_owned": 75,
        "price_per_coin": 25
    },
    {
        "symbol": "USDT",
        "amount_owned": 10,
        "price_per_coin": 48.05
    }]

    total_pl =0
    coin_row =1
    total_curr_value=0
    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin["symbol"]:
                total_paid = coin["amount_owned"] * coin["price_per_coin"]
                current_value = coin["amount_owned"] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin["price_per_coin"]
                total_pl_coin = pl_percoin *coin["amount_owned"]

                total_pl = total_pl + total_pl_coin
                total_curr_value=total_curr_value+current_value

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black",font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=0, sticky=N+S+E+W)

                price = Label(pycrypto, text=" {0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                price.grid(row=coin_row, column=1, sticky=N+S+E+W)

                no_coins = Label(pycrypto, text=coin["amount_owned"], bg="#F3F4F6", fg="black",font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=2, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=3, sticky=N+S+E+W)

                current_val = Label(pycrypto, text="${0: .2f}".format(current_value), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                current_val.grid(row=coin_row, column=4, sticky=N+S+E+W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_percoin), bg="#F3F4F6", fg=font_color(float("{0: .2f}".format(pl_percoin))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=5, sticky=N+S+E+W)

                Total_pl = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=font_color(float("{0: .2f}".format(total_pl_coin))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                Total_pl.grid(row=coin_row, column=6, sticky=N+S+E+W)

                coin_row = coin_row +1

    Total_cv = Label(pycrypto, text="${0:.2f}".format(total_curr_value), bg = "#F3F4F6", fg = "black", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 2, relief = "groove")
    Total_cv.grid(row=coin_row, column=4, sticky=N+S+E+W)

    Total_pl = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    Total_pl.grid(row=coin_row, column=6, sticky=N+S+E+W)
    
    api=""

    update = Button(pycrypto, text="Update", bg="#142E54", fg="black", command=my_portfolio,
                    font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    update.grid(row=coin_row+1, column=6, sticky=N+S+E+W)
    


name = Label(pycrypto, text="Coin Name", bg="#142E54", fg="white")
name.grid(row=0, column=0, sticky=N+S+E+W)

price = Label(pycrypto, text="Price", bg="#142E54", fg="white")
price.grid(row=0, column=1, sticky=N+S+E+W)

no_coins = Label(pycrypto, text="Coin Owned", bg="#142E54", fg="white")
no_coins.grid(row=0, column=2, sticky=N+S+E+W)

amount_paid = Label(pycrypto, text="Total Amount Paid",bg="#142E54", fg="white")
amount_paid.grid(row=0, column=3, sticky=N+S+E+W)

current_val = Label(pycrypto, text="Current Value", bg="#142E54", fg="white")
current_val.grid(row=0, column=4, sticky=N+S+E+W)

pl_coin = Label(pycrypto, text="P/L Per Coin", bg="#142E54", fg="white")
pl_coin.grid(row=0, column=5, sticky=N+S+E+W)

Totalpl = Label(pycrypto, text="Total P/L with Coin", bg="#142E54", fg="white")
Totalpl.grid(row=0, column=6, sticky=N+S+E+W)



my_portfolio()
pycrypto.mainloop()

