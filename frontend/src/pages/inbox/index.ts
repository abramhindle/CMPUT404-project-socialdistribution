import { provideFASTDesignSystem} from "@microsoft/fast-components";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { Inbox } from "./Inbox";
import { InboxPageStyles as styles } from "./Inbox.styles";
import { InboxPageTemplate as template } from "./Inbox.template";

export const inboxPage = {
    name: "inbox-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(inboxPage, Inbox));

provideFASTDesignSystem()
      .register();
