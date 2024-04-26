import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

# Base URL
base_url = "https://www.erasmushogeschool.be/nl/opleidingen"

# Make a request to the website
r = requests.get(base_url)
r.content

# Use the 'html.parser' to parse the page
soup = BeautifulSoup(r.content, 'html.parser')

# Find all links on page
links = soup.findAll('a')

# Filter the links
filtered_links = []
for link in links:
    href = link.get('href')
    # select the relative links to 'opleidingen'
    if href and href.startswith('/nl/opleidingen/'):
        full_url = urljoin(base_url, href)  # Join the base URL with the relative URL
        if full_url not in filtered_links:
            filtered_links.append(full_url)
    # select the absolute links 1 level deeper than 'https://www.erasmushogeschool.be/nl/'
    elif href and href.startswith('https://www.erasmushogeschool.be/nl/') and not href.startswith('https://www.erasmushogeschool.be/nl/opleidingen')  and href.count('/') == 4:
        if href not in filtered_links:
            filtered_links.append(href)


# save the links to html files
for link in tqdm(filtered_links):
    # Make a request to the website
    r = requests.get(link)

    # Use the 'html.parser' to parse the page
    soup = BeautifulSoup(r.content, 'html.parser')

    # generate the file name
    file_name = link.replace('https://www.erasmushogeschool.be/nl/', '').replace('/', '_') + '.html'

    # Write the parsed content to a file
    with open(f"erasmus-site-parsed/{file_name}", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))