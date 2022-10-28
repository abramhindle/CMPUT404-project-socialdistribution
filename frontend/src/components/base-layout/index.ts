import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";
import { Layout } from "./Layout";
import { LayoutStyles as styles } from "./Layout.styles";
import { LayoutTemplate as template } from "./Layout.template";

export const layoutComponent = {
    name: "page-layout",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(layoutComponent, Layout));

provideFASTDesignSystem()
    .register();


