import { FASTElement, observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Author } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { LayoutType } from "../../libs/core/PageModel";

export class Layout extends FASTElement {
    @observable
    public user?: Author | null;

    @observable
    public layoutStyleClass: string = "";

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;
}