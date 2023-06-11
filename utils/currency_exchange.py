"""Module to hold all functions to convert into different Currency Exchanges"""

from forex_python.converter import CurrencyRates
from .available_currencies import available_currencies

class CurrencyExchange:
    """
    Class holding useful functions for Currency Exchange calculations    
    """

    def __init__(self) -> None:
        self.default_currency = "AUD"
        self.cr = CurrencyExchange()
    
    def get_available_currency_rates(self) -> None:
        
        for currencie in available_currencies:
            print(f"{currencie}: {currencie}")

    def convert_into(self, currency: str, amount: float) -> None:
        """
        This function will convert the amount
        on the default currency into the desired one

        Args:
            currency (str): Currency. For a full list of currencies, use the
                get_available_currency_rates method 
            amount (float): Amount to be converted
        """
        

