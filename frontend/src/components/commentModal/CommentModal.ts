import { attr, FASTElement } from "@microsoft/fast-element";

export class CommentModal extends FASTElement {
  @attr greeting: string = 'Comment Modal';

  public connectedCallback() {
    super.connectedCallback();
  }
}
