import { html } from "@microsoft/fast-element";
import { Markdown } from "./Markdown";

export const MarkdownTemplate = html<Markdown>`
    <div :innerHTML="${x => x.getHTMLFromMarkdown()}"></div>
`;