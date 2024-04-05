import sys
from time import sleep
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def exit_program(message):
    """Exits the program gracefully, printing a message."""
    print(Style.BLUE + message + Style.RESET)
    sleep(2)
    sys.exit(0)

def read_file(filepath, encoding="utf-8"):
    """Reads a file and returns its contents as a string."""
    message = ""
    try:
        with open(filepath, "r", encoding=encoding) as file:
            message = file.read().strip()
    except FileNotFoundError:
        exit_program(f"File not found: {filepath}")
    return message

def read_phone_numbers(filepath, encoding="utf-8"):
    """Reads phone numbers from a CSV file, skipping the header."""
    numbers = []
    try:
        with open(filepath, "r", encoding=encoding) as file:
            next(file) # Skip the header row
            for line in file:
                name, phone_number = line.strip().split(",")
                if name and phone_number: # Check for empty entries
                    numbers.append((name, phone_number))
    except FileNotFoundError:
        exit_program(f"File not found: {filepath}")
    return numbers

def send_whatsapp_message(driver, phone_number, message, max_retry=3):
    """Sends a WhatsApp message using the provided URL."""
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]/p'
    try:
        sent = False
        for i in range(max_retry):
            if sent:
                break
            driver.get('https://web.whatsapp.com/send?phone=+' + phone_number + '&text=' + quote(message) + "&type=phone_number&app_absent=1")
            try:
                input_box = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                sleep(15)
                input_box.send_keys(Keys.ENTER)
            except Exception as e:
                print(Style.RED + f"Failed to send message to: {phone_number}, retry ({i+1}/{max_retry})")
                print("Make sure your phone and computer is connected to the internet.")
                print("If there is an alert, please dismiss it." + Style.RESET)
            else:
                sent=True
                print(Style.GREEN + f"Message sent to {phone_number} successfully." + Style.RESET)
                sleep(10)
        if not sent:
            # Append failed number
            print("failed")
    except Exception as e:
        print(Style.RED + f"Error sending message: {e}" + Style.RESET)

if __name__ == "__main__":
    """Main program logic."""
    print(Style.BLUE + "Starting the program..." + Style.RESET)
    sleep(2)

    # Read contacts from CSV
    phone_numbers = read_phone_numbers("contacts.csv")
    if not phone_numbers:
        exit_program(Style.RED + "No valid phone numbers found." + Style.RESET)

    # Read message template
    message_template = read_file("message.txt")
    if not message_template:
        exit_program(Style.RED + "No message template found." + Style.RESET)

    print(Style.BLUE + "\nThis is your message:" + Style.RESET)
    print(message_template)

    # Set up browser
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    print(Style.BLUE + '\nOnce your browser opens up sign in to web whatsapp')
    driver.get('https://web.whatsapp.com')
    input(Style.BLUE + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER..." + Style.RESET)

    for idx, (name, phone_number) in enumerate(phone_numbers):
        # Clean phone number
        phone_number = ''.join(char for char in phone_number if char.isdigit())
        print(Style.YELLOW + '\n{}/{} => Sending message to {}.'.format((idx+1), len(phone_numbers), phone_number) + Style.RESET)

        # Insert name into message
        formatted_message = message_template.format(name)

        send_whatsapp_message(driver, phone_number, formatted_message)

    exit_program("\nProgram is finished, thank you!")
    driver.close()
