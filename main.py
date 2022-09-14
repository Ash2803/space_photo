import os
import urllib.parse
import requests
from pathlib import Path
from dotenv import load_dotenv


def file_download(path, url):
    """Download files to user created directory"""
    response = requests.get(url)
    response.raise_for_status()
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(f'{path}/hubble.jpeg', 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(launch_id, path):
    """Get photos of the last SpaceX rocket launch"""
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{launch_id}')
    response.raise_for_status()
    urls = response.json()['links']['flickr']['original']
    Path(path).mkdir(parents=True, exist_ok=True)
    for url_number, url in enumerate(urls):
        image = requests.get(url)
        image.raise_for_status()
        with open(f'{path}/spacex_{url_number}.jpeg', 'wb') as file:
            file.write(image.content)


def download_nasa_photo(token, nasa_url, path):
    """Getting photo urls and downloading"""
    param = {
        'api_key': token,
        'count': '40'
    }
    response = requests.get(nasa_url, params=param)
    response.raise_for_status()
    Path(path).mkdir(parents=True, exist_ok=True)
    for url_number, url in enumerate(response.json()):
        image = requests.get(url['url'])
        image.raise_for_status()
        file_format = get_format(url['url'])
        if not file_format:
            continue
        with open(f'{path}/nasa_{url_number}{file_format}', 'wb') as file:
            file.write(image.content)


def get_epic_nasa(url, token, path):
    links = []
    param = {
        'api_key': token
    }
    response = requests.get(url, params=param)
    response.raise_for_status()
    Path(path).mkdir(parents=True, exist_ok=True)
    for info in response.json():
        image_name = info['image']
        image_date = info['date'].split(" ")[0].replace('-', '/')
        image_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date}/png/{image_name}.png?api_key={token}'
        links.append(image_url)
        for link_number, link in enumerate(links):
            image = requests.get(link)
            image.raise_for_status()
            file_format = get_format(link)
            with open(f'{path}/nasa_epic_photo{link_number}{file_format}', 'wb') as file:
                file.write(image.content)


def get_format(photo_url):
    url_split = urllib.parse.urlsplit(photo_url)
    domain_split = urllib.parse.unquote(url_split[2])
    get_file_format = os.path.splitext(domain_split)
    if get_file_format[1]:
        return get_file_format[1]


def main():
    # url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    # file_download(path, url)
    # launch_id = input('Enter launch id: ')
    path = input('Enter download path: ')
    # fetch_spacex_last_launch(launch_id, path)
    load_dotenv()
    nasa_url = input('Enter url: ')
    nasa_apikey = os.getenv('NASA_API_KEY')
    # download_nasa_photo(nasa_apikey, nasa_url, path)
    # print(nasa_photo_url)
    # print(refactoring_nasa_photo(nasa_photo_url))
    get_epic_nasa(nasa_url, nasa_apikey, path)


if __name__ == '__main__':
    main()
