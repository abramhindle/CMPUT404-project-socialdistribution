import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";
import { SocialSearch } from "./SocialSearch";
import { SocialSearchStyles as styles } from "./SocialSearch.styles";
import { SocialSearchTemplate as template } from "./SocialSearch.template";

export const socialSearch = {
    name: "social-search",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(socialSearch, SocialSearch));

provideFASTDesignSystem()
    .register();


