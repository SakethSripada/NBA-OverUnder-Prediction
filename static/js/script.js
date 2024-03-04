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

     $('#prediction_form').on('submit', function() {
    let formData = $(this).serialize();

    $.post('/', formData, function(data) {
        $('#resultModalBody').text(data);
        $('#resultModal').addClass('show');
        console.log('AJAX request successful, server responded with: ', data);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('AJAX request failed: ', textStatus, ', ', errorThrown);
    });

    return false;
});
        $('.btn-close').on('click', function() {
        $('#resultModal').removeClass('show');
    });
});