$(document).ready(function() {
    $('#playerName').on('input', function() {
        let query = $(this).val();
        if (query.length > 2) {
            $.getJSON('/search_players', {query: query}, function(data) {
                let dataList = $('#playerNames');
                dataList.empty();
                data.forEach(function(item) {
                    dataList.append($('<option>').val(item));
                });
            });
        }
    });
});