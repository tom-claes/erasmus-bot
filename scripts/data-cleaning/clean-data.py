# Importeer de nodige libraries
import os
import json
import re
from bs4 import BeautifulSoup


# slaag de nodige data op in een dictionary en maak de html pagina klaar voor scraping
def parse_html(file_path):
    # Open het bestand en lees het uit met UTF-8 codering
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Maak een BeautifulSoup object van de inhoud van het bestand door de html.parser te gebruiken
    soup = BeautifulSoup(content, 'html.parser')

    # Slaag metadata mee op
    for course in soup:
        # Haal de titel, de url en de beschrijving van de cursus op
        title = soup.find('h1', class_='page-header').text.strip().lower()
        source = soup.find('link', rel='canonical')['href'] if soup.find('link', rel='canonical') else None
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None

        # Voeg de titel, de url en de beschrijving toe aan de lijst van cursussen
        course = {
            'title': title,
            'source': source,
            'description': description,
            'content': soup.prettify()
        }

    return [course]


def clean_data(data):
    cleaned_data = []

    for item in data:
        for field in ['title', 'description', 'content']:
            key = item[field]

            # Create a BeautifulSoup object from the content of the field
            soup = BeautifulSoup(key, 'html.parser')

            # Remove all unnecessary things and save the clean text in the item
            cleaned_text = soup.get_text().replace('\n', '').replace('\xa0', ' ').replace('\u00AD', '').replace('\u200b', '').replace('\u2009', ' ').replace('\u0081', ' ')
            cleaned_text = re.sub(' +', ' ', cleaned_text).strip()

            if field == 'content':
                tokens = cleaned_text.split()
                num_tokens = len(tokens)

                if num_tokens > 3000:
                    chunks = num_tokens // 3000
                    if num_tokens % 3000 != 0:
                        chunks += 1
                else:
                    chunks = 1

                chunk_size = min(num_tokens // chunks, 3000)
                chunks = [' '.join(tokens[i:i + chunk_size]) for i in range(0, num_tokens, chunk_size)]

                for chunk in chunks:
                    cleaned_item = item.copy()
                    cleaned_item[field] = chunk
                    cleaned_data.append(cleaned_item)
            else:
                item[field] = cleaned_text

    return cleaned_data


def main():
    # Definieer de directory waar de HTML-bestanden zich bevinden
    data_directory = '../../erasmus-site-parsed/'
    # Initialiseer een lege list om alle cursussen in op te slaan
    all_courses = []

    # Loop over all files in the data directory
    for filename in os.listdir(data_directory):
        # Check of het bestand een HTML-bestand is
        if filename.endswith('.html'):
            # Definieer het volledige pad naar het bestand
            file_path = os.path.join(data_directory, filename)
            try:
                print(f"Opening file: {file_path}")  # Print het pad naar het bestand
                # Parse het HTML-bestand en voeg de resultaten toe aan de all_courses list
                all_courses.extend(parse_html(file_path))
            except Exception as e:
                # Als er een fout optreedt, print dan een foutmelding en ga verder met het volgende bestand
                print(f"Error reading file {file_path}: {e}")
                continue

    # Clean de data (bijv. verwijder extra spaties) en sla de resultaten op in een nieuwe variabele
    cleaned_data = clean_data(all_courses)

    # Sla de propere data op in een JSON-bestand
    with open('cleaned_data.json', 'w', encoding='utf-8') as json_file:
        # Dump de data naar het JSON-bestand
        json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
