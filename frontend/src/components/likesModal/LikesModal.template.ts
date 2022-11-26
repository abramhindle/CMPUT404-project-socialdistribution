import {html, repeat} from "@microsoft/fast-element";
import { LikesModal } from "./LikesModal";


export const LikesModalTemplate = html<LikesModal>`
    <div>
        <div class="likes-container">
            <div class="likes-banner">
                <h1 class="likes-text"><span>Likes</span></h1>
            </div>
            <ul class="likes-ul list">
                ${repeat(x => x.likes || [], html`
                    <li class="likes-li list-item">
                        <div class="likes-container">
                            <span class="likes-text"><span>${x => x.author.display_name}</span></span>
                            <img
                                    alt="image"
                                    src=${x => x.author.profile_image}
                                    class="likes-image"
                            />
                        </div>
                    </li>
                `)}
            </ul>
        </div>
        <button @click="${x => x.parent.toggleModal()}">
            Close
        </button>
    </div>
`;
