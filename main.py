from scrape591 import scrape_all_pages
from notify591 import send_links_via_line

def main():
    # Replace with your Line Notify token
    # LINE_TOKEN = "YOUR_LINE_NOTIFY_TOKEN"
    # notifier = send_links_via_line(LINE_TOKEN)

    # Scrape house links
    house_links = scrape_all_pages()

    if house_links:
        print(f"\nFound {len(house_links)} houses updated within the last 6 hours.")
        for link in house_links:
            print(f"Link: {link}")
        
        # Send the links via LINE
        send_links_via_line(house_links)
    else:
        print("No houses updated within the last 6 hours.")

if __name__ == "__main__":
    main()

