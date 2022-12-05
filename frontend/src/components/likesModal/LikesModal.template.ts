import {html, repeat} from "@microsoft/fast-element";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { followerComponent } from "../follower-component";
import { LikesModal } from "./LikesModal";

followerComponent;

export const LikesModalTemplate = html<LikesModal>`
    <div>
        <div class="likes-container">
            <div class="likes-banner">
                <h1 class="likes-text"><span>Likes</span></h1>
                <button class="close-modal" @click="${x => x.parent.toggleModal()}">
                    Close
                </button>
            </div>
            <ul class="likes-ul list">
                ${repeat(x => x.likes || [], html`
                    <follower-component
                        :profile=${x => x.author}
                        :user=${(x, c) => c.parent.user}
                        :layoutStyleClass="${(x, c) => LayoutHelpers.getLayoutStyle(c.parent.layoutType)}">
                    </follower-component>
                `)}
            </ul>
        </div>
    </div>
`;
