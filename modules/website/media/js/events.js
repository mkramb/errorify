function highlight(line) {
    if (typeof(SyntaxHighlighter) != "undefined") {
        SyntaxHighlighter.defaults['highlight'] = line;
        SyntaxHighlighter.defaults['html-script'] = false;
        SyntaxHighlighter.defaults['toolbar'] = false;
        SyntaxHighlighter.all();

        var counter = 0;
        var interval = setInterval(function() {
            var element = $('.syntaxhighlighter');
            if (element.length) {
                window.clearInterval(interval);
                return element.scrollTop(
                    $('.highlighted:first', element).position().top
                        - (element.height() / 2)
                );
            }
            if (++counter > 10) {
                window.clearInterval(interval);
            }
        }, 100);
    }
}
