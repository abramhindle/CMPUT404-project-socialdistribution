import { icon } from "@fortawesome/fontawesome-svg-core";
import { html } from "@microsoft/fast-element";
import { SocialSearch } from "./SocialSearch";

export const SocialSearchTemplate = html<SocialSearch>`
    <div class="search-container">
        <div class="search-icon" :innerHTML="${_ => icon({prefix: "fas", iconName: "search"}).html}"></div>
        Universal Search Bar (WIP)
    </div>
`;