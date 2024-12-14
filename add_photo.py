import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import json
import os
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class ImageScraper:
    def __init__(self):
        self.progress_file = 'scraping_progress.json'
        self.completed = self.load_progress()
        self.user_agent = UserAgent()
        
    def load_progress(self):
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or invalid, return an empty dictionary
                return {}
        return {}

    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.completed, f)

    def get_random_headers(self):
        return {
            "User-Agent": self.user_agent.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def scrape_flickr(self, query):
        # Flickr search URL for high-quality food photos
        search_url = f"https://www.flickr.com/search/?text={query}%20food&sort=relevance&size=large"
        try:
            response = requests.get(
                search_url,
                headers=self.get_random_headers(),
                timeout=5
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find high-res image URLs
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    # Convert to high-res version
                    if 'live.staticflickr.com' in src:
                        # Replace with larger size
                        high_res = src.replace('_n.jpg', '_b.jpg').replace('_m.jpg', '_b.jpg')
                        return high_res
        except Exception as e:
            print(f"Flickr error for {query}: {e}")
        return None

    def fetch_image_url(self, query):
        if query in self.completed:
            return self.completed[query]

        url = self.scrape_flickr(query)
        if url:
            self.completed[query] = url
            return url
        
        return None

def process_recipes(file_path, batch_size=100):
    recipes = pd.read_csv(file_path)
    scraper = ImageScraper()
    
    # Process in batches
    for i in range(0, len(recipes), batch_size):
        batch = recipes.iloc[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1} of {len(recipes)//batch_size + 1}")
        
        # Process batch with more workers for speed
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(scraper.fetch_image_url, title): title 
                      for title in batch['title']}
            
            for future in tqdm(as_completed(futures), 
                             total=len(futures), 
                             desc="Fetching images"):
                time.sleep(0.1)  # Minimal delay
        
        # Save progress
        scraper.save_progress()
        
        # Update DataFrame
        recipes.loc[batch.index, 'image_url'] = [scraper.completed.get(title) 
                                               for title in batch['title']]
        
        # Save results
        recipes.to_csv("recipes_with_images.csv", index=False)
        
        print(f"Completed batch {i//batch_size + 1}, saved progress")

if __name__ == "__main__":
    process_recipes('merged_dataset.csv', batch_size=100)
