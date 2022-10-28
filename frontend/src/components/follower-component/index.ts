import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { Follower } from "./Follower";
import { FollowerStyles as styles } from "./Follower.styles";
import { FollowerTemplate as template } from "./Follower.template";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";

export const followerComponent = {
    name: "follower-component",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(followerComponent, Follower));

provideFASTDesignSystem()
    .register();


