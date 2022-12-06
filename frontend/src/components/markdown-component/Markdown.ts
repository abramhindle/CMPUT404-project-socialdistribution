import { FASTElement, observable } from "@microsoft/fast-element";
import { marked } from "marked";
import * as sanitizeHtml from 'sanitize-html';

export class Markdown extends FASTElement {
    @observable
    public content?: string;

    public getHTMLFromMarkdown(): string {
        if (!this.content) {
            return ""
        }

        return sanitizeHtml(marked.parse(this.content), {
            allowedTags: sanitizeHtml.defaults.allowedTags.concat([ 'img' ])
        })
    }
}
