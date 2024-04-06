import pandas as pd
import string

# Conversion dictionaries
dict_char_to_int = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5'}
dict_int_to_char = {'0': 'O', '1': 'I', '3': 'J', '4': 'A', '6': 'G', '5': 'S'}

# Function to convert string according to conversion dictionaries and provided mapping
def format_license(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_char_to_int,
               2: dict_char_to_int, 3: dict_char_to_int, 7: dict_char_to_int, 8: dict_char_to_int, 9: dict_char_to_int}

    for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

# Function to check if the string follows the specified format and perform conversions if necessary
def check_and_convert_format(text):
    if len(text) != 10:
        return False

    for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if text[j] in dict_char_to_int.keys():
            text = text[:j] + dict_char_to_int[text[j]] + text[j+1:]
        elif text[j] in dict_int_to_char.keys():
            text = text[:j] + dict_int_to_char[text[j]] + text[j+1:]

    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
       (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[6] in dict_char_to_int.keys()) and \
       (text[7] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[7] in dict_char_to_int.keys()) and \
       (text[8] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[8] in dict_char_to_int.keys()) and \
       (text[9] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[9] in dict_char_to_int.keys()):
        return True
    else:
        return False

def process_csv(csv_file_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert the 'box_coord' column from string to list
    df['box_coord'] = df['box_coord'].apply(eval)

    # Sort the DataFrame by the first coordinate in 'box_coord'
    df = df.iloc[df['box_coord'].apply(lambda x: x[0][0]).argsort()]

    # Group the DataFrame by 'path' and aggregate the 'class_name' column into a single string
    grouped = df.groupby('path')['class_name'].apply(lambda x: ' '.join(x))

    # Initialize a list to store valid data
    valid_data = []

    # Process and append the valid data to the list
    for path, class_names in grouped.items():
        combined_string = class_names.replace(" ", "")
        if check_and_convert_format(combined_string):
            combined_string = format_license(combined_string)  # Applying the conversion
            valid_data.append({'Path': path, 'Combined Class Names': combined_string})

    # Create a DataFrame from the valid data
    valid_df = pd.DataFrame(valid_data)

    # Save the DataFrame to a new CSV file
    valid_df.to_csv('static\\uploads\\valid_data.csv', index=False)


