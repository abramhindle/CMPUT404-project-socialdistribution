import { FASTElement, observable } from "@microsoft/fast-element";
import { LayoutType } from "../../libs/core/PageModel";

export class Logo extends FASTElement {
    @observable
    public logoUrl = require('../../assets/images/LogoIcon.png').default;

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;

    @observable
    public layoutStyleClass: string = "";

    layoutTypeChanged(old: any, newval: any) {
        console.log(old, newval)
    }
}