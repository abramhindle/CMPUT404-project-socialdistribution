import {provideFASTDesignSystem} from "@microsoft/fast-components";
import {ComponentEntry, defineComponent} from "../AppRegistry";

import {EditPost} from "./EditPost";
import {EditPostPageStyles as styles} from "./styles/EditPost.styles";
import {EditPostPageTemplate as template} from "./EditPost.template";


export const editPostPage = {
  name: 'edit-post-page',
  template,
  styles,
  shadowOptions: {
    delegatesFocus: true
  }
}

defineComponent(new ComponentEntry(editPostPage, EditPost));

provideFASTDesignSystem()
  .register();
