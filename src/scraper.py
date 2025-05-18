import requests
from bs4 import BeautifulSoup

def get_csv_links_for_year(year: int) -> dict:
    url = "https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2023/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    files = {
        "caracteristiques": None,
        "lieux": None,
        "usagers": None,
        "vehicules": None
    }

    for link in links:
        href = link["href"]
        text = link.get_text().lower()

        if not href.endswith(".csv"):
            continue

        if str(year) in href or str(year) in text:
            for key in files.keys():
                if key in href or key in text:
                    files[key] = "https://www.data.gouv.fr" + href if href.startswith("/") else href

    return files
