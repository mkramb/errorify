$(function(){
    $('.modal-hide-upload').on('click', function(e) {
        if (!window.uploading) {
            var div = $(this).closest('.modal');
            $('form', div).clearForm();
            e.preventDefault();

            if (window.uploaded_files.length) {
                window.uploaded_files = [];
                window.location.reload();
            }
            else {
                div.modal('hide');
            }
        }
        else {
            setTimeout(function() {
                $('.modal-hide-upload').trigger('click');
            }, 1000);
        }
    });

    $("a[draggable]").on("dragstart", function(e){
        e.originalEvent.dataTransfer.setData(
            "DownloadURL", $(this).data('downloadurl')
        );
    });

    if (!uploadSupported()) {
        $('#modal-upload-resources .modal-submit').show();
    }
});

function startUploadCheck() {
    window.upload_interval = setInterval(function() {
        var form = $('#modal-upload-resources form'),
            message = $('#modal-upload-resources .message');

        if (window.uploading && form.is(":visible")) {
            form.hide('fast', function() { message.show(); });
        }
        else {
            window.clearInterval(window.upload_interval);
            if (message.is(":visible")) {
                message.hide('normal', function() { form.show();});
            }
        }
    }, 1000);
}