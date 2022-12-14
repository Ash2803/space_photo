import os
import requests
from dotenv import load_dotenv
from download_photos import fetch_images
from datetime import datetime


def get_epic_nasa(token, img_name):
    """Downloading EPIC NASA photos"""
    params = {
        'api_key': token
    }
    response = requests.get('https://api.nasa.gov/EPIC/api/natural', params=params)
    response.raise_for_status()
    urls = []
    for link_number, link in enumerate(response.json(), start=1):
        image_name = link['image']
        date_format = datetime.fromisoformat(link['date'])
        image_date = datetime.strftime(date_format, '%Y/%m/%d')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png'
        urls.append(image_url)
        fetch_images(urls, params, img_name)


def main():
    load_dotenv()
    nasa_apikey = os.environ['NASA_API_KEY']
    get_epic_nasa(nasa_apikey, img_name='EPIC_photo_')


if __name__ == '__main__':
    main()
