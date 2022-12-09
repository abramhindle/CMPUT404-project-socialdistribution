import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { AuthorInfo } from "./AuthorInfo";
import { AuthorInfoStyles as styles } from "./AuthorInfo.styles";
import { AuthorInfoTemplate as template } from "./AuthorInfo.template";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";

export const authorInfo = {
    name: "author-info",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(authorInfo, AuthorInfo));

provideFASTDesignSystem()
    .register();


