class MarkdownConverter {
    constructor(sourceString, destString, immediateConvert=true) {
        this.sourceString = sourceString;
        this.destString = destString;
        this.converter = window.markdownit({ html: false, typographer: true })
            .use(window.markdownitEmoji);
        if (immediateConvert) { this.convert_and_insert(); }
    }

    source() { return $(this.sourceString); }
    dest()   { return $(this.destString); }

    source_text() {
        var source = this.source();
        if (source.is("textarea")) { return source.val(); }
        else if (source.is("div")) { return source.text(); }
        else { throw "Expected a div or textarea as source element"; }
    }

    convert_and_insert() {
        // Get text, convert to HTML, insert
        var dest = this.dest();
        dest.html(this.converter.render(this.source_text()));
        // Fix some issues with the inserted HTML
        // -- Blockquotes
        dest.find("blockquote").addClass("blockquote");
        // -- Inline code
        dest.find("code").addClass("code");
        // -- Code blocks
        dest.find("code").each(function(index) {
            parent = $(this).parent()
            if (parent.is("pre")) { parent.addClass('code'); }
        });
        // -- Tables
        dest.find("table").addClass("table table-striped");
        // -- Images (make them fit in parent div)
        dest.find("img").addClass("img-fluid");
    }
}