from bs4 import BeautifulSoup
import requests
import json

# Target URL
url = "https://www.sfscollege.in/ba_eco_poli_dept_of_hum.php"

# Send an HTTP request and parse HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all team-content divs
team_content_divs = soup.find_all("div", class_="team-content")

data = []

# Extract h4 (title) and span (title1)
for team in team_content_divs:
    name_tag = team.find("h4", class_="title")
    qualification_tag = team.find("span", class_="title1")

    if name_tag and qualification_tag:
        data.append({
            "name": name_tag.text.strip(),
            "qualification": qualification_tag.text.strip()
        })

# Save to JSON file
with open("faculty_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Scraping completed! Data saved in 'faculty_data.json'.")
