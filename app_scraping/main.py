import asyncio

from aiohttp import web
from app_scraping.parser import parser
from app_scraping.routes import setup_routes
import aiohttp_jinja2
import jinja2

from app_scraping.settings import load_config
import app_scraping.mongo as mongo

"""
Created on July 23, 2020
@author: Semen Kotsyuruba
"""

async def create_app():
    """app configurations"""
    app = web.Application()
    conf = load_config()
    app['config'] = conf
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('app_scraping', 'templates'))
    mongo.setup(app)
    setup_routes(app)
    return app

def main():
    """start app and parsing process when open index page '/' """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser())

    app = create_app()
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()