from aiohttp import web
from aiohttp_jinja2 import template
from pymongo import MongoClient
from app_scraping.settings import load_config

settings = load_config()

client = MongoClient(settings['mongo_uri'])

db = client[settings['db_name']]


@template('result_list.html')
async def index(request):
    """
    generate main page '/' with information about all result what was scraped
    """
    results = db.result.find()
    all_results = []
    for result in results:
        # create list with all results
        all_results.append(dict(result))
    return {'results': all_results, 'start': 'All results'}


@template('result_list.html')
async def filtered(request):
    """
    generate page '/{letter}' with information witch was sorted by first letter
    """
    start_word = str(request.match_info['letter'])
    if len(start_word) > 1:
        # return information about incorrect firs letter
        return {'start': f'incorrect letter "{start_word}"'}
    results = db.result.find({"event": {'$regex': f"^[{start_word.upper()}{start_word.lower()}]"}})

    all_results = []
    for result in results:
        # create list with all results
        all_results.append(dict(result))
    return {'results': all_results, 'start': f'Results started with letter "{start_word}"'}
