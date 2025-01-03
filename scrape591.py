import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from database import load_links, save_links, is_new_link
from notify591 import send_line_message



# Load environment variables from .env file
load_dotenv()

# Get all BASE_URLs
BASE_URLS = {key: value for key, value in os.environ.items() if key.startswith("BASE_URL_")}

# Custom messages for each BASE_URL
BASE_URL_MESSAGES = {
    "BASE_URL_1": "🏠 New Storefronts for RENT.\n",
    "BASE_URL_2": "🏠 New Storefronts for SALE\n",
    "BASE_URL_3": "🏠 New APARTMENTS.\n",
}

# Custom Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}
# Validate consistency between BASE_URL keys and BASE_URL_MESSAGES
def validate_base_url_messages():
    """Ensure every BASE_URL key has a corresponding custom message."""
    for base_url_key in BASE_URLS.keys():
        if base_url_key not in BASE_URL_MESSAGES:
            BASE_URL_MESSAGES[base_url_key] = "🏠 Forgot custom msg for this URL's listings.:n"

validate_base_url_messages()

def fetch_houses(base_url, page):
    """Fetch house listings from the given page."""
    response = requests.get(base_url.format(page), headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all('div', class_='item-info')  # Adjust the class as needed based on actual HTML
    else:
        print(f"Failed to fetch page {page} from {base_url}, status code: {response.status_code}")
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

def scrape_for_url(base_url_key, base_url):
    """
    Scrape all pages for a specific BASE_URL and notify about new listings.
    
    Parameters:
    - base_url_key: The key identifying the BASE_URL in the environment.
    - base_url: The BASE_URL to scrape.
    """
    page = 1
    filtered_links = []
    existing_links = load_links()

    while True:
        print(f"Fetching page {page} from {base_url}...")
        houses = fetch_houses(base_url, page)

        if not houses:
            print(f"No houses found on page {page} for {base_url}. Stopping.")
            break

        for house in houses:
            link = parse_house(house)
            if link and is_new_link(link, existing_links):
                filtered_links.append(link)
                message = BASE_URL_MESSAGES.get(base_url_key, "🏠 New rental listing:\n") + link
                send_line_message(message)

        page += 1
    
    # Save new links to the database
    if filtered_links:
        save_links(filtered_links)

def scrape_all_sites():
    """
    Iterate through all BASE_URLs in the environment and scrape each site for new listings.
    """
    for base_url_key, base_url in BASE_URLS.items():
        scrape_for_url(base_url_key, base_url)
