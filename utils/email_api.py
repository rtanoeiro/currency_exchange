"""Class that hold all email functions the team uses to send reports by email."""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.nonmultipart import MIMENonMultipart
from typing import List, Optional, Union

import pandas as pd

from .email_addresses import EMAILS
from .html_messages import HTML_MESSAGES

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

    def __init__(
        self,
        to_address: List[str],
        subject: str,
        cc_addresses: Optional[List[str]] = None,
    ) -> None:
        """
        Each Email object will represent a MIMEMultipart object.
        So for each different email, the class will be called.
        """
        self.message = MIMEMultipart()
        self.smtp_server = SMTP_SERVER
        self.smtp_username = SMTP_USERNAME
        self.to_address = to_address
        self.app_password = APP_PASSWORD

        self.message["From"] = EMAILS["RAMON_EMAIL"]
        self.message["To"] = ", ".join(to_address)
        self.message["Subject"] = subject
        if cc_addresses:
            self.message["Cc"] = ", ".join(cc_addresses)

    # TODO: Check if function can be removed. We can only have different methods
    # To add messages, text, images to an MIMEMultipart object, and then call
    # send email.
    def send_email_without_attachment(
        self,
        email_message: Optional[str] = HTML_MESSAGES["DEFAULT_MESSAGE"],
    ):
        """
        Function to send an email without an attachment

        Args:
            email_message (Optional[str], optional): _description_. Defaults to HTML_MESSAGES["DEFAULT_MESSAGE"].
        """
        if email_message:
            self.message.attach(MIMEText(email_message, "html"))

        self.send_email()

    def send_email_with_attachments(
        self,
        report_name: str,
        attachment_df: pd.DataFrame,
        email_message: Optional[str] = HTML_MESSAGES["DEFAULT_MESSAGE"],
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

        if email_message:
            self.message.attach(MIMEText(email_message, "html"))

        attachment = self.get_df_attachment(
            attachment_df=attachment_df, report_name=report_name
        )
        self.message.attach(attachment)

        self.send_email()

    def get_df_attachment(
        self, attachment_df: pd.DataFrame, report_name: str
    ) -> MIMEText:
        """
        This function will be used to attach a Dataframe into the email.

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

    def add_attachment(
        self,
        attachment_type: str,
        attachment_path: Optional[str] = None,
    ):
        """
        This function will be used to add any known attachments to the message.
        Any new attachment types can be further added on the logic

        Args:
            attachment (MIMENonMultipart): _description_
            attchment_type (str): Attachment type to be added. Values can be:
                Application (still on dev), Audio, Image, Text (DataFrame),
                all are subclasses from MIMENonMultipart
            attachment_path (str): Path to attachment. If attachment is already in bytes
                format, it does not need to be called. If attachment is a file, then the
                parameter must be set.
        """
        attachment_mapping = {
            # "Application": ValueError("Attachment type still on the work"),
            "Audio": MIMEAudio,
            "Image": MIMEImage,
            "Text": MIMEText,
        }

        if attachment_type not in attachment_mapping:
            raise ValueError(f"Invalid attachment type: {attachment_type}")

        if attachment_path:
            with open(attachment_path, "rb") as file:
                binary_file = file.read()
                attachment_class = attachment_mapping[attachment_type]
                self.message.attach(attachment_class(binary_file))

    def send_email(self) -> None:
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
                from_addr=EMAILS["RAMON_EMAIL"],
                to_addrs=self.to_address,
                msg=self.message.as_string(),
            )

        if len(failed_emails) == 0:
            logging.info("Email sent successfully to all recipients")
        else:
            logging.error("Email failed to send to %s", failed_emails)
