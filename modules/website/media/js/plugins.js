$.fn.clearForm = function() {
    return this.each(function() {
        var type = this.type,
            tag = this.tagName.toLowerCase(),
            css = this.className;

        if (tag == 'form') {
            $('.error', $(this)).removeClass('error');
            $('.alert-error, .help-inline', $(this)).remove();
            return $(':input',this).clearForm();
        }

        if (css.indexOf('dont-clear') < 0) {
            if (type == 'text' || type == 'password' || tag == 'textarea' || type == 'file') {
                this.value = '';
            }
            else if (type == 'checkbox' || type == 'radio') {
                this.checked = false;
            }
            else if (tag == 'select') {
                $(this).val('').change();
            }
        }
    });
};

$.fn.highlight = function(options) {
    var settings = {
        start_color:"#ff0",
        end_color:"#fff",
        delay:1000
    };

    if (options) {
        $.extend(settings, options);
    }

    $(this).each(function() {
        $(this).stop().css({"background-color":settings.start_color}).animate(
            {"background-color":settings.end_color}, settings.delay
        );
    });
};