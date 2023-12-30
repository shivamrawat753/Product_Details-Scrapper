# Women's Jackets Web Scraper

## Overview

This Python project, "Women's Jackets Web Scraper," utilizes the Selenium web automation library to scrape women's jackets data from various outdoor clothing retailers. The script is designed to extract information such as brand, product title, product URL, product image URL, product price, rating, and review count from multiple websites, including Patagonia, REI, Backcountry, Dick's Sporting Goods, and Moosejaw.

## Key Features

1. **Modular Structure:** The code is organized into a class-based structure, making it easy to extend and maintain. Each website has its dedicated scraping method.

2. **Chrome WebDriver Setup:** The project incorporates a Chrome WebDriver with headless browsing and stealth features to mimic human-like interactions and avoid bot detection.

3. **CSV Data Storage:** Scraped data is saved to a CSV file, allowing for easy analysis and further processing.

4. **Multi-Website Scraping:** The script iterates through different URLs representing distinct outdoor clothing retailers, applying site-specific scraping logic for each.
