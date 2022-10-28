import { Page } from "../Page";
import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";

export class Profile extends Page {

    @observable
    public getID(){
        const info = window.location.search
        const urlP = new URLSearchParams(info)
        const id = urlP.get("userID")
        console.log(id)
    }
    
    public  getInfo(){
        const id = this.getID()
        var name = ""
        try {
            const responseData =  SocialApi.fetchAuthor("1")
            responseData.then(
                (data) =>  {
                    const name = data?.displayName
                    console.log( name)
                    return name?.toString
                }
            )
            
        } catch (e) {
            console.warn(e);
        }
    
    }


}