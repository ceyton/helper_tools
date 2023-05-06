import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = "https://afasiaarchzine.com/page/{}"
num_pages = 50000  # Change this to the number of pages you want to scrape
counter = 0  # Initialize the counter variable

# Create the "images" folder if it doesn't exist
if not os.path.exists("images_v2"):
    os.makedirs("images_v2")

# Create the tqdm progress bar with the initial description
pbar = tqdm(range(1, num_pages + 1), desc="Pages")

# Loop through all the pages
for page in pbar:
    url = base_url.format(page)

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the article links on the page
    article_links = [a.find("a")["href"] for a in soup.find_all("article")]

    # Loop through all the article links
    for link in article_links:
        # Send a GET request to the article URL
        response = requests.get(link)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find("h1", class_="entry-title").text.strip()
        # Find all the div tags with class "gallery-icon portrait" on the article page
        gallery_divs = soup.find_all("div", class_="gallery-icon portrait")

        # Find all the image tags within the gallery divs
        for gallery_div in gallery_divs:
            gallery_images = gallery_div.find_all("img")

            # Modify the src attribute of each image tag to remove the "-250X250" part
            for gallery_image in gallery_images:
                src = gallery_image["src"]
                modified_url = src.replace("-250x250", "")

                counter += 1  # Increment the counter variable
                gallery_image["src"] = modified_url

                # Save the modified image to the "images" folder
                filename = f"{title}_image_{counter}.jpg"
                filepath = os.path.join("images", filename)
                with open(filepath, "wb") as f:
                    f.write(requests.get(modified_url).content)

                # Update the tqdm progress bar description
                desc = f"Pages ({counter} modified URLs)"
                pbar.set_description(desc)

# Close the tqdm progress bar
pbar.close()

print("Number of modified URLs:", counter)
