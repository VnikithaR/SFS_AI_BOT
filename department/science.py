from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Setup Chrome WebDriver (For Older Selenium Versions)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no UI)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # Alternative initialization

# Target URL
url = "https://www.sfscollege.in/bca_dep_of_sci.php"
driver.get(url)

# Wait for JavaScript to load content
time.sleep(5)  # Increase sleep time if needed

try:
    # Find the active tab-pane
    active_tab = driver.find_element("class name", "tab-pane.fade.active.show")

    # Find the target div inside the active tab
    activity_div = active_tab.find_element("class name", "col-lg-12.shadow.p-3.mb-5.bg-white.rounded")

    # Extract h3 and p tags
    h3_tags = activity_div.find_elements("tag name", "h3")
    p_tags = activity_div.find_elements("tag name", "p")

    activities = []

    # Pair h3 and p together
    for h3, p in zip(h3_tags, p_tags):
        activities.append({
            "name": h3.text.strip(),
            "detail": p.text.strip()
        })

    # Save data as JSON file
    with open("bca_activity.json", "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=4, ensure_ascii=False)

    print("✅ Scraping completed! Data saved in 'bca_activity.json'.")

except Exception as e:
    print(f"❌ Error: {e}")

# Close the browser
driver.quit()
