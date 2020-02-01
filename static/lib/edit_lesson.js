$( document ).ready(function() {

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

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
    var examplesSourceElement   = $("#review-group"),
        examplesDestElement     = $("#examples-target");
    parseExamples = function() {
        examplesTexts = [];
        //// Note: hard-coded max 10 examples read here
        for (let i = 0; i < 10; i++) {
            var q   = $("#question-" + String(i)).val(),
                a   = $("#answer-" + String(i)).val();
            if (q || a) { 
                examplesTexts.push(
                    {
                        'question': escapeHtml(q), 
                        'answer': escapeHtml(a)
                    }
                );
            }
        }
        s = ""
        for (let i = 0; i < examplesTexts.length; i++) {
            ex = examplesTexts[i]
            s += '<div class="row"><div class="col-sm-4"> \
            <p class="lead"><strong>Q: </strong>' + ex['question'] + '</p> \
            </div><div class="col-sm-4"> \
            <p class="lead"><strong>A: </strong>' + ex['answer'] + '</p> \
            </div></div>'
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