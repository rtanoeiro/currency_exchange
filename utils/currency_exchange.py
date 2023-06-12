"""Module to hold all functions to convert into different Currency Exchanges"""

from urllib.request import urlretrieve

import pandas as pd
from currency_converter import ECB_URL, CurrencyConverter


class CurrencyExchange:
    """
    Class holding useful functions for Currency Conversion calculations

    The base currency for this Database is Euro. To make calculations on any of the
    available currencies, the data file will be updated based on the base currency selected
    """

    def __init__(self, base_currency: str = "EUR") -> None:
        """
        Construction of class function

        Args:
            base_currency (str, optional): Currency to be used as base for all calculations.
            Defaults to "EUR".
        """
        self.default_currency = base_currency
        self.currency_exchange = CurrencyConverter(currency_file=ECB_URL)

    def get_available_currency_rates(self) -> list:
        """
        Function to get all available currencies

        Returns:
            list: List of all avalulable currencies
        """

        file_path, _ = urlretrieve(url=ECB_URL)
        data = pd.read_csv(file_path, compression="zip")
        available_currencies = [
            currency if len(currency) == 3 else "" for currency in data.columns
        ][1:-1]

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

        amount_converted = self.currency_exchange.convert(
            base_cur=self.default_currency, dest_cur=currency, amount=amount
        )
        print(amount_converted)


currency_exchange = CurrencyExchange()

currency_exchange.get_available_currency_rates()
