# https://api.nlt.to/Documentation
import requests
import dotenv
import os

dotenv.load_dotenv(".env")
API_KEY = os.getenv("NLT_API_KEY")

book = "James"
chapters = 5

for chapter in range(1, chapters + 1):
    # Define the directory and file paths
    directory_path = f"data/{book}"
    file_path = os.path.join(directory_path, f"chapter_{chapter}.html")

    # Step 1: Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    if not os.path.exists(file_path):
        query = f"https://api.nlt.to/api/passages?ref={book}.{chapter}&key={API_KEY}"
        result = requests.get(query)
        chapter_text = result.text

        with open(file_path, "w") as file:
            print(f"Writing to {file_path}...")
            file.write(chapter_text)
            print(f"Wrote to {file_path}")
        continue

    print(f"{file_path} already exists")
