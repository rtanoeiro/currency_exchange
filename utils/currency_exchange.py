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

    def _get_dataframe(self) -> pd.DataFrame:
        """_summary_

        Returns:
            pd.DataFrame: Last updated Dataframe from European Central Bank
        """

        file_path, _ = urlretrieve(url=ECB_URL)
        data = pd.read_csv(file_path, compression="zip")
        data.pop(data.columns[-1])

        return data

    def convert_data_to_currency(self, target_currency: str) -> pd.DataFrame:
        """
        This function will convert the Base Data file from "EUR" currency exchange rates
        into the desired currency

        Args:
            target_currency (str): Currency to convert the data to.
                Examples are "USD", "AUD"

        Returns:
            pd.DataFrame: Converted DataFrame
        """

    def get_available_currency_rates(self) -> list:
        """
        Function to get all available currencies

        Returns:
            list: List of all avalulable currencies
        """

        data = self._get_dataframe()
        available_currencies = [
            currency if len(currency) == 3 else "" for currency in data.columns
        ][1:]

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

dataframe = currency_exchange._get_dataframe()

dataframe.to_csv("Test_data.csv", index=False)
