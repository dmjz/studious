class MarkdownConverter {
    constructor(sourceString, destString, immediateConvert=true, isJquerySource=true) {
        /* sourceString may be either a jQuery element identifier, or a String.
           This is indicated by the isJquerySource argument.
        */
        this.sourceString = sourceString;
        this.destString = destString;
        this.isJquerySource = isJquerySource;
        this.converter = window.markdownit({ html: false, typographer: true })
            .use(window.markdownitEmoji);
        if (immediateConvert) { this.convert_and_insert(); }
    }

    source() {
        if (!(this.isJquerySource)) { throw "Called source() but isJquerySource=false"; }
        return $(this.sourceString);
    }

    source_text() {
        if (!(this.isJquerySource)) { return this.sourceString; }
        var source = $(this.sourceString);
        if (source.is("textarea")) { return source.val(); }
        if (source.is("div")) { return source.text(); }
        throw "Expected a div or textarea as source element";
    }

    convert_and_insert() {
        // Get text, convert to HTML, insert
        var dest = $(this.destString);
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