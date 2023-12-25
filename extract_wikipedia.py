from pathlib import Path
import requests

def extract_wikipedia(wiki_page):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': wiki_page,
            'prop': 'extracts',
            'explaintext': True,
        }
    ).json()
    page = next(iter(response['query']['pages'].values()))
    wiki_text = page['extract']

    data_path = Path('WikiData')
    if not data_path.exists():
        Path.mkdir(data_path)

    with open(data_path / f"{wiki_page}.txt", 'w') as fp:
        fp.write(wiki_text)


if __name__ == '__main__':
    extract_wikipedia('Breaking Bad')