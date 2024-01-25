import requests
from bs4 import BeautifulSoup

backup_entry_list = []
backup_title_list = []
number_list = ['2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '1.', 'I.', 'II.', 'III.', *range(1, 30, 1), '2)', '3)',
               '4)', '5)', '6)', '7)', '8)', '9)', '1)', '1-2', '2-3', '3-4', '5-6', '7-8', '8-9']


def search(processed):
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

        if explanation not in backup_entry_list:
            backup_entry_list.append(explanation)
        if title not in backup_title_list:
            backup_title_list.append(title)


def next_entry():
    explanation = backup_entry_list[1]
    title = backup_title_list[1]
    backup_entry_list.pop(0)
    backup_title_list.pop(0)
    nextentry = f"🧩{title.upper()}\n{explanation.replace(title, '')}"
    return nextentry
