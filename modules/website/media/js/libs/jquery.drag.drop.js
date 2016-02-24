/*
 * Copyright (c) 2011 Arron Bailiss <arron@arronbailiss.com>
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

(function($) {
    var settings = {
        'uploadUrl' : '/upload', // URL to POST files to
        'dropClass' : 'file-drop', // Default class for the drop div
        'dropHoverClass' : 'file-drop-hover', // Class applied to the drop div when dragging over it
        'defaultText' : 'Drop your files here!', // Default HTML content for the drop div
        'hoverText' : 'Let go, to upload!', // HTML content shown when hovering over the drop div
        'onUploaded' : null, // Callback function fired when files have been uploaded - defaults to methods.uploaded
        'onStartSending': null // Callback function fired when files start go to server
    };

    var $this = null,
        xhr = new XMLHttpRequest(),
        formData = new FormData();

    var methods = {
        // Initialises the plugin
        init : function(options) { 
            return $(this).each(function() {
                $this = $(this);

                if (options) {
                    $.extend(settings, options);
                }

                // Default callback
                if (settings.onUploaded === null) {
                    settings.onUploaded = methods.onUploaded;
                }

                if (methods.supported()) {
                    methods.createDropDiv();
                    methods.bindEvents();
                }
            });
        },
        // Checks support for functionality
        supported : function() { 
            return 'draggable' in document.createElement('span') && xhr.upload;
        },
        // Creates the div that files can be dropped on to
        createDropDiv : function() { 
            $dropDiv = $('<div>').addClass(settings.dropClass).html(settings.defaultText);
            $this.after($dropDiv);
        },
        // Bind plugin events
        bindEvents : function() { 
            $this.bind('change.dropUpload', methods.fileChange) // Bind event for manual file selection
                .next()
                .bind('dragenter.dropUpload dragleave.dropUpload', methods.dragHover) // Bind event for dragging file over/out of the drop area
                .bind('drop.dropUpload', methods.fileChange) // Bind event for drag+drop file selection
                .bind('dragover.dropUpload dragstart.dropUpload dragend.dropUpload', methods.cancelEvent); // Block events
        },
        // Fired when new files are selected manually or by drag+drop
        fileChange : function(e) { 
            methods.dragHover(e);
            var files = e.originalEvent.target.files || e.originalEvent.dataTransfer.files;

            for ( var i = 0, f; f = files[i]; i++) {
                formData.append(f.name, f); // Append each files to the form data
            }

            methods.sendFormData();
            return false;
        },
        // Sends (POST) populated form data to the upload URL
        sendFormData : function() {
            if (typeof(settings.onStartSending) != "undefined") {
                settings.onStartSending();
            }

            $.ajax({
                url : settings.uploadUrl,
                data : formData,
                cache : false,
                contentType : false,
                processData : false,
                type : 'POST',
                success : function(data) {
                    settings.onUploaded(data);
                }
            });

            // Reset form data
            formData = new FormData();
        },
        // Default callback
        onUploaded : function(resp) {
            console.log(resp);
        },
        // Fired when a file is dragged over the drop area
        dragHover : function(e) { 
            e.stopPropagation();
            e.preventDefault();

            // Add/remove class dropHoverClass to the drop area
            if ($this.next().hasClass(settings.dropHoverClass) || e.type == 'drop' || e.type == 'change') {
                $this.next().removeClass(settings.dropHoverClass).html(settings.defaultText);
            } else {
                $this.next().addClass(settings.dropHoverClass).html(settings.hoverText);
            }

            return false;
        },
        // Function to cancel an event's default behaviour
        cancelEvent : function(e) { 
            e.stopPropagation();
            e.preventDefault();
            return false;
        }
    };

    $.fn.dropUpload = function(method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.dropUpload');
        }
    };
})(jQuery);