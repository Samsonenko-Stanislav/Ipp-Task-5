import typing

if typing.TYPE_CHECKING:
    from aiohttp.web_app import Application


def setup_routes(app: "Application"):
    from IppTask5.app.contact.api.routes import setup_routes as setup_api_routes
    from IppTask5.app.contact.html.routes import setup_routes as setup_html_routes
    setup_api_routes(app)
    setup_html_routes(app)
