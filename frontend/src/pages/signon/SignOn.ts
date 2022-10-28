import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Page } from "../Page";

export const SignOnType = Object.freeze({
    Register: "Register",
    Login: "Login",
    Logout: "Logout"
} as const);

export type SignOnType = keyof typeof SignOnType;

export class SignOn extends Page {
    @observable
    public errorMessages: string[] = [];

    @observable
    public signOnType?: SignOnType;

    public form?: HTMLFormElement;

    constructor() {
        super();
        const signOnType = this.getAttribute("signOnType");
        this.removeAttribute("signOnType");
        this.signOnType = this.parseSignOnType(signOnType);
    }

    public async register(e: Event) {
        e.preventDefault();

        if (!this.form) {
            return;
        }
        
        this.clearErrorMessages();
        const formData = new FormData(this.form)
        try {
            const responseData = await SocialApi.register(formData);
            if (responseData && responseData.username == formData.get("username") && responseData.display_name == formData.get("display_name")) {
                window.location.replace("/login/");
            }
        } catch (e) {
            this.pushErrorMessages(e as string[]);
        }
    }

    public async login(e: Event) {
        e.preventDefault();

        if (!this.form) {
            return;
        }
        
        this.clearErrorMessages();
        const formData = new FormData(this.form)
        try {
            const responseData = await SocialApi.login(formData);
            if (responseData && responseData.message == "Login Success") {
                window.location.replace("/");
            }
        } catch (e) {
            this.pushErrorMessages([e as string]);
        }
    }

    public async logout(e: Event) {
        e.preventDefault();
    
        try {
            const responseData = await SocialApi.logout();
            if (responseData && responseData.message == "Successfully Logged out") {
                window.location.replace("/");
            }
        } catch (e) {
            console.warn(e);
        }
    }

    private clearErrorMessages() {
        this.errorMessages.splice(0, this.errorMessages.length);
    }

    private pushErrorMessages(messages: string[]) {
        this.errorMessages?.push(...messages);
    }

    private parseSignOnType(signOnType: string | null): SignOnType {
        switch (signOnType) {
            case "register":
                return SignOnType.Register;
            case "login":
                return SignOnType.Login;
            case "logout":
                return SignOnType.Logout
            default:
                return SignOnType.Register;
        }
    }
}