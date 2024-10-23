import os
import time
import json
import argparse
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By

class TikTokScraper:
    def __init__(self, cookie, scrape_count, output_file, profile):
        self.cookie = cookie
        self.scrape_count = scrape_count
        self.output_file = output_file
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.profile = profile

    def convert(self, data):
        # Check if the file exists
        if os.path.exists(self.output_file):
            # If file exists, read the existing data
            try:
                with open(self.output_file, 'r') as infile:
                    existing_data = json.load(infile)
            except json.JSONDecodeError:
                print("Error decoding existing JSON, initializing an empty list.")
                existing_data = []
        else:
            # If file doesn't exist, initialize an empty list
            existing_data = []
        
        # Ensure existing_data is a list before appending
        if not isinstance(existing_data, list):
            print("Existing data is not a list, initializing an empty list.")
            existing_data = []
        
        # Append the new data (user_list) to the existing data
        existing_data.extend(data)
        
        # Write the combined data back to the file
        with open(self.output_file, 'w') as outfile:
            json.dump(existing_data, outfile, indent=4)

        print(f"Data successfully written to {self.output_file}")

    def scrape(self):
        print("Scraping data...")
        for i in range(len(self.driver.requests)-1, -1, -1):
            request = self.driver.requests[i]
            if "https://www.tiktok.com/api/user/list/?WebIdLastTime" in request.url and request.response:
                print(f"URL: {request.url}")
                body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                data = body.decode("utf8")
                response_json = json.loads(data)
                user_list = response_json.get('userList', [])
                self.convert(user_list)
                break

    def interceptor(self, request):
        # Add the missing headers
        request.headers["sec-fetch-mode"] = "cors"
        request.headers["cookie"] = self.cookie

    def run(self):
        self.driver.request_interceptor = self.interceptor
        self.driver.get(self.profile)
        time.sleep(5)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/h3/div[2]/span').click()
        time.sleep(5)

        modal = self.driver.find_element(By.XPATH, '/html/body/div[9]/div/div[2]/div/div/div[2]/div/div/section/div/div[3]')

        while self.scrape_count:
            try:
                # Scroll to load more data in the modal
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)  # Pause for the scroll to load content
                self.scrape()
                self.scrape_count -= 1
            except Exception as e:
                print(f"Error during scrolling: {e}")
                break  # Break the loop if scrolling fails, but retain collected data

        self.driver.quit()

if __name__ == "__main__":
    # CLI argument parsing
    parser = argparse.ArgumentParser(description='TikTok scraper with Selenium.')
    parser.add_argument('--cookie', type=str, required=True, help='Cookie string for authentication')
    parser.add_argument('--scrape', type=int, required=True, help='Number of times to scroll and scrape data')
    parser.add_argument('--output', type=str, required=True, help='Output file for scraped data')
    parser.add_argument('--profile', type=str, required=True, help='Tiktok profile to scrape from')

    args = parser.parse_args()

    # Instantiate the scraper and run it
    scraper = TikTokScraper(cookie=args.cookie, scrape_count=args.scrape, output_file=args.output, profile=args.profile)
    scraper.run()
