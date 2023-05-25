import csv
import ast
from collections import defaultdict

def extract_values(input_file, output_file):
    with open(input_file, 'r', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        headers = ['full_name', 'emails', 'gender', 'personal1', 'personal', 'professional', 'current_professional', 'null', 'none']

        # Use a set to keep track of unique row tuples
        unique_rows = set()

        for row in reader:
            emails = row.get('emails', '')

            # Parse the content of the 'emails' column
            email_list = []

            if emails:
                # Remove unnecessary characters and format the string as a list of dictionaries
                emails = emails.replace('[', '').replace(']', '')
                emails = emails.split(', {')

                for email in emails:
                    # Remove unnecessary characters and split the string into address and type
                    email = email.replace('{', '').replace('}', '')
                    address, email_type = email.split(', ')

                    # Create a dictionary for each email and add it to the list
                    email_dict = {'address': address.split('=')[1], 'type': email_type.split('=')[1]}
                    email_list.append(email_dict)

            # Create a dictionary to store email addresses for each type
            email_columns = defaultdict(list)

            # Assign email addresses to respective columns based on type
            for email in email_list:
                address = email.get('address', '')
                email_type = email.get('type', '')

                email_columns[email_type].append(address)

            # Convert the lists within email_columns to tuples
            email_columns = {k: tuple(v) for k, v in email_columns.items()}

            # Create a tuple of the row values with default values for missing columns
            row_values = [row.get(header, '') for header in headers]

            # Update the row values with email addresses for each email type
            for email_type, addresses in email_columns.items():
                if email_type in headers:
                    index = headers.index(email_type)
                    row_values[index] = addresses

            # Add the first email from 'personal' to 'personal1' if 'personal' is present
            if 'personal' in email_columns:
                personal_emails = email_columns['personal']
                if personal_emails:
                    row_values[headers.index('personal1')] = personal_emails[0]

            # Convert the row values to a tuple
            row_tuple = tuple(row_values)

            # Check if the row tuple is already in the set
            if row_tuple not in unique_rows:
                unique_rows.add(row_tuple)

    # Convert unique rows back to a list of dictionaries
    unique_rows_list = [dict(zip(headers, row_tuple)) for row_tuple in unique_rows]

    # Remove trailing commas from each column
    for row_dict in unique_rows_list:
        for key, value in row_dict.items():
            if isinstance(value, str):
                row_dict[key] = value.rstrip(',')

    with open(output_file, 'w', newline='', encoding='latin-1') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        # Write the unique rows to the output file
        writer.writerows(unique_rows_list)

    # Remove parentheses from the output file
    with open(output_file, 'r+', newline='', encoding='latin-1') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines:
            line = line.replace("(", "").replace(")", "").replace("'","")
            file.write(line)

# Example usage
input_file = 'data-original.csv'  # Replace with your input file name
output_file = 'output.csv'  # Replace with your desired output file name

extract_values(input_file, output_file)
