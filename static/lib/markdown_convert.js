
class MarkdownConverter {
    constructor(source, dest, attachKeyup=false, immediateConvert=true) {
        this.source = source;
        this.dest = dest;
        this.converter = window.markdownit({ html: false, typographer: true });
        if (attachKeyup) { this.source.keyup(this.convert_and_insert); }
        if (immediateConvert) { this.convert_and_insert(); }
    }

    source_text() {
        if (this.source.is("textarea")) {
            return this.source.val();
        } else if (this.source.is("div")) {
            return this.source.text();
        } else {
            throw "Expected a div or textarea as source element";
        }
    }

    convert_and_insert() {
        // Get text, convert to HTML, insert
        this.dest.html(this.converter.render(this.source_text()));
        // Fix some issues with the inserted HTML
        // -- Blockquotes
        this.dest.find("blockquote").addClass("blockquote");
        // -- Inline code
        this.dest.find("code").addClass("code");
        // -- Code blocks
        this.dest.find("code").each(function(index) {
            parent = $(this).parent()
            if (parent.is("pre")) { parent.addClass('code'); }
        });
    }
}