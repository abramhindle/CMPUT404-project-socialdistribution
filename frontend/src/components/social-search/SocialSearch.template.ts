import { icon } from "@fortawesome/fontawesome-svg-core";
import { html, ref, repeat } from "@microsoft/fast-element";
import { Author } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { LayoutType } from "../../libs/core/PageModel";
import { followerComponent } from "../follower-component";
import { SocialSearch } from "./SocialSearch";

followerComponent;


export const SocialSearchTemplate = html<SocialSearch>`
    <div class="search-container">
        <div class="search-icon" :innerHTML="${_ => icon({prefix: "fas", iconName: "search"}).html}"></div>
        <input ${ref('searchInput')} type="text" placeholder="Search..">
        </input>
    </div>
    <div class="results-container">
        ${repeat(x => x.searchResults, html<Author>`
        <follower-component
            :profile=${x => x}
            :user=${(x, c) => c.parent.user}
            :layoutStyleClass=${_ => LayoutHelpers.getLayoutStyle(LayoutType.Tablet)}>
        </follower-component>
        `)}
    </div>
`;