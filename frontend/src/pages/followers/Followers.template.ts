import { html, ref, repeat, when } from "@microsoft/fast-element";
import { followerComponent } from "../../components/follower-component";
import { Author } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { Followers } from "./Followers";

followerComponent;

export const ProfilePageTemplate = html<Followers>`
    <page-layout
        :userId="${x => x.userId}"
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        <h1>${x => x.profile?.displayName}'s Followers</h1>
        <div class="follower-container">
        ${repeat(x => x.followers, html<Author>`
            <follower-component
                :profile=${x => x}
                :user=${(x, c) => c.parent.user}>
            </follower-component>
        `)}
        </div>
    </page-layout>
`;