#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from urllib.parse import urljoin

class WebScraper:
    def __init__(self):
        # Initialize the web driver, CSV file, and CSV columns
        self.driver = self.setup_driver()
        self.csv_file = "women's_jackets_data.csv"
        self.csv_columns = ["brand", "product title", "product URL", "product image URL", "product price", "rating", "review count"]
        self.data_list = []
        self.visited_links = set() # Initialize visited_links as an instance variable
        
    def setup_driver(self):
        # Set up Chrome WebDriver
        chrome_driver_path = 'C:/Users/Vijay Computers/Documents/Web_Scraping/chromedriver/chromedriver.exe'
        chrome_service = Service(chrome_driver_path)

        options = webdriver.ChromeOptions() 
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(service=chrome_service, options=options)

        # Apply stealth settings to reduce detection
        stealth(driver,
                user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        return driver

    def scrape_platform(self, platform_url):
        self.driver.get(platform_url)

        # Add scraping logic for each platform
        if "patagonia" in platform_url:
            self.scrape_patagonia()
        elif "rei" in platform_url:
            self.scrape_rei()
        elif "backcountry" in platform_url:
            self.scrape_backcountry()
        elif "dickssportinggoods" in platform_url:
            self.scrape_dicks_sporting_goods()

    def scrape_patagonia(self):
        # Navigate to the given platform URL and call specific scraping logic
        
        # Wait until the cookie popup element is present on the page
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#onetrust-button-group #onetrust-reject-all-handler')))
        # Find and click on the "Reject All" button in the cookie popup
        cookie_popup = self.driver.find_element(By.CSS_SELECTOR, '#onetrust-button-group #onetrust-reject-all-handler')
        cookie_popup.click()

        # Find and click on the close button of another popup
#         popup = self.driver.find_element(By.CSS_SELECTOR, '#modalNotification .modal__close .cta-circle')
#         time.sleep(2)
#         popup.click()
#         time.sleep(2)

        # Find and click on the search icon in the navigation bar
        search_icon = self.driver.find_element(By.CSS_SELECTOR, '.navigation-primary__icon--search-desktop svg')
        search_icon.click()

        # Find the search bar, input "women's jackets," and press Enter
        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
        search_bar.send_keys("women's jackets")
        time.sleep(2)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)

        # Find and click on the gender filter button
        gender = self.driver.find_element(By.CSS_SELECTOR, '#button-26')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", gender)
        time.sleep(2)
        gender.click()

        # Find and click on the filter option for Women's gender
        women = self.driver.find_element(By.CSS_SELECTOR, '#collapsible-26 li[title="Refine by Gender: Women\'s"] a')
        time.sleep(2)
        women.click()
        time.sleep(5)

        # Initialize an empty set to keep track of visited links
        visited_links = set()

        # Start scraping loop
        while True:
            try:
                # Find all product elements on the page
                products = self.driver.find_elements(By.CSS_SELECTOR, 'div.product-tile__wrapper')
                for product in products:
                    # Extract the product link
                    link_element = product.find_element(By.CSS_SELECTOR, ".link")
                    link = link_element.get_attribute("href")

                    # Check if the link has not been visited before
                    if link not in self.visited_links: 
                        # Open a new tab and navigate to the product link
                        self.driver.execute_script("window.open('', '_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.driver.get(link)
                        time.sleep(2)

                        # Extract product details (title, image URL, price, rating, review)
                        title = self.driver.find_element(By.CSS_SELECTOR, '#product-title').text
                        image_url = self.driver.find_element(By.CSS_SELECTOR, '.card__image picture source').get_attribute('srcset')
                        price_element = self.driver.find_element(By.CSS_SELECTOR, '.pdp-intro .price .value').text
                        price = float(price_element.replace('$', ''))

                        try:
                            review_element = self.driver.find_element(By.CSS_SELECTOR, 'span.pdp-intro__reviews').text
                            review_value = review_element.replace('Reviews', '').strip()
                            review_count = int(review_value)
                        except:
                            review_count = 0

                        try:
                            rating_element = self.driver.find_element(By.CSS_SELECTOR, '.pdp-intro .sr-only').text
                            rating_value = rating_element.split(':')[-1].strip().split('/')[0].strip()
                            rating = float(rating_value)
                        except:
                            rating = 0.0

                        # Store the extracted data in a dictionary
                        data = {
                            'brand' : "Patagonia",
                            'title' : title,
                            'image url' : image_url,
                            'url' : link,
                            'price' : price,
                            'rating' : rating,
                            'review' : review_count
                        }

                        # Append the data to the list and mark the link as visited
                        self.data_list.append(data)
                        self.visited_links.add(link)  

                        # Close the current tab and switch back to the main window
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(2)

                # Find and click on the "Load More" button
                load_more = self.driver.find_element(By.CSS_SELECTOR, 'div.show-more button')
                self.driver.execute_script("arguments[0].scrollIntoView();", load_more)
                time.sleep(2)
                load_more.click()
                time.sleep(5)
            except:
                # Break out of the loop if an exception occurs (e.g., no more products to load)
                break

    def scrape_rei(self):
        # Navigate to the given platform URL and call specific scraping logic
        
        # Input search query for women's jackets
        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
        search_bar.send_keys("women's jackets")
        time.sleep(2)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)

        # Wait for the Patagonia brand filter to be present
        wait = WebDriverWait(self.driver, 10)
        patagonia_brand = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#filter-brand li:nth-child(5) a')))
        self.driver.execute_script("arguments[0].scrollIntoView();", patagonia_brand)
        time.sleep(5)

        # Click on the Patagonia brand filter
        patagonia_brand.click()
        time.sleep(5)

        # Start scraping loop
        while True:
            try:
                # Extract product links from the current page
                products = self.driver.find_elements(By.CSS_SELECTOR, '.VcGDfKKy_dvNbxUqm29K')
                for product in products:
                    # Get the link for each product
                    link = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    # Check if the link has not been visited before
                    if link not in self.visited_links:

                        # Open a new tab and navigate to the product page
                        self.driver.execute_script("window.open('', '_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.driver.get(link)
                        time.sleep(5)

                        # Extract product details
                        title = self.driver.find_element(By.CSS_SELECTOR, '#product-page-title').text
                        image_url = self.driver.find_element(By.CSS_SELECTOR, '#media-center-primary-image').get_attribute('src')
                        price_element = self.driver.find_element(By.CSS_SELECTOR, '#buy-box-product-price').text
                        price = float(price_element.replace('$', ''))

                        try:
                            review = self.driver.find_element(By.CSS_SELECTOR, '#product-rating .cdr-rating__count_13-5-3 span:nth-child(2)').text
                            review_count = int(review)
                        except:
                            review_count = 0

                        try:
                            rating = self.driver.find_element(By.CSS_SELECTOR, '#product-rating .cdr-rating__number_13-5-3').text
                            rating = float(rating)
                        except:
                            rating = 0.0

                        # Store the extracted data in a dictionary
                        data = {
                            'brand': "Patagonia",
                            'title': title,
                            'image url': image_url,
                            'url': link,
                            'price': price,
                            'rating': rating,
                            'review': review_count
                        }

                        # Append the data dictionary to the data_list
                        self.data_list.append(data)
                        self.visited_links.add(link) 

                        # Close the current tab and switch back to the main tab
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(5)

                # Navigate to the next page
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'div.U6aiNae0xHxm_mgWhHsW a[data-id="pagination-test-link-next"]')
                next_ = next_button.get_attribute('href')
                time.sleep(2)
                self.driver.get(next_)
                time.sleep(5)

            except Exception as e:
                # Break the loop if there are no more pages or an exception occurs
                break

    def scrape_backcountry(self):
        # Navigate to the given platform URL and call specific scraping logic
        
        # Input search query for "women's jackets"
        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
        search_bar.send_keys("women's jackets")
        time.sleep(2)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)

        # Wait for the Patagonia brand filter to be present
        wait = WebDriverWait(self.driver, 10)
        patagonia_brand = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li:nth-child(3) .chakra-checkbox__label p')))
        self.driver.execute_script("arguments[0].scrollIntoView();", patagonia_brand)
        time.sleep(5)

        # Click on the Patagonia brand filter
        patagonia_brand.click()
        time.sleep(5)

        # Start scraping loop
        while True:
            try:
                # Extract product links from the current page
                products = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-id="productsWrap"] div[data-id="productListingItems"]')))
                for product in products:
                    # Get the link for each product
                    link = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    
                    # Check if the link has not been visited before
                    if link not in self.visited_links:

                        # Open a new tab and navigate to the product page
                        self.driver.execute_script("window.open('', '_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.driver.get(link)
                        time.sleep(5)

                        # Extract product details
                        title = self.driver.find_element(By.CSS_SELECTOR, 'span[data-id="productTitle"]').text
                        image_url = self.driver.find_element(By.CSS_SELECTOR, 'div.css-kbissy img').get_attribute('src')

                        # Extract price information (handle different formats)
                        try:
                            price_element = self.driver.find_element(By.CSS_SELECTOR, 'span[data-id="pricing"] .css-17wknbl').text
                            price = float(price_element.replace('$', ''))
                        except:
                            price_element = self.driver.find_element(By.CSS_SELECTOR, 'span[data-id="pricing"]').text
                            price = (re.search(r'\$\d+\.\d+', price_element)).group(0)
                            price = float(price.replace('$', ''))

                        # Extract review count
                        try:
                            review_element = self.driver.find_element(By.CSS_SELECTOR, 'div[data-id="buyboxRating"] .chakra-text.css-0').text
                            review = review_element.split()[0]
                            review_count = int(review)
                        except:
                            review_count = 0

                        # Extract product rating
                        try:
                            rating_element = self.driver.find_element(By.CSS_SELECTOR, 'div[data-id="buyboxRating"] .css-f8n5zr').text
                            rating = rating_element.split()[0]
                            rating = float(rating)
                        except:
                            rating = 0.0

                        # Store the extracted data in a dictionary
                        data = {
                            'brand': "Patagonia",
                            'title': title,
                            'image url': image_url,
                            'url': link,
                            'price': price,
                            'rating': rating,
                            'review': review_count
                        }

                        # Append the data dictionary to the data_list
                        self.data_list.append(data)
                        self.visited_links.add(link) 

                        # Close the current tab and switch back to the main tab
                        self.driver.close()
                        self.driver.switch_to.window(driver.window_handles[0])
                        time.sleep(5)

                # Navigate to the next page
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'div.css-11fzw6j a')
                next_page = next_button.get_attribute('href')
                time.sleep(2)
                self.driver.get(next_page)
                time.sleep(5)

            except Exception as e:
                # Break the loop if there are no more pages or an exception occurs
                break

    def scrape_dicks_sporting_goods(self):
        # Navigate to the given platform URL and call specific scraping logic
        
        # Input search query for "womens jackets"
        search_bar = self.driver.find_element(By.CSS_SELECTOR, '#searchInput')
        search_bar.send_keys("women's jackets")
        time.sleep(2)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)

        # Wait for the Patagonia brand filter to be present
        wait = WebDriverWait(driver, 10)
        patagonia_brand = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#brand_facet_value_Patagonia')))
        # Scroll into view (commented out, as it may not be needed)
        # driver.execute_script("arguments[0].scrollIntoView();", patagonia_brand)
        time.sleep(5)

        # Click on the Patagonia brand filter
        patagonia_brand.click()
        time.sleep(5)

        # Start scraping loop
        while True:
            try:
                # Extract product links from the current page
                products = self.driver.find_elements(By.CSS_SELECTOR, '.dsg-flex.flex-column.dsg-react-product-card.rs_product_card.dsg-react-product-card-col-4')
                for product in products:
                    # Get the link for each product
                    link_element = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    link = urljoin(base_url, link_element)
                    
                    # Check if the link has not been visited before
                    if link not in self.visited_links:

                        # Open a new tab and navigate to the product page
                        self.driver.execute_script("window.open('', '_blank');")
                        self.driver.switch_to.window(driver.window_handles[-1])
                        self.driver.get(link)
                        time.sleep(10)

                        # Extract product details
                        title = self.driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]').text
                        image_url = self.driver.find_element(By.CSS_SELECTOR, 'img[data-cy="product-image"]').get_attribute('src')

                        # Extract price information
                        price_element = self.driver.find_element(By.CSS_SELECTOR, 'div .product-price.ng-star-inserted').text
                        price = float(price_element.replace('$', ''))

                        # Extract review count
                        try:
                            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="bv_numReviews_text"]')))
                            review_element = self.driver.find_element(By.CSS_SELECTOR, 'div[class="bv_numReviews_text"]').text
                            review_count = int(review_element.strip('()').split()[0])
                        except:
                            review_count = 0

                        # Extract product rating
                        try:
                            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[itemprop="ratingValue"]')))
                            rating_element = self.driver.find_element(By.CSS_SELECTOR, 'div[itemprop="ratingValue"]').text
                            rating = float(rating_element)
                        except:
                            rating = 0.0

                        # Store the extracted data in a dictionary
                        data = {
                            'brand': "Patagonia",
                            'title': title,
                            'image url': image_url,
                            'url': link,
                            'price': price,
                            'rating': rating,
                            'review': review_count
                        }

                        # Append the data dictionary to the data_list
                        self.data_list.append(data)
                        self.visited_links.add(link) 

                        # Close the current tab and switch back to the main tab
                        self.driver.close()
                        self.driver.switch_to.window(driver.window_handles[0])
                        time.sleep(5)

                # Navigate to the next page
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'a.dsg-flex.flex-column.rs-page-item.rs-next-item')
                time.sleep(2)
                next_button.click()
                time.sleep(5)

            except Exception as e:
                # Break the loop if there are no more pages or an exception occurs
                break
        pass

#     def save_to_csv(self, data):
#         # Save the scraped data to the CSV file
#         with open(self.csv_file, mode="a", newline="", encoding="utf-8") as file:
#             writer = csv.DictWriter(file, fieldnames=self.csv_columns)
#             writer.writerow(data)
    def save_to_csv(self, data):
        df = pd.DataFrame(data, columns=self.csv_columns)
        df.to_csv(self.csv_file, mode="a", index=False, header=not os.path.exists(self.csv_file), encoding="utf-8")
        
    def read_csv(self):
        df = pd.read_csv(self.csv_file)
        return df

    def run(self):
        # Iterate through platform URLs and perform scraping
        for platform_url in [
            "https://www.patagonia.com",
            "https://www.rei.com",
            "https://www.backcountry.com",
            "https://www.dickssportinggoods.com",
        ]:
            self.scrape_platform(platform_url)
            
        # After all scraping is done, save the accumulated data to CSV
        for data in self.data_list:
            self.save_to_csv(data)
        
        # Quit the web driver after scraping all platforms
        self.driver.quit()
        
        df = self.read_csv()
        print(df)

if __name__ == "__main__":
    # Instantiate the WebScraper class and run the scraping process
    scraper = WebScraper()
    scraper.run()

