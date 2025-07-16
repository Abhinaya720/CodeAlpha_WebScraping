import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL (pagination)
base_url = "https://books.toscrape.com/"

# Data containers
titles, prices, availability, ratings = [], [], [], []

# Scrape first 5 pages (you can change this to 1–50)
for page_num in range(1, 6):
    url = base_url.format(page_num)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to access page {page_num}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        # Title
        title = book.h3.a["title"]
        titles.append(title)

        # Price
        price = book.find("p", class_="price_color").text.strip().lstrip("£")
        prices.append(price)

        # Availability
        stock = book.find("p", class_="instock availability").text.strip()
        availability.append(stock)

        # Rating (extracted from class name)
        rating_class = book.find("p", class_="star-rating")["class"]
        rating = rating_class[1] if len(rating_class) > 1 else "No Rating"
        ratings.append(rating)

# Create a DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price (£)": prices,
    "Availability": availability,
    "Rating": ratings
})

# Save to CSV
df.to_csv("books_data.csv", index=False)
print(" Scraping completed. Data saved to books_data.csv")
