import { html, when } from "@microsoft/fast-element";
import { Profile } from "./Profile";

export const ProfilePageTemplate = html<Profile>`
    ${when(x => x.profile, html<Profile>`
        <div class="profile-background"></div>
        <img class="profile-image" src="${x => x.profile?.profileImage}"/>
        ${when(x => x.user?.id == x.profile?.id, html<Profile>`
            <button @click=${(x, c) => x.openEditModal()}>
                Edit
            </button>
        `)}
        ${when(x => x.user?.id != x.profile?.id, html<Profile>`
            <button @click=${(x, c) => x.followRequest()}>
                ${x => x.getFollowStatus()}
            </button>
        `)}
        <h2>${x => x.profile?.displayName}</h1>
    `)}
`;