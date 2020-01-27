$( document ).ready(function() {
    var markdownSourceElement   = $("#fullLessonFormTextarea"),
        markdownDestElement     = $("#preview-target"),
        markdownConvertButton   = $("#preview-button"),
        converter               = new showdown.Converter();

    markdownConvertButton.click(function() {
        markdownText = markdownSourceElement.val();
        convertedHtml = converter.makeHtml(markdownText);
        markdownDestElement.html(convertedHtml);
    });
});