import pandas as pd
import sqlite3
import os

# Define the pipeline
def process_csv(input_file, output_file, db_file, table_name):
    # Step 1: Load the CSV file
    df = pd.read_csv(input_file)
    print("Original DataFrame:\n", df.head())
    
    # Step 2: Delete rows 1 to 5 (Indexing in pandas starts at 0)
    df = df.drop(index=range(0, 4))
    print("After deleting rows 1-5:\n", df.head())
    
    # Step 3: Delete the first column
    df = df.iloc[:, 1:]
    print("After deleting the first column:\n", df.head())

    # Step 4: Remove space in text from a cell on the first row in the third column
    df.iat[0, 2] = df.iat[0, 2].replace(" ", "")
    print("After removing spaces from the cell in the first row, third column:\n", df.head())

    # Step 5: Set the headers to be the values in the first row
    df.columns = df.iloc[0]
    df = df[1:]
    print("After setting the first row as headers:\n", df.head())
    
    # Step 4: Save the modified data to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Modified data saved to {output_file}")
    
    # Step 5: Load the data into an SQLite database
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Data loaded into SQLite database table: {table_name}")
    conn.close()

# Prompt for file paths and database configuration
input_csv = input("Enter the name of the input CSV file: ")
output_csv = os.path.basename(input_csv)
sqlite_db = "ownership.db"  # Fixed database file name

# Extract the table name from the input file name without the extension
table_name = os.path.splitext(os.path.basename(input_csv))[0]

# Run the pipeline
process_csv(input_csv, output_csv, sqlite_db, table_name)
