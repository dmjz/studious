$( document ).ready(function() {

    // Markdown conversion
    var markdownSourceElement   = $("#lesson-body-source"),
        markdownDestElement     = $("#lesson-body"),
        converter               = window.markdownit({ html: false, typographer: true });
    convertMarkdown = function(e) {
        if (markdownSourceElement.is("textarea")) {
            markdownText = markdownSourceElement.val();
        } else if (markdownSourceElement.is("div")) {
            markdownText = markdownSourceElement.text();
        } else {
            throw "Expected a div or textarea as markdwonSourceElement";
        }
        convertedHtml = converter.render(markdownText);
        markdownDestElement.html(convertedHtml);
    };
    convertMarkdown();
});