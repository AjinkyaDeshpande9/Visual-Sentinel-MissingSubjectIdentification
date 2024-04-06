import pandas as pd
import difflib

# Read the valid data CSV file into a pandas DataFrame
valid_df = pd.read_csv('static\\uploads\\valid_data.csv')

#Function to search for matches in the DataFrame
def search_matches(input_string):
    matches = []
    for index, row in valid_df.iterrows():
        combined_class_names = row['Combined Class Names']
        # Calculate similarity ratio between the input string and combined class names
        similarity_ratio = difflib.SequenceMatcher(None, input_string, combined_class_names).ratio()
        # If similarity ratio is above 70%, add it to the matches list
        if similarity_ratio > 0.7:
            matches.append((row['Path'], combined_class_names, similarity_ratio))
    return matches


# Function to take user input and search for matches
def main(lpnumber):
    matches = search_matches(lpnumber)
    if matches:
        print("Matches found:")
        for match in matches:
            print(f"Path: {match[0]}, Combined Class Names: {match[1]}, Similarity Ratio: {match[2]}")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
