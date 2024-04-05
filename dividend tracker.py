# -*- coding: utf-8 -*-
"""
Dividend Tracker from Email

"""

import imaplib
import getpass
from email.header import decode_header
from datetime import datetime
import pandas as pd
from google.oauth2 import service_account
import gspread
import email
import time

def decode_subject(subject):
    decoded, encoding = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        decoded = decoded.decode(encoding if encoding else 'utf-8')
    return decoded

email_address = 'tanuj127@gmail.com'
app_password = getpass.getpass(prompt='Enter your Gmail app password: ')

mail = imaplib.IMAP4_SSL('imap.gmail.com')

mail.login(email_address, app_password)

mailbox = 'INBOX'

result, _ = mail.select(mailbox)
if result != 'OK':
    print(f"Failed to select mailbox '{mailbox}'")
    exit()

from datetime import datetime, timedelta

seven_days_ago = datetime.now() - timedelta(days=30)
since_date = seven_days_ago.strftime('%d-%b-%Y')

from email import message_from_bytes
from email import policy

def extract_html(email_message):
    html_content = None
    for part in email_message.walk():
        content_type = part.get_content_type()
        if content_type == 'text/html':
            charset = part.get_content_charset() or 'utf-8'
            try:
                html_content = part.get_payload(decode=True).decode(charset)
            except UnicodeDecodeError as e:
                print("UnicodeDecodeError occurred:", e)
                print("Charset:", charset)
                print("Payload:", part.get_payload())
                break
    return html_content


result, data = mail.search(None, 'SINCE', since_date, '(TEXT "Net Dividend")')
html_list= []

if result == 'OK':
    email_ids = data[0].split()

    if email_ids:
        print(f"Found {len(email_ids)} emails within the last 30 days with the specified criteria")
        for email_id in email_ids[:30]:
            result, email_data = mail.fetch(email_id, '(RFC822)')
            if result == 'OK':
                raw_email = email_data[0][1]
                email_message = message_from_bytes(raw_email, policy=policy.default)
                html_content = extract_html(email_message)
                subject = email_message.get("Subject")  # Get the subject of the email

                if html_content:
                    html_list.append((subject, html_content))  # Store subject and HTML content as a tuple
                else:
                    print("No HTML content found in the email")
            else:
                print(f"Failed to fetch email ID {email_id}")
    else:
        print("No emails within the last 7 days found with the specified criteria")
else:
    print("Failed to search emails within the last 7 days with the specified criteria")


mail.close()

from bs4 import BeautifulSoup
import pandas as pd

def extract_rows(table):
    rows = []
    for row in table.find_all('tr'):
        row_text = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        if any("net" in cell_text.lower() and "dividend" in cell_text.lower() for cell_text in row_text):
            if all(len(cell_text) <= 40 for cell_text in row_text):  # Check if each cell has <= 20 characters
                rows.append(row_text)
    return rows


def extract_tables(mail):
    tables = []
    if mail:
        soup = BeautifulSoup(mail, 'html.parser') 
        tables = soup.find_all('table')
    return tables


def count_tables(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    return len(tables)

import pandas as pd

df = pd.DataFrame()

for subject, first_mail in html_list:
    tables = extract_tables(first_mail)
    
    for table in tables:
        rows = extract_rows(table)
        rows_df = pd.DataFrame(rows)
        rows_df['Subject'] = subject
        df = df.append(rows_df, ignore_index=True)

df_unique = df.drop_duplicates()
df_unique.to_csv("dividend.csv", index=False)


