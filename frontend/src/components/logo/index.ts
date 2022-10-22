import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";
import { Logo } from "./Logo";
import { LogoStyles as styles } from "./Logo.styles";
import { LogoTemplate as template } from "./Logo.template";

export const logoComponent = {
    name: "site-logo",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(logoComponent, Logo));

provideFASTDesignSystem()
    .register();


