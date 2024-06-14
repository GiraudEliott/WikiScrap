# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import os
import requests
from bs4 import BeautifulSoup


def get_wikipedia_links_with_names(url):
    # pylint: disable=missing-function-docstring
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find(id="mw-content-text")
    links = content.find_all("a", href=True)

    valid_links = []
    for link in links:
        href = link["href"]
        if (
            href.startswith("/wiki/")
            and not href.startswith("/wiki/File:")
            and not href.startswith("/wiki/Template:")
            and not href.startswith("/wiki/Category:")
        ):
            name = link.get_text().strip()
            if name:  # Vérifie si le titre du lien n'est pas vide
                valid_links.append((name, href))

    return valid_links


# pylint: disable=missing-function-docstring
if __name__ == "__main__":
    url = "https://fr.wikipedia.org/wiki/Martinique"
    links = get_wikipedia_links_with_names(url)

    total_links = len(links)
    print(f"Total de liens sur la page {url}: {total_links}")

    # Nombre de liens par page à afficher
    links_per_page = 50
    
    page_number = 1
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Efface la console
        print(f"\nPage {page_number}:")
        start_index = (page_number - 1) * links_per_page
        end_index = min(page_number * links_per_page, total_links)

        for idx, link in enumerate(links[start_index:end_index], start=start_index + 1):
            name, href = link
            print(f"{idx:02d} - {name}")

        print("\n98 - Page précédente")
        print("99 - Page suivante")
        print("0 - Quitter")

        user_input = input("Entrez votre choix : ")
        
        if user_input == "98":
            if page_number > 1:
                page_number -= 1
            else:
                print("Vous êtes déjà sur la première page.")
                input("Appuyez sur Entrée pour continuer...")
        elif user_input == "99":
            if page_number < (total_links // links_per_page) + 1:
                page_number += 1
            else:
                print("Vous êtes déjà sur la dernière page.")
                input("Appuyez sur Entrée pour continuer...")
        elif user_input == "0":
            print("Fin du programme.")
            break
        else:
            print("Choix invalide. Veuillez entrer 98 pour la page précédente, 99 pour la page suivante, ou 0 pour quitter.")
            input("Appuyez sur Entrée pour continuer...")
