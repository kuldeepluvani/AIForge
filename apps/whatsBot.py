import datetime
import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from clients.ollama_client import call_llama_api


# Configuration
CONTACT_NAME = "John Doe"
LLAMA_API_URL = "http://localhost:11434/api/generate"


def find_chat_and_click(driver, contact_name):
    """Finds a chat by name and clicks on it.
    Args:
        driver: The WebDriver instance.
        contact_name: The name of the contact to find.

    Raises:
        NoSuchElementException: If the chat is not found.
    """
    text_area = driver.find_element(
        by="xpath", value="//*[@id='side']/div[1]/div/div[2]/div[2]/div/div[1]"
    )
    text_area.send_keys(CONTACT_NAME)

    time.sleep(2)

    chat_elements = driver.find_elements(By.CLASS_NAME, value="Mk0Bp")

    for chat in chat_elements:
        if chat.text == contact_name:
            chat.click()
            return

    raise NoSuchElementException(f"Chat with name '{contact_name}' not found")


def get_messages(driver):
    """Extracts incoming and outgoing messages from the current chat.

    Args:
        driver: The WebDriver instance.

    Returns:
        tuple: Two lists, one for incoming messages and one for outgoing.
    """

    main = driver.find_elements(By.CLASS_NAME, value="n5hs2j7m")
    incoming_messages = []
    outgoing_messages = []

    for msg in main:
        incoming = msg.find_elements(By.CLASS_NAME, value="message-in")
        outgoing = msg.find_elements(By.CLASS_NAME, value="message-out")

        if incoming:
            incoming_messages.append(incoming[0].text)
        elif outgoing:
            outgoing_messages.append(outgoing[0].text)

    return incoming_messages, outgoing_messages


def get_timestamp(message):
    """Extracts the timestamp (HH:MM) from a message string."""
    return message.split()[-1]


def sort_key(message):
    """Returns a datetime object for sorting messages."""
    time_str = get_timestamp(message)
    return datetime.datetime.strptime(time_str, "%H:%M")


def send_message(driver, message):
    """Sends a message in the current chat."""
    text_area = driver.find_element(
        By.XPATH,
        value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
    )
    text_area.send_keys(f"WhatsBot: {message}")

    time.sleep(5)

    send_button = driver.find_element(
        By.XPATH,
        value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span",
    )
    time.sleep(2)

    send_button.click()


def main(driver):
    """Main operation"""
    find_chat_and_click(driver, CONTACT_NAME)
    time.sleep(2)

    incoming_msgs, outgoing_msgs = get_messages(driver)
    all_messages = incoming_msgs + outgoing_msgs
    all_messages.sort(key=sort_key)

    time.sleep(2)

    conversation = ""
    for msg in all_messages:
        label = "incoming" if msg in incoming_msgs else "outgoing"
        conversation += f"{label}: {msg}\n"

    api_response = call_llama_api(
        prompt=conversation,
        pre_prompt="This is a my conversation ",
        post_prompt=" what is the context of my conversation give me a short tlrd? Do not include the conversation. Do not ask questions. Write a thank you note at the end. Message should be 100 words long. Do not include 'based on given conversation' inside the message.",
    )

    send_message(driver, api_response)


# Main program flow
if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        driver.get("https://web.whatsapp.com/")
        driver.maximize_window()
        input("Press Enter after you have logged in to WhatsApp Web.")
        main(driver)

        while True:
            wanna_quit = input("Do you want to quit? (y/n): ")
            if wanna_quit.lower() == "y":
                break
            else:
                update_contact = input("Update the contact name and press Enter: ")
                if update_contact:
                    CONTACT_NAME = update_contact
                main(driver)

    except Exception as e:
        print(f"An error occurred: {e}")
