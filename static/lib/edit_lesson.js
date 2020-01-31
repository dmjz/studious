$( document ).ready(function() {

    // Title writer
    var titleSourceElement  = $("#titleFormInput"),
        titleDestElement    = $("#title-target");

    updateTitle = function(e) {
        titleText = titleSourceElement.val();
        titleDestElement.text(titleText);
    };
    titleSourceElement.keyup(updateTitle);
    updateTitle();

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

    // Examples writer
    //
    // Note: hard-coded max of 10 review questions will be read here
    // This can be easily extended by just increasing the max to N
    // where N = max review questions per lesson.
    //
    var examplesSourceElement   = $("#review-group"),
        examplesDestElement     = $("#examples-target");
    parseExamples = function() {
        examplesTexts = [];
        for (let i = 0; i < 10; i++) {
            var q   = $("#question-" + String(i)).val(),
                a   = $("#answer-" + String(i)).val();
            if (q || a) { examplesTexts.push({'q': q, 'a': a}); }
        }
        console.log(examplesTexts)
        s = ""
        for (let i = 0; i < examplesTexts.length; i++) {
            ex = examplesTexts[i]
            s += "<p><em>Q: </em>" + ex['q'] + "  -- <em>A: </em>" + ex['a'] + "</p>\n";
        }
        return s;
    };
    updateExamples = function(e) {
        examplesHtml = parseExamples();
        examplesDestElement.html(examplesHtml);
    };
    examplesSourceElement.keyup(updateExamples);
    updateExamples();
});