import { html } from "@microsoft/fast-element";
import { Markdown } from "./Markdown";

export const MarkdownTemplate = html<Markdown>`
    <div class="markdown-root" :innerHTML="${x => x.getHTMLFromMarkdown()}"></div>
`;