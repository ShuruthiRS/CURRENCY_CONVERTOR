# Import required modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import requests
import datetime as dt

# Converting stuff
class CurrencyConverter:

    def _init_(self, url):
        self.url = 'https://api.exchangerate.host/latest'
        self.response = requests.get(url)
        self.data = self.response.json()
        self.rates = self.data.get('rates')

    def convert(self, amount, base_currency, des_currency):
        if base_currency != 'EUR':
            amount = amount/self.rates[base_currency]

        # Limiting the result to 2 decimal places
        amount = round(amount*self.rates[des_currency], 2)
        # Add comma every 3 numbers
        amount = '{:,}'.format(amount)
        return amount

# Main window
class Main(tk.Tk):

    def _init_(self, converter):
        tk.Tk._init_(self)
        self.title('Currency Converter')
        self.geometry('400x400')
        self.config(bg='#3A3B3C')
        self.CurrencyConverter = converter

        # Create title label
        self.title_label = Label(self, text='Currency Converter', bg='#3A3B3C', fg='white', font=('franklin gothic medium', 20), relief='sunken')
        self.title_label.place(x=200, y=35, anchor='center')

        # Create date label
        self.date_label = Label(self, text=f'{dt.datetime.now():%A, %B %d, %Y}', bg='#3A3B3C', fg='white', font=('calibri', 10))
        self.date_label.place(x=0, y=400, anchor='sw')

        # Create version label
        self.version_label = Label(self, text='v1.0', bg='#3A3B3C', fg='white', font=('calibri', 10))
        self.version_label.place(x=400, y=400, anchor='se')

        # Create amount label
        self.amount_label = Label(self, text='Input Amount: ', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15))
        self.amount_label.place(x=200, y=80, anchor='center')

        # Create amount entry box
        self.amount_entry = Entry(self)
        self.amount_entry.config(width=25)
        self.amount_entry.place(x=200, y=110, anchor='center')

        # Create 'from' label
        self.base_currency_label = Label(self, text='From: ', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15))
        self.base_currency_label.place(x=200, y=140, anchor='center')

        # Create 'to' label
        self.destination_currency_label = Label(self, text='To: ', bg='#3A3B3C', fg='white', font=('franklin gothic book', 15))
        self.destination_currency_label.place(x=200, y=200, anchor='center')

        # Create dropdown menus
        self.currency_variable1 = StringVar(self)
        self.currency_variable2 = StringVar(self)
        self.currency_variable1.set('USD')
        self.currency_variable2.set('IDR')

        self.currency_combobox1 = ttk.Combobox(self, width=20, textvariable=self.currency_variable1, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox1.place(x=200, y=170, anchor='center')

        self.currency_combobox2 = ttk.Combobox(self, width=20, textvariable=self.currency_variable2, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.currency_combobox2.place(x=200, y=230, anchor='center')

        # Create 'convert' button
        self.convert_button = Button(self, text='Convert', bg='#52595D', fg='white', command=self.processed)
        self.convert_button.place(x=170, y=270, anchor='center')

        # Create 'clear' button
        self.clear_button = Button(self, text='Clear', bg='red', fg='white', command=self.clear)
        self.clear_button.place(x=230, y=270, anchor='center')

        # Create converted result field
        self.final_result = Label(self, text='', bg='#52595D', fg='white', font=('calibri', 12), relief='sunken', width=40)
        self.final_result.place(x=200, y=310, anchor='center')

    # Create clear function, to clear the amount field and final result field
    def clear(self):
        clear_entry = self.amount_entry.delete(0, END)
        clear_result = self.final_result.config(text='')
        return clear_entry, clear_result

    # Create a function to perform
    def processed(self):
        try:
            given_amount = float(self.amount_entry.get())
            given_base_currency = self.currency_variable1.get()
            given_des_currency = self.currency_variable2.get()
            converted_amount = self.CurrencyConverter.convert(given_amount, given_base_currency, given_des_currency)
            # Add comma every 3 numbers
            given_amount = '{:,}'.format(given_amount)

            self.final_result.config(text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}')

        # Create warning message box
        except ValueError:
            convert_error = messagebox.showwarning('WARNING!', 'Please Fill the Amount Field (integer only)!')
            return convert_error


if _name_ == '_main_':
    converter = CurrencyConverter('https://api.exchangerate.host/latest')
    Main(converter)
    mainloop()
