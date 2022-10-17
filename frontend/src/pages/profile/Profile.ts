import { attr, FASTElement } from "@microsoft/fast-element";

export class Profile extends FASTElement {
    @attr greeting: string = 'Hello';

    public connectedCallback() {
        super.connectedCallback();
    }
}