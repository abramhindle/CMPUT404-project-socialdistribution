import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";
import { Markdown } from "./Markdown";
import { MarkdownStyles as styles } from "./Markdown.styles";
import { MarkdownTemplate as template } from "./Markdown.template";

export const markdownComponent = {
    name: "markdown-component",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(markdownComponent, Markdown));

provideFASTDesignSystem()
    .register();


