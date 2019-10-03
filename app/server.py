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

        if not search_string:
            await ws.send_json([])
            continue

        # TODO: could block the main loop.
        # TODO: exclude unwanted fields
        search_result = es.search(index=settings.ELASTICSEARCH_INDEX, size=10, q=f'*"{search_string}"*')

        await ws.send_json([hit['_source']['symbol'] for hit in search_result['hits']['hits']])

    # await ws.close()


if __name__ == '__main__':
    api.run()
