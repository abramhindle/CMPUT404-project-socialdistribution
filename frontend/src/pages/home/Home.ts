import { baseHeightMultiplier, neutralColor } from "@microsoft/fast-components";
import { attr, FASTElement, observable } from "@microsoft/fast-element";

export class Home extends FASTElement {
    @observable
    public isAuth: boolean = false;

    public connectedCallback() {
        super.connectedCallback();
    }
}