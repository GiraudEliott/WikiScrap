# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import os
import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin

# Variables globales pour mémoriser les liens
start_url = None
start_title = None
end_url = None
end_title = None
current_url = None
current_title = None
coup_counter = 0


def get_wikipedia_links_with_names(url):
    # Fetch the HTML content from the URL
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
            if name:  # Check if the link text (name) is not empty
                valid_links.append((name, href))

    return valid_links


def get_wikipedia_random_link():
    random_url = "https://fr.wikipedia.org/wiki/Spécial:Page_au_hasard"
    response = requests.get(random_url)
    soup = BeautifulSoup(response.text, "html.parser")
    random_link = soup.find("link", {"rel": "canonical"})

    if random_link:
        return random_link["href"]
    else:
        return None


def display_links(links, page_number, total_pages):
    # Fonction pour afficher les liens d'une page donnée
    print(f"\nPage {page_number}:")
    for idx, link in enumerate(links, start=1):
        name, href = link
        print(f"{idx:02d} - {name}")
    print(
        f"\nPage {page_number}/{total_pages} - Lien actuel : {current_title} ({current_url})"
    )


if __name__ == "__main__":
    # Fetch the random start URL
    start_url = get_wikipedia_random_link()
    if not start_url:
        print("Impossible de récupérer le lien de départ aléatoire.")
        exit()

    # Définition du lien d'arrivée
    end_url = get_wikipedia_random_link()
    if not end_url:
        print("Impossible de récupérer le lien d'arrivée aléatoire.")
        exit()

    # Récupérer les titres des pages de départ et cible une seule fois
    response_start = requests.get(start_url)
    soup_start = BeautifulSoup(response_start.text, "html.parser")
    start_title = soup_start.find("title").get_text()

    response_end = requests.get(end_url)
    soup_end = BeautifulSoup(response_end.text, "html.parser")
    end_title = soup_end.find("title").get_text()

    # Initialiser l'URL et le titre actuels
    current_url = start_url
    current_title = start_title

    # Récupération des liens de la page de départ
    start_links = get_wikipedia_links_with_names(current_url)
    total_links_start = len(start_links)
    print(f"\nTotal des liens sur la page : {total_links_start}")
    print("")

    # Nombre de liens par page à afficher
    links_per_page = 20

    page_number = 1
    while True:
        # Afficher les informations actuelles à chaque itération de la boucle
        print("｡.｡:+* ﾟ ゜ﾟ *+:｡.｡:+* ﾟ ゜ﾟ *+:｡.｡.｡:+* ﾟ ゜ﾟ *+:｡.｡:+* ﾟ ゜ﾟ *+:｡.｡")
        print(f"\nPage de départ : {start_title} ({start_url})")
        print(f"Page cible : {end_title} ({end_url})")
        print("")
        print(
            f"Page actuelle : Page {page_number}/{(total_links_start // links_per_page) + 1}"
        )
        print(f"Nombre de coups : {coup_counter}")

        # Afficher les liens de la page courante
        display_links(
            start_links[
                (page_number - 1) * links_per_page : page_number * links_per_page
            ],
            page_number,
            (total_links_start // links_per_page) + 1,
        )

        print("\n98 - Page précédente")
        print("99 - Page suivante")
        print("0 - Quitter")
        print("Choisir un lien spécifique (1-20)")
        print("")

        user_input = input("Entrez votre choix : ")

        if user_input.isdigit() and 1 <= int(user_input) <= 20:
            chosen_link = start_links[
                (page_number - 1) * links_per_page + int(user_input) - 1
            ]
            name, href = chosen_link
            print(f"Vous avez choisi le lien : {name} ({href})")

            # Construire l'URL absolue à partir du lien relatif
            new_url = urljoin(current_url, href)

            # Mise à jour de la page actuelle sans changer start_url ou end_url
            current_url = new_url
            response_start = requests.get(current_url)
            soup_start = BeautifulSoup(response_start.text, "html.parser")
            current_title = soup_start.find("title").get_text()
            start_links = get_wikipedia_links_with_names(current_url)
            total_links_start = len(start_links)
            page_number = (
                1  # Retour à la première page après avoir choisi un nouveau lien
            )
            coup_counter += 1  # Incrémenter le compteur de coups

            # Vérifier si la page actuelle est la page ciblecl
            if current_url == end_url:
                print("Félicitations ! Vous avez atteint la page cible.")
                print(f"Nombre total de coups : {coup_counter}")
                break

        elif user_input == "98":
            if page_number > 1:
                page_number -= 1
            else:
                print("Vous êtes déjà sur la première page.")
                input("Appuyez sur Entrée pour continuer...")
        elif user_input == "99":
            if page_number < (total_links_start // links_per_page) + 1:
                page_number += 1
            else:
                print("Vous êtes déjà sur la dernière page.")
                input("Appuyez sur Entrée pour continuer...")
        elif user_input == "0":
            print("Fin du programme.")
            break
        else:
            print(
                "Choix invalide. Veuillez entrer un nombre de lien valide (1-20), 98 pour la page précédente, 99 pour la page suivante, ou 0 pour quitter."
            )
            input("Appuyez sur Entrée pour continuer...")
