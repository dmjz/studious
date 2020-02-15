$( document ).ready(function() {

    // Markdown conversion
    var converter = new MarkdownConverter(
        source      = $("#lesson-body-source"),
        dest        = $("#lesson-body")
    );
})   