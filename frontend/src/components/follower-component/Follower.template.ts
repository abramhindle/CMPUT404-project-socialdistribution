import { html, when } from "@microsoft/fast-element";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { FollowStatus } from "../../libs/core/PageModel";
import { Follower } from "./Follower";

export const FollowerTemplate = html<Follower>`
    ${when(x => !x.isDeleted, html<Follower>`
        <div class="follower ${x => x.layoutStyleClass}">
            <h3><a href="${x => "/profile/" + x.profile?.id}">${x => x.profile?.displayName}</a></h3>
            ${when(x => x.user?.id != x.profile?.id, html<Follower>`
                ${when(x => x.request, html<Follower>`
                    <div class="follow-decision">
                        <button class="accept" @click=${(x, c) => x.acceptRequest()}>
                            Accept Request
                        </button>
                        <button class="decline" @click=${(x, c) => x.declineRequest()}>
                            Decline Request
                        </button>
                    </div>
                `)}
                ${when(x => !x.request, html<Follower>`
                    <button class="follow-request ${x => x.followStatus == FollowStatus.NotFollowing}" @click=${(x, c) => x.followRequest()}>
                        ${x => LayoutHelpers.parseFollowStatus(x.followStatus)}
                    </button>
                `)}
            `)}
        </div>
    `)}
`;