import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://www.sfscollege.in/"

# Headers to mimic a real browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# Sending a request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Example: Get the page title
    title = soup.title.text
    print("Page Title:", title)

    # Example: Get all links on the homepage
    links = [a["href"] for a in soup.find_all("a", href=True)]
    print("\nLinks Found on the Homepage:")
    for link in links:
        print(link)

    # Example: Extract all headings (h1, h2, h3)
    headings = {f"h{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 4)}
    print("\nHeadings Found:")
    for tag, texts in headings.items():
        if texts:
            print(f"{tag}: {texts}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
