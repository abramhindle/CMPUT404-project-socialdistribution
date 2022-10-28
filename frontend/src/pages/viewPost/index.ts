import {provideFASTDesignSystem} from "@microsoft/fast-components";
import {ComponentEntry, defineComponent} from "../AppRegistry";

import {ViewPost} from "./ViewPost";
import {ViewPostPageStyles as styles} from "./styles/ViewPost.styles";
import {ViewPostPageTemplate as template} from "./ViewPost.template";


export const viewPostPage = {
  name: 'view-post-page',
  template,
  styles,
  shadowOptions: {
    delegatesFocus: true
  }
}

defineComponent(new ComponentEntry(viewPostPage, ViewPost));

provideFASTDesignSystem()
  .register();
