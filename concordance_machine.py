import os
import glob
from typing import Mapping, List, Tuple
from bs4 import BeautifulSoup
import re
from verse import Verse


class ConcordanceMachine:

    def __init__(self, books: List[str]):
        self.books: list = books
        self.html_files: Mapping[str: List[Tuple[int, str]]] = {}
        self.section_titles: Mapping[Tuple[str, int]: List[str]] = {}
        for book in books:
            self.html_files[book] = []
        self.verses: Mapping[Tuple[str, int]: List[Verse]] = {}

        self.concordance: Mapping[str: Tuple[int, List[Tuple[str, int]]]] = {}
        self.phrase_concordance: Mapping[str: Tuple[int, List[Tuple[str, int]]]] = {}

    def get_html_files(self):
        for book in self.books:
            # Define the directory path
            directory_path = f"data/{book}"

            # Get a list of all files in the directory
            file_list = glob.glob(os.path.join(directory_path, '*'))

            # Loop through each file in the list
            for file_path in file_list:
                chapter_number = int(file_path[file_path.index("chapter_") + 8:file_path.index(".html")])
                self.html_files[book].append((chapter_number, file_path))

    def read_html_files(self):
        for book in self.books:
            html_files_list = self.html_files[book]
            html_files_list.sort()
            for chapter, file_path in html_files_list:
                with open(file_path, "r") as file:
                    html_text = file.read()
                    self.verses[(book, chapter)] = self.process_html_file(html_text=html_text, book=book, chapter=chapter)

    def process_html_file(self, html_text: str, book: str, chapter: int) -> List[Verse]:
        soup = BeautifulSoup(html_text, "html.parser")
        print(f"Processing {book} {chapter}...")

        section = soup.find('div', id='bibletext')

        verses = []

        for verse_export in section.find_all('verse_export'):
            # Remove footnotes
            for tag in verse_export.find_all(['a', 'span'], class_=['a-tn', 'tn', 'tn-ref']):
                tag.decompose()
            # Extract verse number and text
            verse_number = verse_export.find('span', class_='vn').text.strip()
            print(verse_number)
            # verse_text = verse_export.text.strip().replace(verse_number, '', 1).strip()
            # Find the section title associated with this verse
            verse_texts = []
            for text in verse_export.find_all('p', class_='body-ch-hd'):
                verse_texts.append(text.text.strip().replace(verse_number, '', 1).strip())
            for text in verse_export.find_all('p', class_='body-hd'):
                verse_texts.append(text.text.strip().replace(verse_number, '', 1).strip())
            for text in verse_export.find_all('p', class_='body'):
                verse_texts.append(text.text.strip().replace(verse_number, '', 1).strip())
            if not verse_texts:
                verse_texts = [verse_export.text.strip().replace(verse_number, '', 1).strip()]
            verse_text = " ".join(verse_texts)
            print(verse_text)

            try:
                section_title = verse_export.find('h3', class_='subhead').text.strip()
            except AttributeError:
                try:
                    section_title = verse_export.find_previous('h3', class_='subhead').text.strip()
                except AttributeError:
                    if chapter == 1:
                        section_title = f"The Untitled Section of {book}"
                    else:
                        # Grab the last section title of the previous chapter
                        section_title = self.section_titles[(book, chapter - 1)][-1]
            try:
                self.section_titles[(book, chapter)].append(section_title)
            except KeyError:
                self.section_titles[(book, chapter)] = [section_title]
            print(section_title)
            # Add verse number, text, and section to the dictionary
            new_verse = Verse(book, chapter, verse_number, section_title, verse_text)
            verses.append(new_verse)

        return verses

    def generate_concordance(self):
        for book, chapter in self.verses:
            verses = self.verses[(book, chapter)]
            # Iterate through each Verse object
            for verse in verses:
                # Tokenize the text of the verse into words
                words = re.findall(r"\b[\w'’]+\b",
                                   verse.text.upper())  # Using regex to split by word boundaries and convert to uppercase
                # unique_words = set(words)  # Get unique words in the verse

                phrases = []
                # Generate all possible phrases
                for start in range(len(words)):
                    for end in range(start + 2, len(words) + 1):
                        phrase = " ".join(words[start:end]).strip()
                        phrases.append(phrase)

                # Increment the count of verses each word appears in
                for word in words:
                    try:
                        count, references = self.concordance[word]
                        count += 1
                        references.append((book, chapter, verse.verse))
                        self.concordance[word] = [count, references]
                    except KeyError:
                        self.concordance[word] = (1, [(book, chapter, verse.verse)])

                for phrase in phrases:
                    try:
                        count, references = self.phrase_concordance[phrase]
                        count += 1
                        references.append((book, chapter, verse.verse))
                        self.phrase_concordance[phrase] = [count, references]
                    except KeyError:
                        self.phrase_concordance[phrase] = (1, [(book, chapter, verse.verse)])

    def print_concordance(self, type="word"):
        concordance = self.concordance
        if type == "phrase":
            concordance = self.phrase_concordance
        words = []
        for word in concordance:
            words.append((concordance[word][0], word))

        words.sort()
        for count, word in words:
            if count != 1:
                print(f"{word}: {count}")