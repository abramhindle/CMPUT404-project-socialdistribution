import { attr, FASTElement } from "@microsoft/fast-element";

export class LikesModal extends FASTElement {
  @attr greeting: string = 'Likes Modal';

  public connectedCallback() {
    super.connectedCallback();
  }
}
