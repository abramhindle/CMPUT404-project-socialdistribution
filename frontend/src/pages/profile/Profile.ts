import { Page } from "../Page";
import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";

export class Profile extends Page {
    @observable
    public errorMessages: string[] = [];
    public form?: HTMLFormElement;
    const id = "123"
    public async getInfo(e:Event){
        try {
            const responseData = await SocialApi.fetchAuthor(id);
            if (responseData ) {
                window.location.replace("/profile");
            }
        } catch (e) {
            console.warn(e);
        }
    }
    
    
    public async submit(e: Event) {
        e.preventDefault();

        if (!this.form) {
            return;
        }
        
        this.errorMessages.splice(0, this.errorMessages.length);
     
        // const requestOptions = {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json; charset=UTF-8" },
        //     body: JSON.stringify()
        // };
        // try {
        //     const responseData = await ;
        //     if (responseData && responseData.username == formData.get("username") && responseData.display_name == formData.get("display_name")) {
        //         window.location.replace("/profile/");
        //     }
        // } catch (e) {
        //     this.pushErrorMessages(e as string[]);
        // }
    }
    private pushErrorMessages(messages: string[]) {
        this.errorMessages?.push(...messages);
    }
}