import requests
import lxml.html as html
import os
import datetime

tema = input('Que tema quereres descargar?: ')
INFOCAMPO_URL = f'https://www.infocampo.com.ar/tag/{tema}/'
INFOCAMPO_LINKS_PATH = '//h1/a/@href'
INFOCAMPO_TITLE_PATH = '//div[@class="bloque_superior"]/h1/text()'
INFOCAMPO_SUMARRY_PATH = '//div[@class="bloque_superior"]/h2/text()'
INFOCAMPO_BODY_PATH = '//div[@class="contenidoNota"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(INFOCAMPO_TITLE_PATH)[0]
                title = title.replace('\"', '')
                sumarry = parsed.xpath(INFOCAMPO_SUMARRY_PATH)[0]
                body = parsed.xpath(INFOCAMPO_BODY_PATH)
            except IndexError as ve:
                print(f'Error: {ve}')

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n \n')
                f.write(sumarry)
                f.write('\n \n')
                for b in body:
                   f.write(b)
                   f.write(' ')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(f'Error: {ve}')


def parse_home():
    try:
        response = requests.get(INFOCAMPO_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links = parsed.xpath(INFOCAMPO_LINKS_PATH)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links:
                parse_notice(link, today)    
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(f'Error: {ve}')


def run():
    parse_home()


if __name__ == '__main__':
    run()