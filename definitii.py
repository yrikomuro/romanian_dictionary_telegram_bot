# program for getting dictionary entries from online dictionary and displaying them
# make /n before each 1. 2. 3. 4. entry
import requests
from bs4 import BeautifulSoup


backup_entry_list = []
backup_title_list = []
number_list = ['2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '1.', 'I.', 'II.', 'III.', *range(1, 100, 1), '2)', '3)', '4)', '5)', '6)', '7)', '8)', '9)', '1)']


def search(processed):
    del_reps_list = []
    title_list = []
    backup_entry_list.clear()
    backup_title_list.clear()
    html_text = requests.get(f'https://dexonline.ro/definitie/{processed}/definitii').text

    soup = BeautifulSoup(html_text, 'lxml')
    explanation_components = soup.find_all('span', class_="def", title="Clic pentru a naviga la acest cuvânt")

    for explanation_component in explanation_components:
        explanation = explanation_component.text
        title = explanation_component.b.text

        for number in number_list:
            for character in explanation.split():
                if str(number) == character:
                    explanation = explanation.replace(f' {character} ', f'\n\n{character.replace('.', ')').replace(')', '')}) ')

        if explanation not in del_reps_list:
            del_reps_list.append(explanation)
            backup_entry_list.append(explanation)
        if title not in title_list:
            title_list.append(title)
            backup_title_list.append(title)
    for item in del_reps_list:
        for title in title_list:
            entry = f'🇹🇩{title.upper()}🇹🇩\n\n{item.replace(title, '')}'
            return entry


def next_entry():
    explanation = backup_entry_list[1]
    title = backup_title_list[1]
    backup_entry_list.pop(1)
    backup_title_list.pop(1)

    nextentry = f"🇹🇩{title.upper()}🇹🇩\n{explanation.replace(title, '')}"
    return nextentry


# search('organ')
