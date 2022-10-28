import { provideFASTDesignSystem } from "@microsoft/fast-components";
import { FeedPost } from "./FeedPost";
import { FeedPostStyles as styles } from "./FeedPost.styles";
import { FeedPostTemplate as template } from "./FeedPost.template";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";

export const feedPost = {
    name: "feed-post",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(feedPost, FeedPost));

provideFASTDesignSystem()
    .register();


