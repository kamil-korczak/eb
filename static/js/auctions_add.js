$(document).ready(function(){

    function checkRadioChecked(){
       setFormFieldDisable($("input[type=radio]:checked"));
    }

    function setFormFieldDisable(element){
        $('form#add-auction-type .input-auctions').each(function() {
            $(this).prop('disabled', true );
            $(this).removeClass('disabled');
        });

        elem_searched = $(element).closest('.input-group').find('.input-auctions');
        elem_searched.prop('disabled', false );
        elem_searched.focus();
        
    }

    checkRadioChecked();

    $('form#add-auction-type').on('click', 'input[type=radio]', function(event) {
        setFormFieldDisable(this);
    });

});