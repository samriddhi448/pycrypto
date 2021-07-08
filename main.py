from tkinter import *
from tkinter import messagebox , Menu
from sqlite3.dbapi2 import Cursor
import requests
import json
from tkinter import *
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crpto Protfolio")
pycrypto.iconbitmap('favicon.ico')

con = sqlite3.connect('coin.db')
Cursorobj = con.cursor()
Cursorobj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT, amount INTEGER,price REAL) ")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_nav()
    app_header()
    my_portfolio()

def app_nav():
    def clear_all():
        Cursorobj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showwarning("Portfolio Notification","Portfolio Cleared - Add New Coins")
        reset()
    def close_app():
        pycrypto.destroy()
           
    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio',command=clear_all)
    file_item.add_command(label='Close App',command=close_app)
    menu.add_cascade(label="File",menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
    api_request = requests.get(
    "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=1555d7a9-2cbc-4c7d-88a1-de83f1f7948f")

    api = json.loads(api_request.content)
   
    Cursorobj.execute("SELECT * FROM coin")
    coins = Cursorobj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        Cursorobj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(), price_txt.get(),amount_txt.get()))
        con.commit()

        messagebox.showinfo("Portfolio notification","Coin Added To Portfolio Successfully!")
        reset()

    def update_coin():
        Cursorobj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        
        
        con.commit()
        messagebox.showinfo("Portfolio notification","Coin Updated To Portfolio Successfully!")
        reset()

    def delete_coin():
        Cursorobj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        
        
        con.commit()
        messagebox.showinfo("Portfolio notification","Coin Deleted From Portfolio Successfully!")
        reset()

    total_pl =0
    coin_row =1
    total_curr_value=0
    total_amt_paid =0

    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin *coin[2]

                total_pl += total_pl_coin
                total_curr_value += current_value
                total_amt_paid += total_paid
                
                portfolio_id = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black",font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black",font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N+S+E+W)

                price = Label(pycrypto, text=" {0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                price.grid(row=coin_row, column=2, sticky=N+S+E+W)

                no_coins = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black",font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

                current_val = Label(pycrypto, text="${0: .2f}".format(current_value), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                current_val.grid(row=coin_row, column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_percoin), bg="#F3F4F6", fg=font_color(float("{0: .2f}".format(pl_percoin))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                Total_pl = Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=font_color(float("{0: .2f}".format(total_pl_coin))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
                Total_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)

                coin_row += 1

    #insert coin
    symbol_txt = Entry(pycrypto, borderwidth=3, relief="groove")
    symbol_txt.grid(row=coin_row+1, column =1)

    price_txt = Entry(pycrypto, borderwidth=3, relief="groove")
    price_txt.grid(row=coin_row+1, column =2)

    amount_txt = Entry(pycrypto, borderwidth=3, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3)

    add_coin = Button(pycrypto, text="Add Coin", bg="#142E54", fg="white", command=insert_coin,font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    add_coin.grid(row=coin_row+1, column=4, sticky=N+S+E+W)

    #update coin
    portid_update = Entry(pycrypto, borderwidth=3, relief="groove")
    portid_update.grid(row=coin_row+2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=3, relief="groove")
    symbol_update.grid(row=coin_row+2, column=1)

    price_update = Entry(pycrypto, borderwidth=3, relief="groove")
    price_update.grid(row=coin_row+2, column=2)

    amount_update = Entry(pycrypto, borderwidth=3, relief="groove")
    amount_update.grid(row=coin_row+2, column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin", bg="#142E54", fg="white", command=update_coin,
                      font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    update_coin_txt.grid(row=coin_row+2, column=4, sticky=N+S+E+W)

    #delete coin

    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=coin_row+3, column=0)

    delete_coin_txt = Button(pycrypto, text="Delete Coin", bg="#142E54", fg="white",
                             command=delete_coin, font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    delete_coin_txt.grid(row=coin_row+3, column=4, sticky=N+S+E+W)


    total_amt_paid = Label(pycrypto, text="${0:.2f}".format(total_amt_paid), bg="#F3F4F6",fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    total_amt_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

    Total_cv = Label(pycrypto, text="${0:.2f}".format(total_curr_value), bg = "#F3F4F6", fg = "black", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 2, relief = "groove")
    Total_cv.grid(row=coin_row, column=5, sticky=N+S+E+W)

    Total_pl = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="#F3F4F6", fg="black", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    Total_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)
    
    api=""

    refresh = Button(pycrypto, text="Refresh", bg="#142E54", fg="black", command=reset,font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    refresh.grid(row=coin_row+1, column=7, sticky=N+S+E+W)
    

def app_header():


    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#142E54", fg="white")
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    name = Label(pycrypto, text="Coin Name", bg="#142E54", fg="white")
    name.grid(row=0, column=1, sticky=N+S+E+W)

    price = Label(pycrypto, text="Price", bg="#142E54", fg="white")
    price.grid(row=0, column=2, sticky=N+S+E+W)

    no_coins = Label(pycrypto, text="Coin Owned", bg="#142E54", fg="white")
    no_coins.grid(row=0, column=3, sticky=N+S+E+W)

    amount_paid = Label(pycrypto, text="Total Amount Paid",bg="#142E54", fg="white")
    amount_paid.grid(row=0, column=4, sticky=N+S+E+W)

    current_val = Label(pycrypto, text="Current Value", bg="#142E54", fg="white")
    current_val.grid(row=0, column=5, sticky=N+S+E+W)

    pl_coin = Label(pycrypto, text="P/L Per Coin", bg="#142E54", fg="white")
    pl_coin.grid(row=0, column=6, sticky=N+S+E+W)

    Totalpl = Label(pycrypto, text="Total P/L with Coin", bg="#142E54", fg="white")
    Totalpl.grid(row=0, column=7, sticky=N+S+E+W)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

Cursorobj.close()
con.close()

