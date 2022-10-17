import { html } from "@microsoft/fast-element";
import { Profile } from "./Profile";


export const ProfilePageTemplate = html<Profile>`
    <div>${x => x.greeting} world!</div>
`;