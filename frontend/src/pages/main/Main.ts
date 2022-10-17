import { attr, FASTElement } from "@microsoft/fast-element";

export class Main extends FASTElement {
    @attr greeting: string = 'Hello';

    public connectedCallback() {
        super.connectedCallback();
        console.log('Hello world!');
    }
}