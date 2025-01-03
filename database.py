import os

DATABASE_FILE = "scraped_links.txt"

def load_links():
    """Load scraped links from the database file."""
    if not os.path.exists(DATABASE_FILE):
        return set()  # Return an empty set if file doesn't exist
    try:
        with open(DATABASE_FILE, "r") as file:
            return set(line.strip() for line in file if line.strip())
    except Exception as e:
        print(f"Error loading database: {e}. Starting fresh.")
        return set()

def save_links(links):
    """Save a batch of links to the database file."""
    try:
        with open(DATABASE_FILE, "a") as file:
            for link in links:
                file.write(f"{link}\n")
    except Exception as e:
        print(f"Error saving links to database: {e}")

def is_new_link(link, existing_links):
    """Check if a link is new."""
    return link not in existing_links
