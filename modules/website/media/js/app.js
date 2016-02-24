$(function(){
    bootbox.animate(false);

    $('select.chosen').chosen();
    $('.alert:not(.dont-hide)').delay(3000).slideToggle();

    $('.toggle-filter').on('click', function(e) {
        $('.filter').slideDown();
        e.preventDefault();
    });

    $('.dialog-confirm').on('click', function(e) {
        bootbox.confirm($(this).attr('title'), $.proxy(function(result) {
            if (result) {
                window.location = $(this).attr("href");
            }
        }, this));

        e.preventDefault();
        return false;
    });
});
