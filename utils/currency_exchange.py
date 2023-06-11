"""Module to hold all functions to convert into different Currency Exchanges"""

import datetime
from io import BytesIO
from urllib.request import urlopen, urlretrieve
from zipfile import ZipFile

import pandas as pd
import wget
from currency_converter import ECB_URL, CurrencyConverter


class CurrencyExchange:
    """
    Class holding useful functions for Currency Exchange calculations    
    """

    def __init__(self) -> None:
        self.default_currency = "AUD"
        self.currency_exchange = CurrencyConverter(currency_file=ECB_URL)

    def get_available_currency_rates(self) -> list:
        """
        Function to get all available currencies
        """

        # TODO: STUDY urlopen, urlretrieve
        file_path = urlretrieve(url=ECB_URL)
        data = pd.read_csv(file_path[0], compression='zip')
        available_currencies = [currency if len(currency)==3 else "" for currency in data.columns][1:-1]

        return available_currencies
    
    def convert_into(self, currency: str, amount: float) -> None:
        """
        This function will convert the amount
        on the default currency into the desired one

        Args:
            currency (str): Currency. For a full list of currencies, use the
                get_available_currency_rates method 
            amount (float): Amount to be converted
        """

        amount_converted = self.currency_exchange.convert(base_cur=self.default_currency, dest_cur=currency, amount=amount)
        print(amount_converted)

currency_exchange = CurrencyExchange()

currency_exchange.get_available_currency_rates()