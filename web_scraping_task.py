# -*- coding: utf-8 -*-
"""web_scraping_task.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iHujSRctL64_ycIcoA-rW7nj2oxcDDgn
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin

# List of URLs to scrape
urls = [
     "https://www.webfx.com/digital-marketing/",
    "https://www.thriveagency.com/digital-marketing/",
    "https://www.lyfemarketing.com/digital-marketing/",
    "https://www.smartbugmedia.com/inbound-marketing-agency",
    "https://www.seo.com",
    "https://www.vivial.net",
    "https://www.bigdropinc.com",
    "https://www.singlegrain.com",
    "https://www.bluecorona.com",
    "https://www.disruptiveadvertising.com",
    "https://www.tubikstudio.com",
    "https://www.ignitevisibility.com",
    "https://www.cleverus.com",
    "https://www.brightedge.com",
    "https://www.lytics.com",
    "https://www.silverbackstrategies.com",
    "https://www.fatjoedigital.com",
    "https://www.jellyfish.com",
    "https://www.gosquared.com",
    "https://www.marlincommunications.com",
    "https://www.neboagency.com",
    "https://www.vayeca.com",
    "https://www.rumoradvertising.com",
    "https://www.theagencyinc.com",
    "https://www.brewerpr.com",
    "https://www.jeffbullas.com",
    "https://www.expeditionco.com",
    "https://www.propelgrowth.com",
    "https://www.barnraiser.com",
    "https://www.qoof.com",
    "https://www.searchenginepeople.com",
    "https://www.localvisibilitysystem.com",
    "https://www.rocketmedia.com",
    "https://www.unmetric.com",
    "https://www.moz.com",
    "https://www.adverity.com",
    "https://www.mediacom.com"
    # Add remaining URLs
]

# Set headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# Function to scrape data from a company URL
def scrape_company(url):
    print(f"Scraping {url}...")

    try:
        # Send a GET request to the website
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')

        # Dictionary to store the company's data
        data = {}

        # Extract the company name (fallback: title tag)
        company_name_tag = soup.find('title')
        data['Company Name'] = company_name_tag.text.strip() if company_name_tag else 'N/A'

        # Extract the website URL
        data['Website URL'] = url  # Use the current URL

        # Extract the contact number
        contact_number = None
        # Look for phone numbers directly within 'tel:' links
        tel_links = soup.find_all('a', href=True)
        for link in tel_links:
            if 'tel:' in link['href']:
                contact_number = link['href'].replace('tel:', '').strip()
                break
        # If no tel link found, search for contact numbers in text
        if not contact_number:
            for tag in soup.find_all(['p', 'span', 'a']):
                if tag.text and any(word in tag.text for word in ['+1', '+91', 'Phone', 'Contact']):
                    contact_number = tag.text.strip()
                    break
        data['Contact Number'] = contact_number if contact_number else 'Not Available'

        # Extract the email address (handle 'mailto:' and other email patterns)
        email = None

        # Look for 'mailto:' links
        email_tag = soup.find('a', href=lambda href: href and 'mailto:' in href)
        if email_tag:
            email = email_tag['href'].replace('mailto:', '').strip()

        # If no email found, check for other email-like patterns in text
        if not email:
            for tag in soup.find_all(['p', 'span', 'a']):
                if tag.text and '@' in tag.text:
                    email = tag.text.strip()
                    break

        data['Email Address'] = email if email else 'Not Available'

        # Extract the industry/category
        data['Industry/Category'] = 'Digital Marketing Agencies'  # Fixed value as per requirement

        # Extract the company description (meta description fallback)
        description_tag = soup.find('meta', attrs={'name': 'description'})
        data['Company Description'] = description_tag['content'].strip() if description_tag and 'content' in description_tag.attrs else 'N/A'

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Main function to scrape all URLs and store the data
def main():
    all_data = []

    for idx, url in enumerate(urls):
        data = scrape_company(url)
        if data:
            all_data.append(data)

        # Adding a delay to avoid being blocked
        delay = random.uniform(2, 5)
        print(f"Waiting for {delay:.2f} seconds...")
        time.sleep(delay)

    # Save the data to a CSV file
    df = pd.DataFrame(all_data)
    output_file = 'digital_marketing_agencies_detailed.csv'
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == '__main__':
    main()