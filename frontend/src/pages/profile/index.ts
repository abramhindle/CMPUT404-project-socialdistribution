import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { Profile } from "./Profile";
import { ProfilePageStyles as styles } from "./Profile.styles";
import { ProfilePageTemplate as template } from "./Profile.template";

export const profilePage = {
    name: "profile-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(profilePage, Profile));

provideFASTDesignSystem()
      .register();
