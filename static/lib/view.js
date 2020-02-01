$( document ).ready(function() {

    // Markdown conversion
    var markdownSourceElement   = $("#lesson-body-source"),
        markdownDestElement     = $("#lesson-body"),
        converter               = new showdown.Converter();
    converter.setFlavor('github')

    convertMarkdown = function(e) {
        if (markdownSourceElement.is("textarea")) {
            markdownText = markdownSourceElement.val();
        } else if (markdownSourceElement.is("div")) {
            markdownText = markdownSourceElement.text();
        } else {
            throw "Expected a div or textarea as markdownSourceElement";
        }
        convertedHtml = converter.makeHtml(markdownText);
        markdownDestElement.html(convertedHtml);
    };
    convertMarkdown();
});