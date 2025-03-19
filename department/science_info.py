import requests
import json
from bs4 import BeautifulSoup

# URL of the BCA department page
url = "https://www.sfscollege.in/bsc_dept_of_sci.php"

# Headers to mimic a real browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# Send request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the "get-to-know-content" div
    content_section = soup.find("div", class_="get-to-know-content")

    # Dictionary to store extracted data
    bca_info = {
        "Program Details": "",
        "Application Process": "",
        "Eligibility": "",
        "Admission Process": "",
        "Fees Structure": "",
        "Syllabus": "",
        "Question Papers": ""
    }

    if content_section:
        # Get all <p> tags inside the "get-to-know-content" div
        paragraphs = content_section.find_all("p")

        # Assign the extracted <p> content to relevant keys (modify order if needed)
        keys = list(bca_info.keys())
        
        for i, paragraph in enumerate(paragraphs):
            if i < len(keys):  # Ensure we don't go out of index range
                bca_info[keys[i]] = paragraph.text.strip()

    # Save to JSON file
    with open("bca_info.json", "w", encoding="utf-8") as f:
        json.dump(bca_info, f, indent=4, ensure_ascii=False)

    print("BCA program details successfully saved in bca_info.json")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
