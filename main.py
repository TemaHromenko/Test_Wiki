import requests
from bs4 import BeautifulSoup

URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80' \
      '%D1%81%D1%82%D0%B2 '
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')


def same_letter_count(dict_, word, countries):
    first_letter = list(word)[0]
    count = 0
    for country in countries:
        if country.startswith(first_letter):
            count += 1
        else:
            continue
    return count


def get_urls():
    urls = []  # Для ссылок на флаги
    table = soup.find(class_="wikitable").find_all("a")
    for item in table:
        url = item.get('href')
        if url.endswith('.svg'):
            urls.append(url)
        else:
            continue
    return urls


def get_info():
    _info = []
    raw_info = soup.find(class_="wikitable").find("tbody").find_all("td")
    for item in raw_info:
        if len(item.text.strip()) > 0:
            _info.append(item.text.strip())
    return _info


def get_content():
    global names
    i = 0
    _dict = []
    names = get_info()[1::3]  # страны
    info = get_info()[-1::-3]
    full_names = info[::-1]  # полное название стран

    """Форматирование"""
    for i in range(len(names)):
        try:
            _dict.append({
                'country': names[i],
                'same_letter_count': same_letter_count(dict_=_dict, word=names[i], countries=names),
                'full_country_name': full_names[i],
                'flag_url': get_urls()[i],
            })
        except Exception as e:
            print('Что-то пошло не так')
            print(e)
            break

    return _dict


def main():
    try:
        word = str(input("\nВведите искомую страну:  "))
        info = get_content()
        _id = names.index(word)
        print(" ")
        print(info[_id])
    except Exception as e:
        print(e)


main()
