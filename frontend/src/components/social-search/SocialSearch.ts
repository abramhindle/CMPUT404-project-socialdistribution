import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import { FASTElement } from "@microsoft/fast-element";

export class SocialSearch extends FASTElement {
    constructor() {
        super()
        this.addIcons();
    }

    private addIcons() {
        library.add(faSearch);
    }
}