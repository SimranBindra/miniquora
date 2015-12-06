Login = (function() {
    'use strict';
    function login(e) {
        e.preventDefault();
        var form = document.getElementById('login-form');
        var form_data = new FormData(form);
        var url = $(form).attr('action');
        console.log(url);
        $.ajax({
            url: url,
            type: 'POST',
            data: form_data,
            processData : false,
            dataType: 'json',
            contentType: false,
            success: function(data, status, xhr) {
                console.log(data);
                location.href = '/account/home/';
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseJSON);
                var form_errors = xhr.responseJSON['errors'];
                var i  = 0;
                
                if ('__all__' in form_errors) {
                    var non_field_errors = form_errors['__all__'];
                    var div = $('<div class="non_field_errors"/>');
                    for (i = 0; i < non_field_errors.length;i++) {
                        div.append('<small class="error">' + non_field_errors[i] + '</small>');
                    }
                    $(form).prepend(div);
                    delete form_errors['__all__'];
                }
                for(var field_name in form_errors) {
                    $('#id_'+field_name+'_container').addClass('has-error');
                    $('#id_'+field_name).addClass('invalid');
                    var field_errors_div = $('<div class="errors"/>');
                    for (i = 0; i < form_errors[field_name].length; i++) {
                        field_errors_div.append('<small class="error">' + form_errors[field_name][i] + '</small>');
                    }
                    $('#id_'+field_name+'_container').append(field_errors_div);
                }
            }
        });
    }
    function init() {
        $('#login-btn').click(login);
    }
    return {
        init : init
    };
})();
