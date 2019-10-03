import responder
from elasticsearch import Elasticsearch
import settings

api = responder.API()
es = Elasticsearch(settings.ELASTICSEARCH_SERVER)


@api.route("/")
async def index(req, resp):
    result_list = []

    search_string = req.params.get('search')

    if search_string:
        search_result = es.search(index=settings.ELASTICSEARCH_INDEX, size=30, q=f'*"{search_string}"*')
    else:
        search_result = es.search(index=settings.ELASTICSEARCH_INDEX, size=30, sort='meta.added_at:desc')

    result_list = [hit['_source'] for hit in search_result['hits']['hits']]

    resp.html = api.template('index.html', result_list=result_list)


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

        await ws.send_json([hit['_source']['title'] for hit in search_result['hits']['hits']])

    # await ws.close()


if __name__ == '__main__':
    api.run()
