$(document).ready(function(){


    var css_active_row = 'table-info';
    var auction_selected_url = '/api/auctions/';

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", csrftoken /*getCookie('csrftoken') */);
            }
        }
    });

    function postAuctionSelect(pk, selected_status, element=false){
        data = { selected: selected_status }

        return $.post( auction_selected_url  + pk + '/',  data, 
           // function( result_data, status ) { /* hmm ? */ }
            ).done(function() {
            if(element) setCheckboxAuction(element, selected_status);
        });
        // jqxhr.fail(function(){
        //     console.log('fail: error');
        // });

    }

    function setCheckboxAuction(element, selected_status){

        if ( selected_status == 0 ){
            $(element).prop('checked', false);
            $(element).closest('tr').removeClass(css_active_row)
        } else if ( selected_status == 1 ){
            $(element).prop('checked', true);
            $(element).closest('tr').addClass(css_active_row)
        }
    }

    function isCheckedAuction(element){

        element = $(element).find('input:checkbox');

        auction_id = $(element).val().replace('acb_','');

        if( $(element).prop('checked') == false ){

            postAuctionSelect(auction_id, 1, element);

        } else if ( $(element).prop('checked') == true ){
            
            post = postAuctionSelect(auction_id, 0, element);
        }
    }

    $('table.auctions tr .form-check:checked').each(function() {
        $(this).closest('tr').addClass(css_active_row);
    });

    $('#auctions-all').on('click', 'table.auctions td.auction-action', function(event) {
        isCheckedAuction(this);
    });
    
});