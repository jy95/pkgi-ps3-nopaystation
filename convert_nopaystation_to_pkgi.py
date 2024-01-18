import requests
import csv
from pathlib import Path

# Input / Output folder
INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")

# define the downloads
# content_type : https://github.com/bucanero/pkgi-ps3?tab=readme-ov-file#content-types
downloads = {
    "PS3_GAMES": {
        "input": "PS3_GAMES.tsv",
        "output": "pkgi_games.txt",
        "content_type": "1",
        "download_link": "https://nopaystation.com/tsv/PS3_GAMES.tsv"
    },
    "PS3_DLCS": {
        "input": "PS3_DLCS.tsv",
        "output": "pkgi_dlcs.txt",
        "content_type": "2",
        "download_link": "https://nopaystation.com/tsv/PS3_DLCS.tsv"
    },
    "PS3_THEMES": {
        "input": "PS3_THEMES.tsv",
        "output": "pkgi_themes.txt",
        "content_type": "3",
        "download_link": "https://nopaystation.com/tsv/PS3_THEMES.tsv"
    },
    "PS3_AVATARS": {
        "input": "PS3_AVATARS.tsv",
        "output": "pkgi_avatars.txt",
        "content_type": "4",
        "download_link": "https://nopaystation.com/tsv/PS3_AVATARS.tsv"
    },
    "PS3_DEMOS": {
        "input": "PS3_DEMOS.tsv",
        "output": "pkgi_demos.txt",
        "content_type": "5",
        "download_link": "https://nopaystation.com/tsv/PS3_DEMOS.tsv"
    },
}

# Create a function to format a row as per your specifications
# Title ID	Region	Name	PKG direct link	RAP	Content ID	Last Modification Date	Download .RAP file	File Size	SHA256
def format_row(row, content_type):
    content_id = row['Content ID']
    content_type = '1'  # Set type to 1 as constant
    name = f"{row['Name']} ({row['Region']})"
    description = ''  # Description is empty
    rap = row['RAP'] if 'RAP' in row else ''  # Leave empty if rap is not needed
    url = row['PKG direct link']
    size = row['File Size'] if 'File Size' in row else '0'  # Set size to 0 if unknown
    checksum = row.get('SHA256', '')  # Leave empty if checksum is not needed
    date = row['Last Modification Date']  # Extract DATE from "Last Modification Date"
    region = row['Region']  # Extract REGION from "Region"
    
    formatted_row = [content_id, content_type, name, description, rap, url, size, checksum, date, region]
    return formatted_row

# process a given item
def process_entries(item):
    input_file = INPUT_FOLDER / item["input"]
    output_file = OUTPUT_FOLDER / item["output"]
    
    # Download file and store it in file
    response = requests.get(item["download_link"], stream=True)
    
    with open(input_file, 'wb') as out_file:
         for chunk in response.iter_content(chunk_size=1024):
            out_file.write(chunk)

    # Read the TSV file and write to the CSV file with the specified format
    with open(input_file, 'r', newline='', encoding='utf-8') as tsvfile, open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        tsvreader = csv.DictReader(tsvfile, delimiter='\t')
        csvwriter = csv.writer(csvfile, delimiter=';')
        
        # Write the header row to the CSV file
        # csvwriter.writerow(['contentid', 'type', 'name', 'description', 'rap', 'url', 'size', 'checksum', 'date', 'region'])
        
        # Process and write the remaining rows
        for row in tsvreader:
            formatted_row = format_row(row)
            csvwriter.writerow(formatted_row)

for entry in downloads.items():
    (entryName, entryObj) = entry
    try:
        print(f"'{entryName}' - Processing ...")
        process_entries(entryObj)
    except Exception as error:
        print("An exception occurred:", error)