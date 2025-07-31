import logging
import os
import smtplib

from email.mime.text import MIMEText
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun


@function_tool()
async def get_weather(
    context: RunContext,
    city: str,
) -> str:
    """
    Get the current weather for a given city.
    """
    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather in {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Could not retrieve weather for {city}."
    except Exception as e:
        logging.error(f"Exception occurred while getting weather for {city}: {e}")
        return f"Could not retrieve weather for {city} "


@function_tool()
async def search_web(
    context: RunContext,
    query: str,
) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Exception occurred while searching for '{query}': {e}")
        return f"Could not perform search for '{query}'."


@function_tool()
async def send_email(
    context: RunContext,
    to: str,
    subject: str,
    body: str,
) -> str:
    """
    Sends an email using Gmail.
    """
    try:
        from_email = "acnphotography.04@gmail.com"
        password = os.getenv("GMAIL_PASSWORD")

        if not password:
            logging.error("GMAIL_PASSWORD environment variable not set.")
            return "GMAIL_PASSWORD environment variable not set."

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.send_message(msg)
        
        logging.info(f"Email sent to {to} with subject '{subject}'")
        return f"Email sent to {to} successfully."
    except Exception as e:
        logging.error(f"Exception occurred while sending email: {e}")
        return f"Could not send email to {to}."


