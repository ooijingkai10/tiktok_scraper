import os
import time
import json
import argparse
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By

class TikTokScraper:
    def __init__(self, cookie, scrape_count, output_dir, profile):
        self.cookie = cookie
        self.scrape_count = scrape_count
        self.output_dir = output_dir
        self.profile = profile
        self.user_list = []  # Temporary storage for user data
        self.file_counter = 0  # To keep track of the output file number
        self.users_per_file = 900  # Number of users per file

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Setup the WebDriver
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def convert(self):
        # Create a new file for every 900 users
        if len(self.user_list) >= self.users_per_file:
            output_file = os.path.join(self.output_dir, f"follower_list_{self.file_counter}.json")
            with open(output_file, 'w') as outfile:
                json.dump(self.user_list, outfile, indent=4)
            print(f"Data successfully written to {output_file}")
            self.file_counter += 1  # Increment the file counter
            self.user_list = []  # Reset the temporary user list

    def scrape(self):
        print("Scraping data...")
        # Define the target URL
        target_url = "https://www.tiktok.com/api/user/list/?WebIdLastTime"
        # Loop through requests in reverse order
        for request in reversed(self.driver.requests):
            
            if target_url in request.url and request.response:
                print(f"Checking request: {request.url}")
                body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                data = body.decode("utf8")
                response_json = json.loads(data)
                # Extend user list with new users
                self.user_list.extend(response_json.get('userList', []))
                self.convert()
                break  # Exit after finding the first match

    def interceptor(self, request):
        # Add the missing headers
        request.headers["sec-fetch-mode"] = "cors"
        request.headers["cookie"] = self.cookie

    def run(self):
        self.driver.request_interceptor = self.interceptor
        self.driver.get(self.profile)
        time.sleep(20)
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div[3]/h3/div[2]/span').click()
        time.sleep(20)
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
        # Write any remaining users to a final file after finishing
        if self.user_list:
            output_file = os.path.join(self.output_dir, f"follower_list_{self.file_counter}.json")
            with open(output_file, 'w') as outfile:
                json.dump(self.user_list, outfile, indent=4)
            print(f"Data successfully written to {output_file}")
        self.driver.quit()

if __name__ == "__main__":
    # CLI argument parsing
    parser = argparse.ArgumentParser(description='TikTok scraper with Selenium.')
    parser.add_argument('--cookie', type=str, required=True, help='Cookie string for authentication')
    parser.add_argument('--scrape', type=int, required=True, help='Number of times to scroll and scrape data')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory for scraped data', default="scraped")
    parser.add_argument('--profile', type=str, required=True, help='TikTok profile to scrape from')

    args = parser.parse_args()

    # Instantiate the scraper and run it
    scraper = TikTokScraper(cookie=args.cookie, scrape_count=args.scrape, output_dir=args.output_dir, profile=args.profile)
    scraper.run()
    scraper.convert()  # Check if we need to write to a file
