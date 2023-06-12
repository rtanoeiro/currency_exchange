"""Main script to create data and send emails"""

if __name__ == "__main__":
    from utils.email_api import Email
    from utils.email_addresses import EMAILS
    from utils.currency_exchange import CurrencyExchange

    CURRENCY_1 = ["EUR", "GBP"]
    CURRENCY_2 = ["BRL"]
    BASE_CURRENCY = "AUD"
    cr = CurrencyExchange(
        currencies_to_watch=CURRENCY_1, base_currency_to_use=BASE_CURRENCY
    )
    cr2 = CurrencyExchange(
        currencies_to_watch=CURRENCY_2, base_currency_to_use=BASE_CURRENCY
    )
    email = Email(
        to_address=[EMAILS["RAMON_EMAIL"], EMAILS["REGINA_EMAIL"]],
        subject="Euro/GBP/BRL Currency Exchange Rates",
    )

    email.add_attachment(attachment_type="Image", attachment_path="EUR_GBP.png")
    email.add_attachment(attachment_type="Image", attachment_path="BRL.png")
    email.send_email()
