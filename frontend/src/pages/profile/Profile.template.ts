import { html, ref, repeat } from "@microsoft/fast-element";
import { Profile} from "./Profile";

export const ProfilePageTemplate = html<Profile>`
    <div class="whole">
        <div class="top">
            <a href="/">
                <button class="btn">Back</button>
            </a>
             <div class = "imgdiv"> 
                <img>image</img>
             </div>
        </div>
        
        <h1>${x => x.getInfo()}</h1>
        
        <form >
            <div class="form-element">
                <fast-text-field type="text" placeholder=${x => x.getInfo()} name="email" required></fast-text-field>
            </div>
            <div class="form-element">
                <fast-text-field type="text" placeholder="githubHandle" name="gh" required></fast-text-field>
            </div>
            <div class="form-element">
                <button >submit</button>
            </div>
        </form>

    </div>


`;