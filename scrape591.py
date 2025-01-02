import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for pagination
BASE_URL = os.getenv("BASE_URL")

# Custom Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

def fetch_houses(page):
    """Fetch house listings from the given page."""
    if not BASE_URL:
        print("Error: BASE_URL is not set in the environment.")
        return []

    response = requests.get(BASE_URL.format(page), headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all('div', class_='item-info')  # Adjust the class as needed based on actual HTML
    else:
        print(f"Failed to fetch page {page}, status code: {response.status_code}")
        return []

def parse_update_time(update_text):
    """Determine if the house was updated within 6 hours based on the text."""
    if "分鐘內更新" in update_text:
        return True  # Always within 6 hours
    elif "小時內更新" in update_text:
        hours = int(update_text.split("小時內更新")[0])
        return hours <= 6
    elif "天前更新" in update_text:
        return False  # Always longer than 6 hours
    return False

def parse_house(house):
    """Parse a single house listing for its details."""
    try:
        link = house.find('a', class_='link v-middle').get('href', None)
        update_span = house.find('span', class_='line', string=lambda x: x and "更新" in x)

        if not update_span:
            return None  # No update time found

        update_text = update_span.text.strip()
        if parse_update_time(update_text):
            return link  # Return link if updated within 6 hours
    except Exception as e:
        print(f"Error parsing house: {e}")
        return None

def scrape_all_pages():
    """Scrape all pages and collect house links updated within 6 hours."""
    page = 1
    filtered_links = []

    while True:
        print(f"Fetching page {page}...")
        houses = fetch_houses(page)

        if not houses:
            print(f"No houses found on page {page}. Stopping.")
            break

        for house in houses:
            link = parse_house(house)
            if link:
                filtered_links.append(link)

        page += 1  # Go to the next page

    return filtered_links
