from bs4 import BeautifulSoup
import requests

def get_itbe_response(band_name):
    response = requests.get('http://isthisbandemo.com', params={'band':band_name})
    if response.status_code != 200:
        return '"It This Band Emo?" website (http://isthisbandemo.com) is currently not\
         responding [Error {}]'.format(response.status_code)

    max_len = 280
    img = None
    soup = BeautifulSoup(response.content, 'html.parser')
    main_answer = soup.find('h2').text
    if 'is an emo band' in main_answer:
        answer = 'Yes, ' + main_answer
    elif 'is not an emo band' in main_answer:
        answer = 'No, ' + main_answer

    sub_answer = soup.find('h4')
    if sub_answer:
        answer += '\n' + sub_answer.text
        link = sub_answer.find('a')
        if link and link.get('href'):
            answer += '\n' + link['href']
            max_len += len(link['href']) - 24
        img_tag = sub_answer.find('img')
        if img_tag:
            img = img_tag.get('src')

    if len(answer) > max_len:
        answer = '{}\n{}'.format(main_answer, response.url)
    return answer, img