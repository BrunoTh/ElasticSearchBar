const ws = new WebSocket('ws://localhost:5042/ws/search');
ws.onmessage = function(e) {show_suggestions(JSON.parse(e.data))};
let autocomplete_instance = null;

document.addEventListener('DOMContentLoaded', function() {
    let elements = document.querySelectorAll('.autocomplete');
    M.Autocomplete.init(elements);

    autocomplete_instance = M.Autocomplete.getInstance(document.getElementById('search'));
    autocomplete_instance.onAutocomplete = function(e) {console.log(e)};
});

function search_suggestion(search_string) {
    ws.send(search_string);
}


function show_suggestions(data) {
    // TODO: show suggestions below input field
    let result = {};
    for (let i=0; i<data.length; i++) {
        result[data[i]] = null;
    }

    autocomplete_instance.updateData(result);
    autocomplete_instance.open();
}