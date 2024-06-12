''' Looker studii Dashboard Email detection '''

import imaplib
import getpass
from email.header import decode_header
from datetime import datetime
import pandas as pd
from google.oauth2 import service_account
import gspread

# Function to decode email subjects
def decode_subject(subject):
    decoded, encoding = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        decoded = decoded.decode(encoding if encoding else 'utf-8')
    return decoded

# Set your Gmail credentials
email_address = 'your email id'
app_password = getpass.getpass(prompt='Enter your Gmail app password: ')

# Connect to Gmail's IMAP server
mail = imaplib.IMAP4_SSL('imap.gmail.com')

# Log in to your Gmail account using the app password
mail.login(email_address, app_password)

# Select the '[Gmail]/Important' mailbox
mailbox = '[Gmail]/Important'
status, _ = mail.select(mailbox)

# Get today's date and day of the month
today = datetime.today()
today_date = today.strftime("%b %d, %Y")

# List of dashboard names
dashboards = ["dashboard name 1",
              "dashboard name 2",
              "dashboard name 3",
              "dashboard name 4",
              "dashboard name 5"]
df = pd.DataFrame(columns=['Date'] + dashboards)

# Get the day part without leading zeros
day_part = today.strftime("%d").lstrip("0")

        # List to store email subjects
email_subjects = []
for dashboard in dashboards:
    # Check if today is the 10th, 20th, or 30th
    if day_part in ['10', '20', '30']:
        target_subject = f"{dashboard} - {today_date}"
    else:
        target_subject = f"{dashboard} - {today_date.replace(today.strftime('%d'), day_part)}"

    # Search for emails with the specific subject in the selected mailbox
    status, email_ids = mail.search(None, f'SUBJECT "{target_subject}"')

    if status == 'OK':
        # Get a list of email IDs
        email_id_list = email_ids[0].split()



        # Loop through each email ID and fetch the subject
        for email_id in email_id_list:
            _, msg_data = mail.fetch(email_id, '(BODY[HEADER.FIELDS (SUBJECT)])')
            raw_subject = msg_data[0][1].decode('utf-8')
            subject_start = raw_subject.find('Subject:') + len('Subject:')
            subject = raw_subject[subject_start:].strip()
            decoded_subject = decode_subject(subject)
            email_subjects.append(decoded_subject)

            print(f"Raw Subject: {raw_subject}")
            print(f"Decoded Subject: {decoded_subject}")

        print(f"All Email Subjects in '{mailbox}' with subject '{target_subject}':")
        for subject in email_subjects:
            print(subject)

        if email_subjects:
            print("Search subject detected.")
            df.loc[0] = [today_date] + ['Yes' if any(dashboard in subject for subject in email_subjects) else 'No' for dashboard in dashboards]

        else:
            print("Search subject not detected.")

    else:
        print(f"Error while searching for emails with subject '{target_subject}'.")

# Logout from the server
mail.logout()

# Print the updated DataFrame
print(df)
# Unpivot the DataFrame using melt
melted_df = pd.melt(df, id_vars='Date', var_name='Dashboards', value_name='Value')

# Pivot the DataFrame back to the desired format
pivoted_df = melted_df.pivot(index='Dashboards', columns='Date', values='Value')

# Reset the index to make 'Dashboards' a column again
pivoted_df = pivoted_df.reset_index()

# Display the result
print(pivoted_df)


# Import required libraries
import gspread
from google.oauth2 import service_account
import pandas as pd

# Google Sheet credentials
SERVICE_ACCOUNT_FILE = 'keys.json'
SHEET_NAME = 'Sheet1'
SPREADSHEET_ID = 'sheet id'

# Authenticate with Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet
spreadsheet = client.open_by_key(SPREADSHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Reset the index to make 'Dashboards' a column again
pivoted_df = pivoted_df.reset_index(drop=True)  # Drop the index column

# Define a function to apply the formula
def assign_to(row):
    if row['Dashboards'] == 'dashboard name 1':
        return 'Vineet'
    elif row['Dashboards'] == 'dahsboard name 2' or row['Dashboards'] == 'dashbaord name 3':
        return 'name'
    else:
        return ''

# Apply the formula to create the new column
pivoted_df['Assigned to'] = pivoted_df.apply(assign_to, axis=1)

# Add 'Date' column
pivoted_df['Date'] = today_date  # Replace this with your actual date
#pivoted_df['Date'] = pd.to_datetime(today_date)

# Reorder columns to place 'Assigned to' column after 'Dashboards' column
columns = pivoted_df.columns.tolist()
columns.insert(1, 'Assigned to')
pivoted_df = pivoted_df[columns]

# Convert DataFrame to a list of lists
values_to_update = pivoted_df.values.tolist()

# Append the data to the Google Sheet
worksheet.append_rows(values_to_update, value_input_option='USER_ENTERED')

