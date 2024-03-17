# WhatsApp Bulk Messenger

This software automates the process of sending messages through WhatsApp Web, enabling users to send messages in bulk. The program functions by iterating through a provided list of numbers in 'contacts.csv' and attempts to send a predefined message template to each contact. Additionally, it can extract information from other columns in the CSV file to customize specific parts of the message, resulting in personalized messages being sent to each recipient. It's important to note that the current version of the program is restricted to sending only text messages.

# Requirements

- Python >= 3.7
- Chrome driver is installed by the program automatically

# Setup

1. Install Python >= 3.7
2. Run `pip install -r requirements.txt`

# How to Run

1. Enter the message you want to send inside `message.txt` file.
2. Enter the list of numbers line-separated in `contacts.csv` file.
3. Run `python main.py`.
4. Once the program starts, you'll see the message and count of numbers.
5. After a while, Chrome should pop-up and open https://web.whatsapp.com.
6. Scan the QR code to login into WhatsApp.
7. Press `Enter` to start sending out messages.
8. Sit back and relax!
