# --- File: scrape.py ---

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Target URLs ---
URLS = [
    "https://www.epassport.gov.bd/instructions/five-step-to-your-epassport",
    "https://www.epassport.gov.bd/instructions/urgent-applications",
    "https://www.epassport.gov.bd/instructions/passport-fees",
]

def setup_driver():
    """Initializes the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_page_content(url, driver):
    """Fetches page content using Selenium and extracts text using BeautifulSoup."""
    try:
        driver.get(url)

        time.sleep(2)

        html_content = driver.page_source

    except Exception as e:
        print(f"Error loading page {url} with Selenium: {e}")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    content_area = soup.find('div', class_='wrapper wrapper--margined') # Adjust based on site inspection

    if not content_area:
        content_area = soup.find('body')

    text_blocks = []
    for element in content_area.find_all(['p', 'li', 'h2', 'h3', 'h4']):
        text = element.get_text(strip=True)
        if text:
            text_blocks.append(text)

    page_title = soup.title.string if soup.title else "Untitled"
    return {"content": "\n".join(text_blocks), "source_url": url, "title": page_title}

def get_all_data():
    """Initializes driver and scrapes all target URLs."""
    driver = setup_driver()
    all_documents = []
    for url in URLS:
        print(f"Scraping {url}...")
        data = scrape_page_content(url, driver)
        if data:
            all_documents.append(data)
    driver.quit()
    return all_documents

if __name__ == "__main__":
    documents = get_all_data()
    print(f"\nSuccessfully scraped {len(documents)} pages.")
    if documents:
        print("\n--- Example content snippet ---")
        print(f"Source: {documents[0]['source_url']}")
        print(documents[0]["content"][:500] + "...")