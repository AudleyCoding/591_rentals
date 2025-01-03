Here's a draft README file based on the information you've provided so far. If anything is missing or incorrect, let me know, and I can refine it further.

---

# Real Estate Scraper & Notifier

## Overview

This project is a Python-based web scraper designed to fetch and filter real estate listings from multiple websites (or URLs). The scraper checks if new listings meet specific criteria (updated within the last 6 hours) and sends notifications for new listings via LINE Notify. The project is modular, making it easy to customize, extend, and maintain.

---

## Features

- Scrapes listings from multiple `BASE_URL`s specified in a `.env` file.
- Filters listings based on the update time (e.g., within the last 6 hours).
- Avoids sending duplicate notifications by maintaining a database of previously notified listings.
- Sends customizable notifications via LINE Notify.
- Modular architecture:
  - `scrape591.py`: Handles scraping and filtering.
  - `database.py`: Manages the database of links.
  - `notify591.py`: Sends notifications via LINE Notify.
  - `main.py`: Entry point for the program.

---

## Setup Instructions

### Prerequisites

1. **Python Version**: Ensure you have Python 3.8 or later installed.
2. **Dependencies**: Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment File**: Create a `.env` file with the following variables:
   ```plaintext
   BASE_URL_1=https://example.com/storefronts-for-rent?page={}
   BASE_URL_2=https://example.com/storefronts-for-sale?page={}
   BASE_URL_3=https://example.com/apartments?page={}
   LINE_NOTIFY_TOKEN=your_line_notify_token
   ```

### Database
The database is a simple text file (`scraped_links.txt`) stored in the project directory. This file keeps track of links already notified to avoid duplicates.

---

## Usage

1. **Run the Scraper**:
   Execute the main script to start scraping and sending notifications:
   ```bash
   python main.py
   ```

2. **Notifications**:
   New listings meeting the criteria will trigger a LINE Notify message based on the `BASE_URL`:
   - **BASE_URL_1**: 🏠 New Storefronts for RENT.
   - **BASE_URL_2**: 🏠 New Storefronts for SALE.
   - **BASE_URL_3**: 🏠 New APARTMENTS.

---

## File Structure

- **`main.py`**: Entry point for running the scraper and notifier.
- **`scrape591.py`**: Core logic for scraping and filtering listings.
- **`notify591.py`**: Contains functionality for sending LINE Notify messages.
- **`database.py`**: Handles loading, saving, and checking the database of previously scraped links.
- **`requirements.txt`**: List of dependencies.
- **`.env`**: Environment file for storing `BASE_URL` and `LINE_NOTIFY_TOKEN`.

---

## Extending the Project

1. **Add More URLs**:
   - Add new `BASE_URL_n` keys to the `.env` file.
   - Add corresponding messages to the `BASE_URL_MESSAGES` dictionary in `scrape591.py`.

2. **Custom Filtering**:
   - Modify the `parse_update_time` or `parse_house` functions in `scrape591.py` to implement new criteria.

3. **Database Updates**:
   - The current database is a simple text file. Replace it with a more robust database (e.g., SQLite or MongoDB) if needed.

---

## Troubleshooting

- **No Listings Found**:
  - Verify the `BASE_URL` structure and ensure it's correctly formatted with a `{}` placeholder for pagination.
  - Inspect the HTML structure of the target site and adjust the `fetch_houses` or `parse_house` logic.

- **LINE Notifications Not Working**:
  - Ensure the `LINE_NOTIFY_TOKEN` in `.env` is valid.
  - Check for network connectivity issues.

---

## License

This project is released under the [MIT License](LICENSE).

---

## Contributions

Feel free to submit issues or pull requests to improve the scraper or add new features.

---

Does this cover everything you need, or would you like to add more details?