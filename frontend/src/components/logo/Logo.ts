import { FASTElement, observable } from "@microsoft/fast-element";

export class Logo extends FASTElement {
    @observable
    public logoUrl = require('../../assets/images/LogoIcon.png').default;
}