import requests
import csv
from pathlib import Path

# --- Configuration ---
# Define the input and output folders for the files.
INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")

# A dictionary defining all the downloads and their configurations.
# Each entry specifies the input TSV file, the desired output CSV file,
# the content type code, and the download link.
downloads = {
    "PS3_GAMES": {
        "input": "PS3_GAMES.tsv",
        "output": "pkgi_games.csv",
        "content_type": "1",
        "download_link": "https://nopaystation.com/tsv/PS3_GAMES.tsv"
    },
    "PS3_DLCS": {
        "input": "PS3_DLCS.tsv",
        "output": "pkgi_dlcs.csv",
        "content_type": "2",
        "download_link": "https://nopaystation.com/tsv/PS3_DLCS.tsv"
    },
    "PS3_THEMES": {
        "input": "PS3_THEMES.tsv",
        "output": "pkgi_themes.csv",
        "content_type": "3",
        "download_link": "https://nopaystation.com/tsv/PS3_THEMES.tsv"
    },
    "PS3_AVATARS": {
        "input": "PS3_AVATARS.tsv",
        "output": "pkgi_avatars.csv",
        "content_type": "4",
        "download_link": "https://nopaystation.com/tsv/PS3_AVATARS.tsv"
    },
    "PS3_DEMOS": {
        "input": "PS3_DEMOS.tsv",
        "output": "pkgi_demos.csv",
        "content_type": "5",
        "download_link": "https://nopaystation.com/tsv/PS3_DEMOS.tsv"
    },
    "PS3_GAMES (pending)": {
        "input": "pending_PS3_GAMES.tsv",
        "output": "pkgi_games_pending.csv",
        "content_type": "1",
        "download_link": "https://nopaystation.com/tsv/pending/PS3_GAMES.tsv"
    },
    "PS3_DLCS (pending)": {
        "input": "pending_PS3_DLCS.tsv",
        "output": "pkgi_dlcs_pending.csv",
        "content_type": "2",
        "download_link": "https://nopaystation.com/tsv/pending/PS3_DLCS.tsv"
    },
    "PS3_THEMES (pending)": {
        "input": "pending_PS3_THEMES.tsv",
        "output": "pkgi_themes_pending.csv",
        "content_type": "3",
        "download_link": "https://nopaystation.com/tsv/pending/PS3_THEMES.tsv"
    },
    "PS3_AVATARS (pending)": {
        "input": "pending_PS3_AVATARS.tsv",
        "output": "pkgi_avatars_pending.csv",
        "content_type": "4",
        "download_link": "https://nopaystation.com/tsv/pending/PS3_AVATARS.tsv"
    },
    "PS3_DEMOS (pending)": {
        "input": "pending_PS3_DEMOS.tsv",
        "output": "pkgi_demos_pending.csv",
        "content_type": "5",
        "download_link": "https://nopaystation.com/tsv/pending/PS3_DEMOS.tsv"
    },
}

# --- Functions ---

def format_row(row: dict, content_type: str) -> list:
    """
    Formats a single row from the TSV data into the required CSV format.

    Args:
        row: A dictionary representing a single row from the TSV file.
        content_type: The content type code for the item.

    Returns:
        A list of strings representing the formatted row.
    """
    # The required output format is:
    # contentid;type;name;description;rap;url;size;checksum;date;region
    # Note: Using .get() with a default value prevents a KeyError if a column is missing.
    content_id = row.get('Content ID', '')
    name = f"{row.get('Name', '')} ({row.get('Region', '')})"
    description = ''
    rap = row.get('RAP', '')
    url = row.get('PKG direct link', '')
    size = row.get('File Size', '0')
    checksum = row.get('SHA256', '')
    date = row.get('Last Modification Date', '')
    region = row.get('Region', '')

    formatted_row = [content_id, content_type, name, description, rap, url, size, checksum, date, region]
    return formatted_row

def process_entry(item: dict):
    """
    Downloads a TSV file and converts it to a formatted CSV file.

    Args:
        item: A dictionary containing the configuration for a single download.
    """
    input_file = INPUT_FOLDER / item["input"]
    output_file = OUTPUT_FOLDER / item["output"]
    content_type = item["content_type"]
    download_link = item["download_link"]

    print(f"  Downloading from '{download_link}'...")
    try:
        response = requests.get(download_link, stream=True)
        # Raise an HTTPError if the status code is not 200 (OK)
        response.raise_for_status()

        # Download the file in chunks to be memory-efficient
        with open(input_file, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)

        print(f"  Downloaded to '{input_file}'. Converting to CSV...")

    except requests.exceptions.RequestException as e:
        print(f"  Failed to download file: {e}")
        return  # Exit the function if download fails

    try:
        # Read the TSV file and write to the CSV file with the specified format
        with open(input_file, 'r', newline='', encoding='utf-8') as tsvfile, \
             open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            
            # Use DictReader for TSV, specifying the tab delimiter
            tsvreader = csv.DictReader(tsvfile, delimiter='\t')
            # Use writer for CSV, specifying the semicolon delimiter
            csvwriter = csv.writer(csvfile, delimiter=';')

            # Define and write the header row for the output CSV file.
            #header = ['contentid', 'type', 'name', 'description', 'rap', 'url', 'size', 'checksum', 'date', 'region']
            #csvwriter.writerow(header)

            # Process each row and write the formatted data to the CSV
            for row in tsvreader:
                formatted_row = format_row(row, content_type)
                csvwriter.writerow(formatted_row)
        
        print(f"  Conversion complete. Saved to '{output_file}'.")

    except (IOError, csv.Error) as e:
        print(f"  Failed to process file: {e}")


# --- Main Execution ---

if __name__ == "__main__":
    # Create the input and output directories if they don't exist
    # Using `exist_ok=True` prevents an error if the directories already exist.
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    print("Starting TSV to PKGi CSV conversion process...")
    
    # Iterate over each item in the downloads dictionary and process it
    for entry_name, entry_data in downloads.items():
        print(f"\nProcessing '{entry_name}'...")
        process_entry(entry_data)
    
    print("\nAll downloads and conversions are complete.")
