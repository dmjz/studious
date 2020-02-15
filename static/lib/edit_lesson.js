$( document ).ready(function() {

    function escapeHtml(text) {
        return text
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/&/g, "&amp;");
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
    var converter = new MarkdownConverter(
        source      = $("#fullLessonFormTextarea"),
        dest        = $("#preview-target"),
        attachKeyup = true
    );

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
                examplesTexts.push({ 'question': q, 'answer': a });
            }
        }
        return examplesTexts;
    };
    updateExamples = function(e) {
        examplesHtml = parseExamples();
        examplesDestElement.html('');
        for (let i = 0; i < examplesTexts.length; i++) {
            ex = examplesTexts[i];
            examplesDestElement.append(
                '<div class="row"><div class="col-sm-4"> \
                <p class="lead"><strong>Q: </strong><span id="q-text-' + String(i) + '"</p> \
                </div><div class="col-sm-4"> \
                <p class="lead"><strong>A: </strong><span id="a-text-' + String(i) + '"</p> \
                </div></div>'
            );
            $("#q-text-" + String(i)).text(ex['question']);
            $("#a-text-" + String(i)).text(ex['answer']);
        }
        //examplesDestElement.html(examplesHtml);
    };
    examplesSourceElement.keyup(updateExamples);
    updateExamples();
});