import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://www.sfscollege.in/naac.php"

# Send a GET request to fetch the webpage
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract main heading (if exists)
    heading = soup.find("h1").text.strip() if soup.find("h1") else "No Heading Found"

    # Extract all paragraphs under the NAAC content
    paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]

    # Extract any relevant links (such as NAAC accreditation PDF, if available)
    links = [a['href'] for a in soup.find_all("a", href=True) if "naac" in a['href'].lower()]

    # Structure data as JSON
    naac_data = {
        "heading": heading,
        "content": paragraphs,
        "links": links
    }

    # Convert to JSON format
    json_data = json.dumps(naac_data, indent=4)

    # Save to a JSON file
    with open("naac_data.json", "w") as file:
        file.write(json_data)

    print("Scraping completed. Data saved in naac_data.json")

else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
