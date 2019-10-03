import responder
from elasticsearch import Elasticsearch
import settings

api = responder.API()
es = Elasticsearch(settings.ELASTICSEARCH_SERVER)


@api.route("/")
async def index(req, resp):
    resp.html = api.template('index.html')


@api.route("/ws/search", websocket=True)
async def ws_search(ws):
    await ws.accept()

    while True:
        search_string = await ws.receive_text()

        search_result = es.search(index=settings.ELASTICSEARCH_INDEX, q=search_string)

        # TODO: exclude unwanted fields

        await ws.send_json({})

    await ws.close()


if __name__ == '__main__':
    api.run()
