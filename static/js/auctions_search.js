function validate(){
    if( 
        $('#id_external_id').val() == '' &&
        $('#id_title').val() == '' &&
        $('#id_company_accounts').val() == '' &&
        $('#id_auctions_display').val() == 1
    ){
        return false;
    } else {
        return true;
    }
}


$(document).ready(function(){
    // $('#search-auctions-button').click(function(){
    //     if ( validate()) { $('#auctions-search-form').submit(); }
    // });
});



