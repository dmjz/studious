$( document ).ready(function() {
    // Title writer
    var titleSourceElement  = $("#titleFormInput"),
        titleDestElement    = $("#title-target");

    updateTitle = function(e) {
        titleText = titleSourceElement.val();
        titleDestElement.text(titleText);
    };
    titleSourceElement.keyup(updateTitle);
    updateTitle()

    // Markdown conversion
    var markdownSourceElement   = $("#fullLessonFormTextarea"),
        markdownDestElement     = $("#preview-target"),
        converter               = new showdown.Converter();
    converter.setFlavor('github')

    convertMarkdown = function(e) {
        if (markdownSourceElement.is("textarea")) {
            markdownText = markdownSourceElement.val();
        } else if (markdownSourceElement.is("div")) {
            markdownText = markdownSourceElement.text();
        } else {
            throw "Expected a div or textarea as markdwonSourceElement";
        }
        convertedHtml = converter.makeHtml(markdownText);
        markdownDestElement.html(convertedHtml);
    };
    markdownSourceElement.keyup(convertMarkdown);
    convertMarkdown();
});