import { attr, FASTElement } from "@microsoft/fast-element";

export class TemplateComponent extends FASTElement {
    @attr greeting: string = 'Using a template component';

    public connectedCallback() {
        super.connectedCallback();
    }
}