$(function(){
    $('#sidebar > .vertical').slideToggle('slow');

    $("a[rel^=external]").live('click', function(event) {
        $(this).attr('target', '_blank');
        return event;
    });

    $('.modal-show').on('click', function(e) {
        var div = $('#' + $(this).data('modal'));
        div.modal({
            keyboard: false,
            backdrop: 'static'
        });
        div.modal('show');
        e.preventDefault();
    });

    $('.modal input').on('keypress', function(e) {
        if (e.which == 13) { // enter
            $('.modal-submit').trigger('click');
        }
    });

    $('.modal-hide').on('click', function(e) {
        var div = $(this).closest('.modal');
        $('form', div).clearForm();
        div.modal('hide');
        e.preventDefault();
    });

    $('.modal-submit').on('click', function(e) {
        $('form', $(this).closest('.modal')).submit();
        e.preventDefault();
    });
});

$(document).ajaxSend(function(event, xhr, settings) {
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
    }
});

$.ajaxSetup({
    crossDomain: false,
    cache: false,
    error: function(xhr, exception) {
        alert('Application error occurred, please refresh current page.')
    }
});

function uploadSupported() {
    return 'draggable' in document.createElement('span') && new XMLHttpRequest().upload;
}