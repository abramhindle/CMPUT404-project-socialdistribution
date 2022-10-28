import {provideFASTDesignSystem} from "@microsoft/fast-components";
import {ComponentEntry, defineComponent} from "../../pages/AppRegistry";
import {CommentModal} from "./CommentModal";
import {CommentModalComponentStyles as styles} from "./styles/CommentModal.styles";
import {CommentModalTemplate as template} from "./CommentModal.template";

export const commentModalComponent = {
  name: 'comment-modal',
  template,
  styles,
  shadowOptions: {
    delegatesFocus: true,
  }
};

defineComponent(new ComponentEntry(commentModalComponent, CommentModal));

provideFASTDesignSystem()
  .register();
