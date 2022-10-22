import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Page } from "../Page";

export class SignOn extends Page {
    @observable
    public errorMessages?: string[];

    public form?: HTMLFormElement;

    constructor() {
        super();
        this.errorMessages = [];
    }

    public connectedCallback() {
        super.connectedCallback();
    }

    register(e: Event) {
        e.preventDefault();

        if (!this.form) {
            return;
        }
        
        this.errorMessages = [];
        SocialApi.register(new FormData(this.form)).then(
            errorMessages => {
                this.errorMessages?.push(...errorMessages);
                console.log(this.errorMessages);
            }
        );
    }
}