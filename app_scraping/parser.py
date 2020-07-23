import aiohttp
import time
from pymongo import MongoClient
from app_scraping.settings import load_config

# load config of data base
settings = load_config()
client = MongoClient(settings['mongo_uri'])
db = client[settings['db_name']]

headers = {'user-agent': 'Chrome (Windows 7; B; br) Presto/2.2.15 Version/10.10'}

# body of request to api of www.fonbet.ru
body = {
    "requests": [
        {

            "sports": '{name: "Футбол", fonbetId: 1, id: "1"}, {name: "Хоккей", fonbetId: 2, id: "2"},'
                      '{name: "Баскетбол", fonbetId: 3, id: "3"},'
                      '{name: "Баскетбол 3x3", fonbetId: 47041, id: "4"},'
                      '{name: "Волейбол", fonbetId: 9, id: "5"},'
                      '{name: "Теннис", fonbetId: 4, id: "6"},'
                      '{name: "Наст. теннис", fonbetId: 3088, id: "7"},'
                      '{name: "Гандбол", fonbetId: 8, id: "8"},'
                      '{name: "Водное поло", fonbetId: 1219, id: "9"},'
                      '{name: "Футзал", fonbetId: 1434, id: "10"},'
                      '{name: "Пляжный волейбол", fonbetId: 11624, id: "11"},'
                      '{name: "Пляжный гандбол", fonbetId: 11626, id: "12"},'
                      '{name: "Пляжный футбол", fonbetId: 11625, id: "13"},'
                      '{name: "Флорбол", fonbetId: 11627, id: "14"},'
                      '{name: "Регби", fonbetId: 16, id: "15"},'
                      '{name: "Автогонки", fonbetId: 7, id: "16"},'
                      '{name: "Австралийский футбол", fonbetId: 11638, id: "17"},'
                      '{name: "Бадминтон", fonbetId: 11630, id: "18"},'
                      '{name: "Бильярд", fonbetId: 1429, id: "19"},'
                      '{name: "Бейсбол", fonbetId: 5, id: "20"},'
                      '{name: "Бокс", fonbetId: 1436, id: "21"},'
                      '{name: "Единоборства", fonbetId: 37145, id: "22"},'
                      '{name: "Крикет", fonbetId: 11634, id: "23"},'
                      '{name: "Гольф", fonbetId: 11631, id: "24"},'
                      '{name: "Дартс", fonbetId: 11632, id: "25"},'
                      '{name: "Шахматы", fonbetId: 1437, id: "26"},'
                      '{name: "Киберспорт", fonbetId: 29086, id: "27"},'
                      '{name: "Кибербаскетбол", fonbetId: 40481, id: "28"},'
                      '{name: "Rocket League", fonbetId: 44943, id: "29"},'
                      '{name: "Разное", fonbetId: 1435, id: "30"},'
                      '{name: "Лотереи", fonbetId: 41963, id: "31"},'
                      '{name: "Лошадиные скачки", fonbetId: 52041, id: "32"},'
                      '{name: "Крикет", fonbetId: 6596, id: "33"},'
                      '{name: "Собачьи бега", fonbetId: 52042, id: "34"},'
                      '{name: "Сумо", fonbetId: 54560, id: "35"},'
                      '{name: "Хоккей на траве", fonbetId: 1439, id: "36"},'
                      '{name: "Нетбол", fonbetId: 15396, id: "37"}'
        }

    ]
}


async def fetch(client, url):
    """
    sending post request with headers and body
    :param client: aiohttp
    :param url: url of api server
    :return: json
    """
    async with client.post(url, headers=headers, json=body) as resp:
        assert resp.status == 200
        return await resp.json()


async def parser():
    """
    Parsing information from api server
    :return: result save in mongoDB
    """
    # url of api server
    post_url = 'https://clientsapi41.bkfon-resource.ru/results/results.json.php?locale=ru&lastUpdate=0&_=1595425218361'

    async with aiohttp.ClientSession() as client:
        get_json = await fetch(client, post_url)
        # get all events from json
        results = get_json.get("events")
        # words witch have key 'name' but is not the result
        exception_name = 'угловые , ж/карты , штанги или перекладины , вброс аутов , удары от ворот ,' \
                         ' видеопросмотры , фолы , удары в створ , офсайды , буллиты  '
        # delete previous data from db
        db.result.remove()
        for result in results:

            if result['name'] not in exception_name:
                finish_result = (str(result['score']).replace(' ', ',')).split(',')[0]
                start_time = str(time.ctime(result['startTime'])).strip('2020')
                result_to_db = {'event': result['name'],
                                'finish_result': finish_result,
                                'start_time': start_time,
                                'status': result['status']
                                }

                results = db.result  # save data in db
                results.insert_one(result_to_db)
