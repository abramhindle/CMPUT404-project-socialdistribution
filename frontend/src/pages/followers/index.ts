import { provideFASTDesignSystem} from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { Followers } from "./Followers";
import { FollowersPageStyles as styles } from "./Followers.styles";
import { ProfilePageTemplate as template } from "./Followers.template";

export const followersPage = {
    name: "followers-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(followersPage, Followers));

provideFASTDesignSystem()
      .register();
