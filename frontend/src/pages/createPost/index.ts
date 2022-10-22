import {provideFASTDesignSystem} from "@microsoft/fast-components";
import {ComponentEntry, defineComponent} from "../AppRegistry";

import {CreatePost} from "./CreatePost";
import {CreatePostPageStyles as styles} from "./styles/CreatePost.styles";
import {CreatePostPageTemplate as template} from "./CreatePost.template";

export const createPostPage = {
  name: 'create-post-page',
  template,
  styles,
  shadowOptions: {
    delegatesFocus: true
  }
}

defineComponent(new ComponentEntry(createPostPage, CreatePost));

provideFASTDesignSystem()
  .register();
