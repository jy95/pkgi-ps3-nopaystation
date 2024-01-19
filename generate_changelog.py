import csv
from pathlib import Path
from datetime import date
from py_markdown_table.markdown_table import markdown_table

# Input / Output folder
OUTPUT_FOLDER = Path("output")
CHANGELOG_FILE = Path("CHANGELOG.md")

# define the files to use for the changelog
FILES = [
    {
        "name": "PS3_GAMES",
        "final": "pkgi_games.csv",
        "pending": "pkgi_games_pending.csv",
    },
    {
        "name": "PS3_DLCS",
        "final": "pkgi_dlcs.csv",
        "pending": "pkgi_dlcs_pending.csv",
    },
    {
        "name": "PS3_THEMES",
        "final": "pkgi_themes.csv",
        "pending": "pkgi_themes_pending.csv",
    },
    {
        "name": "PS3_AVATARS",
        "final": "pkgi_avatars.csv",
        "pending": "pkgi_avatars_pending.csv",
    },
    {
        "name": "PS3_DEMOS",
        "final": "pkgi_demos.csv",
        "pending": "pkgi_demos_pending.csv",
    }
]

# Count how many rows we have in a given file
def count_rows(filename):
    file = OUTPUT_FOLDER / filename
    count = 0
    
    try:
        with open(file, "rb") as csv_file:
            count = sum(1 for _line in csv_file)
    except Exception as error:
        print("An exception occurred:", error)
    finally:
        return count

with open(CHANGELOG_FILE, 'w') as out_file:
    
    today = date.today()
    formatted_date = today.strftime("%d %B %Y")
    
    # Write the summary
    summary = f"NoPayStation - release {formatted_date}\n\n"
    out_file.write(summary)
    
    # Parse each csv and compute its results
    data = []
    for entry in FILES:
        data.append({
            "Dataset": entry["name"],
            "Valid entries": count_rows(entry["final"]),
            "Pending entries": count_rows(entry["pending"]),
        })
    
    markdown = markdown_table(data).set_params(row_sep="markdown",padding_width=0,quote=False).get_markdown()
    out_file.write(markdown)

    