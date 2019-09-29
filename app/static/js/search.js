const ws = new WebSocket('ws://localhost:5042/ws/search');

ws.onmessage = show_suggestions;

function search_suggestion(search_string) {
    ws.send(search_string);
}


function show_suggestions(data) {
    // TODO: show suggestions below input field
    for (let i=0; i<data.length; i++) {

    }
}