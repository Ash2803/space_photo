import requests
from pathlib import Path


from get_format import get_format


def fetch_images(urls):
    Path('images').mkdir(parents=True, exist_ok=True)
    for url_number, url in enumerate(urls):
        file_format = get_format(url)
        image = requests.get(url)
        image.raise_for_status()
        with open(f'images/photo_{url_number}{file_format}', 'wb') as file:
            file.write(image.content)


def main():
    pass


if __name__ == '__main__':
    main()