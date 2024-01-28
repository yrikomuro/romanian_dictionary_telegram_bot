from selenium import webdriver
from selenium.webdriver.common.by import By
import definitii


def sinteza_search(processed):

    definitii.backup_title_list.clear()
    definitii.backup_entry_list.clear()
    PATH = '/usr/bin/safaridriver'
    driver = webdriver.Safari(PATH)
    driver.get(f'https://dexonline.ro/definitie/{processed}')

    title_source = driver.find_element(By.XPATH, "//*[@class='tree-heading']")
    speech_part_source = driver.find_element(By.XPATH, "//*[@class='tree-pos-info']")
    sources = driver.find_elements(By.XPATH, "//*[@class='tree-body']")
    first_source = sources[0]
    meaning_rows = first_source.find_elements(By.XPATH, ".//*[@class='def html']")
    numbers = first_source.find_elements(By.XPATH, ".//*[@class='bc']")

    list1 = []

    # creating a list of items
    for meaning_row, number in zip(meaning_rows, numbers):
        if meaning_row.is_displayed():
            list1.append(number.text)
            list1.append(meaning_row.text)

    # making idents before entry numbers
    idents = ['1.', '2.', '3.', '4.', '5.', '1.1.', '1.2.', '1.3.', '1.4.', '1.5.', '2.1.', '2.2.', '2.3.', '2.4.', '2.5.', '1.1.1.', '1.1.2.', '1.2.1.']

    for ident in idents:
        for item in list1:
            if ident == item:
                replace_index = list1.index(item)
                list1.pop(replace_index)
                list1.insert(replace_index, f'\n\n{ident}')

    explanation = f"\n{speech_part_source.text}{' '.join(list1)}"
    title = title_source.text

    new_title = title.replace(speech_part_source.text, '').upper()
    entry = f'🔎{new_title}{explanation}'

    definitii.backup_title_list.append(new_title)
    definitii.backup_entry_list.append(f'{new_title}{explanation}')
    definitii.search(processed)
    return entry
