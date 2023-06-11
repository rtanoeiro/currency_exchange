"""Class that hold all email functions the team uses to send reports by email."""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

import pandas as pd

from .email_addresses import EMAILS

SMTP_SERVER: str = os.environ["SMTP_SERVER"]
if SMTP_SERVER is None:
    raise ValueError("SMTP_SERVER not found in environment variables")

SMTP_USERNAME: str = os.environ["SMTP_USERNAME"]
if SMTP_USERNAME is None:
    raise ValueError("SMTP_USERNAME not found in environment variables")

APP_PASSWORD: str = os.environ["APP_PASSWORD"]
if APP_PASSWORD is None:
    raise ValueError("APP_PASSWORD not found in environment variables")


class Email:
    """
    Class to hold all email functions the team uses to send reports by email.
    """

    def __init__(self) -> None:
        """
        Each Email object will represent a MIMEMultipart object.
        So for each different email, the class will be called.
        """
        self.message = MIMEMultipart()
        self.default_sender = EMAILS["RAMON_EMAIL"]
        self.smtp_server = SMTP_SERVER
        self.smtp_username = SMTP_USERNAME
        self.app_password = APP_PASSWORD

    def send_email_without_attachment(
        self,
        receiver: List[str],
        subject: str,
        cc_emails: Optional[List[str]] = None,
    ):

        self.message["From"] = self.default_sender
        self.message["To"] = ", ".join(receiver)
        self.message["Subject"] = subject

        if cc_emails:
            self.message["Cc"] = ", ".join(cc_emails)

        self.message.attach(MIMEText("This is a test email", "html"))
        self.send_email(receiver=receiver)

    def send_email_with_attachment(
        self,
        receiver: List[str],
        subject: str,
        report_name: str,
        attachment_df: pd.DataFrame,
        cc_emails: Optional[List[str]] = None,
    ) -> None:
        """
        Function used to send an email with attachment.

        INPUTS
        ------
            receiver (str): email of receiver. Must be an email from an environment variable.
            subject (str): subject of the email.
            report_name (str): Name of the report to appear on the email.
            attachment_path (str): Path to the attachment file.
            cc_emails (Optional[List[str]], optional): CCed emails to receive report.
                Defaults to None.
        """

        default_message = f"""
            <html>

            <body>
                <p>Hi,</p>
                <p>Please find the attached {report_name}.</p>
                <br />
                <p>Contact the data team directly if you have any questions.</p>
                <p>Thank you!</p>
                <br />
                <p>Cheers,<br />
                    The Data Team</p>
                <br />
                <p style="color:red;">
                    Please do not reply to this email as it is auto-generated.
                </p>
            </body>

            </html>
        """

        self.message["From"] = self.default_sender
        self.message["To"] = ", ".join(receiver)
        self.message["Subject"] = subject

        if cc_emails:
            self.message["Cc"] = ", ".join(cc_emails)

        self.message.attach(MIMEText(default_message, "html"))

        attachment = self.get_df_attachment(
            attachment_df=attachment_df, report_name=report_name
        )
        self.message.attach(attachment)

        self.send_email(receiver=receiver)

    def get_df_attachment(
        self, attachment_df: pd.DataFrame, report_name: str
    ) -> MIMEText:
        """
        This function will be used to attach the Dataframe into the email on it's
        selected file format

        INPUTS
        ------
            attachment_df (pd.DataFrame): The DataFrame to be attached
            report_name (str): Name of report to be attached

        OUTPUTS
        -------
            MIMEText: MIMEText object with the DataFrame as a string attached
        """

        string_report = attachment_df.to_csv(index=False)
        attachment = MIMEText(string_report, "csv")
        attachment.add_header(
            "Content-Disposition", f"attachment; filename= {report_name}"
        )

        return attachment

    def send_email(self, receiver: List[str]) -> None:
        """
        Separate function to send email.

        INPUTS
        ------
            receiver (str): receiver email address.
        """
        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.starttls()
            server.login(self.smtp_username, self.app_password)
            failed_emails = server.sendmail(
                self.default_sender, receiver, self.message.as_string()
            )

        if len(failed_emails) == 0:
            logging.info("Email sent successfully to all recipients")
        else:
            logging.error("Email failed to send to %s", failed_emails)
