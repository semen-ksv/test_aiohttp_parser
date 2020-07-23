from motor import motor_asyncio


async def create_mongo(app):
    """
    Settings of mongoDB
    """
    settings = app['config']
    db = motor_asyncio.AsyncIOMotorClient(settings['mongo_uri'])[settings['db_name']]
    app['mongo'] = db

async def close_mongo(app):
    pass

def setup(app):
    app.on_startup.append(create_mongo)
    app.on_cleanup.append(close_mongo)