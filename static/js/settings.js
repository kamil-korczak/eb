$(document).ready(function(){

    function addForm(e, prefix, field_name, position=null){
        e.preventDefault();

        let form = $('.form-'+prefix);

        let formRegex = RegExp(`${prefix}-(\\d){1}-`,'g')
        let object_before = '<div class="col-3"></div>';
        let formNum = form.length-1;
        let totalForms = $(`#id_${prefix}-TOTAL_FORMS`);

        let newForm = form.eq(0).clone();

        formNum++;

        newForm.html(newForm.html().replace(formRegex, `${prefix}-${formNum}-`));

        newForm.find(`#id_${prefix}-${formNum}-${field_name}`).val('');


        if(position){ newForm.find(`#id_${prefix}-${formNum}-${position}`).val('0'); }

        $('#formset-rows-'+prefix).append(`<div class="row row-${prefix}"></div>`);

        $('#formset-rows-'+prefix+' .row-'+prefix+':last').append(object_before,  $(newForm));

        totalForms.prop('value', formNum+1);
    }

    $('form#settings-form').on('click', '#add-account', function(event) {
        addForm(event, prefix='account', field_name='company_account');
    });

    $('form#settings-form').on('click', '#add-ebay-category', function(event) {
        addForm(event, prefix='ebay-category', field_name='ebay_category', position='position');
    });

});