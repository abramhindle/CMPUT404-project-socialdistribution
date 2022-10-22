import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { SignOn } from "./SignOn";
import { SignOnPageStyles as styles } from "./SignOn.styles";
import { SignOnPageTemplate as template } from "./SignOn.template";

export const signOnPage = {
    name: "signon-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(signOnPage, SignOn));

provideFASTDesignSystem()
      .register();
