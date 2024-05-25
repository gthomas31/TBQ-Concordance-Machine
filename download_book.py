# https://api.nlt.to/Documentation
import requests
import dotenv
import os

dotenv.load_dotenv(".env")
API_KEY = os.getenv("NLT_API_KEY")

book = "Romans"
chapters = 1

for chapter in range(1, chapters + 1):
    query = f"https://api.nlt.to/api/passages?ref={book}.{chapter}&key={API_KEY}"
    result = requests.get(query)
    chapter_text = result.text

    # Define the directory and file paths
    directory_path = f"data/{book}"
    file_path = os.path.join(directory_path, f"chapter_{chapter}.txt")

    # Step 1: Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    with open(file_path, "w") as file:
        file.write(chapter_text)
