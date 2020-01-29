$( document ).ready(function() {
    var markdownSourceElement   = $("#fullLessonFormTextarea"),
        markdownDestElement     = $("#preview-target"),
        converter               = new showdown.Converter();
    converter.setFlavor('github')

    convertMarkdown = function(e) {
        markdownText = markdownSourceElement.val();
        convertedHtml = converter.makeHtml(markdownText);
        markdownDestElement.html(convertedHtml);
    };

    markdownSourceElement.keyup(convertMarkdown);
    convertMarkdown();
});