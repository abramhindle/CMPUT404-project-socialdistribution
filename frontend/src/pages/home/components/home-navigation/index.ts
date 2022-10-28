import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { HomeNavigation } from "./HomeNavigation";
import { HomeNavigationStyles as styles } from "./HomeNavigation.styles";
import { HomeNavigationTemplate as template } from "./HomeNavigation.template";
import { ComponentEntry, defineComponent } from "../../../AppRegistry";

export const homeNavigation = {
    name: "home-navigation",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(homeNavigation, HomeNavigation));

provideFASTDesignSystem()
    .register();


