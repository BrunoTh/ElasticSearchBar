import responder

api = responder.API()


@api.route("/")
async def index(req, resp):
    resp.html = api.template('index.html')


@api.route("/ws/search", websocket=True)
async def ws_search(ws):
    await ws.accept()

    while True:
        search_string = await ws.receive_text()
        # TODO: do the search
        await ws.send_json()

    await ws.close()


if __name__ == '__main__':
    api.run()
