import {provideFASTDesignSystem} from "@microsoft/fast-components";
import {ComponentEntry, defineComponent} from "../../pages/AppRegistry";
import {LikesModal} from "./LikesModal";
import {LikesModalComponentStyles as styles} from "./styles/LikesModal.styles";
import {LikesModalTemplate as template} from "./LikesModal.template";

export const likesModalComponent = {
  name: 'likes-modal',
  template,
  styles,
  shadowOptions: {
    delegatesFocus: true,
  }
};

defineComponent(new ComponentEntry(likesModalComponent, LikesModal));

provideFASTDesignSystem()
  .register();
