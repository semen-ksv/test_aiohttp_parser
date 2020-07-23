from app_scraping.views import index, filtered


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/{letter}', filtered)