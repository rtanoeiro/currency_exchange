"""Module to hold all functions to convert into different Currency Exchanges"""

from urllib.request import urlretrieve

import datetime
import pandas as pd
from typing import Optional
from currency_converter import ECB_URL, CurrencyConverter


class CurrencyExchange:
    """
    Class holding useful functions for Currency Conversion calculations

    The base currency for this Database is Euro. To make calculations on any of the
    available currencies, the data file will be updated based on the base currency selected
    """

    def __init__(
        self, currencies_to_watch: list[str], base_currency_to_use: str = "EUR"
    ) -> None:
        """
        Construction of class function

        Args:
            currencies_to_watch (list[str]): Not all currencies will be needed.
            This list will only keep the ones we want to keep an eye on.
            base_currency_to_use (str, optional): The currency on the Dataframe is "EUR".
            This attribute will be used to convert the base currency of the DataFrame
            into the desired one specified. Defaults to "EUR".

            Example: If you currently have "EUR", no need to pass a value.
            If you currently "AUD", then simply assign "AUD" to this attribute
        """

        self.currencies_to_watch = currencies_to_watch
        self.base_currency_to_use = base_currency_to_use
        self.currency_exchange = CurrencyConverter(currency_file=ECB_URL)

    def _get_dataframe(self) -> pd.DataFrame:
        """
        Function to get the latest DataFrame from the European Central Bank

        Returns:
            pd.DataFrame: Last updated Dataframe.
        """

        file_path, _ = urlretrieve(url=ECB_URL)
        data = pd.read_csv(file_path, compression="zip", index_col=0)
        data.pop(data.columns[-1])
        data.to_csv("normal_dataframe.csv", index=True)

        return data

    def convert_data_to_currency(self) -> pd.DataFrame:
        """
        This function will convert the Base Data file from "EUR" currency exchange rates
        into the desired currency

        Args:
            target_currency (str): Currency to convert the data to.
                Examples are "USD", "AUD"

        Returns:
            pd.DataFrame: Converted DataFrame
        """

        if self.base_currency_to_use == "EUR":
            return self._get_dataframe()

        data = self._get_dataframe()
        data["EUR"] = 1 / data[self.base_currency_to_use]
        data = data[self.currencies_to_watch + [self.base_currency_to_use]]

        for column in data.columns:
            if (column == self.base_currency_to_use) or (column == "EUR"):
                pass
            else:
                data[column] = data[column] / data[self.base_currency_to_use]

        data.pop(self.base_currency_to_use)

        return data

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

    def convert_amount(
        self,
        amount: float,
        base_currency: str,
        target_currency: str,
        date: Optional[datetime.date] = None,
    ) -> None:
        """
        This function will convert the amount
        on the default currency into the desired one

        Args:
            currency (str): Currency.  For a full list of currencies, use the
                get_available_currency_rates method
            amount (float): Amount to be converted
        """

        amount_converted = self.currency_exchange.convert(
            amount=amount,
            currency=base_currency,
            new_currency=target_currency,
            date=date,
        )
        print(amount_converted)

    def plot_period(self, period_amount: int = 1, period_timeframe: str = "month"):
        """
        Function to plot the last period of exchange rates
        This image can be attached to an email or used for analysis

        Acceptable values on the period_timeframe parameter are:
        year, month, day

        The timeframe and period can be adjusted and
        Args:
        period_amount (int): Amount of timeframe to go back from current day.
            Defaults to  1
        period_timeframe (str): Timeframe to go back from today.
            Defaults to "month"

        """

        period_last_day = datetime.datetime.today()

        ## TODO: IMPROVE LOGIC
        if period_timeframe == "month":
            initial_day = datetime.datetime(
                year=period_last_day.year,
                month=period_last_day.month - period_amount,
                day=period_last_day.day,
            )
        elif period_timeframe == "year":
            initial_day = datetime.datetime(
                year=period_last_day.year - period_amount,
                month=period_last_day.month,
                day=period_last_day.day,
            )
        elif period_timeframe == "day":
            initial_day = datetime.datetime(
                year=period_last_day.year,
                month=period_last_day.month,
                day=period_last_day.day - period_amount,
            )
