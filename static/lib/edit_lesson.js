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
    var converter = new MarkdownConverter(
        sourceString    = "#fullLessonFormTextarea",
        destString      = "#preview-target"
    );
    converter.source().on('keyup', function () { converter.convert_and_insert(); })

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

    // Resize the lesson preview div when either it or the edit form are resized
    var previewDiv = $('#preview-container');
    var editForm = $('#edit-form');
    previewDiv.height(editForm.height())
    var resize_preview = function() {
        previewDiv.height( editForm.height() );
    };
    previewDiv.on('resize', resize_preview);
    editForm.on('resize', resize_preview);

});