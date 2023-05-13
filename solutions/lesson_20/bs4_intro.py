"""
Intro to webscraping
"""
import os
import requests
from bs4 import BeautifulSoup as bs


def get_page(url: str) -> bs:
    return bs(requests.get(url).content, "html.parser")


def get_jpgs(soup: bs) -> list:
    """
    Given a webpage as beautifulsoup, extracts the jpg links and stores them in a list
    """
    imgs = soup.find_all("img")
    jpgs = list()
    for i in imgs:
        if 'jpg' in i.get('src'):
            jpgs.append(i)
    return jpgs


def save_jpgs(jpg_list: list):
    """
    Saves the jpgs to file
    """
    # use a for-loop to go through each of the items
    for jpg in jpg_list:
        # 1) extract the link from each item in the list  
        # 2) fix the link to make a proper web address
        link = "https:" + jpg['src']

        try:
            # 3) extract the data from the link
            img_data = requests.get(link).content

            # 4) write the data to a file 
            with open(os.path.basename(link), "wb") as f:
                f.write(img_data)
        except:
            print(f"Could not process {link}")


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Pok%C3%A9mon"

    pkm_soup = get_page(url)

    links = pkm_soup.find_all("a")

    jpgz = get_jpgs(pkm_soup)
    save_jpgs(jpgz)
