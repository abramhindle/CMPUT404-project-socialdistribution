import { html, ref, repeat } from "@microsoft/fast-element";

import { Profile } from "./Profile";


export const ProfilePageTemplate = html<Profile>`
    <div class="whole">
        <div class="top">
            <a href="/">
                <button class="btn">Back</button>
            </a>
            <img>image</img>  
        </div>
        
        <form >
            <div class="form-element">
                <fast-text-field type="text" placeholder="Zebra Zigby" name="display_name" required></fast-text-field>
            </div>
            <div class="form-element">
                <fast-text-field type="text" placeholder="Username" name="username" required></fast-text-field>
            </div>
            <div class="form-element">
                <fast-text-field type="text" placeholder="email" name="email" required></fast-text-field>
            </div>
            <div class="form-element">
                <fast-text-field type="text" placeholder="date of birth" name="db" required></fast-text-field>
            </div>
            <div class="form-element">
                <button >submit</button>
            </div>
        </form>

    </div>


`;