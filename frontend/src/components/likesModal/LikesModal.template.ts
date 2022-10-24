import { html } from "@microsoft/fast-element";
import { LikesModal } from "./LikesModal";


export const LikesModalTemplate = html<LikesModal>`
    <div>
        <div class="likes-container">
            <div class="likes-banner">
                <h1 class="likes-text"><span>Likes</span></h1>
            </div>
            <ul class="likes-ul list">
                <li class="likes-li list-item">
                    <div class="likes-container1">
                        <span class="likes-text1"><span>Username</span></span>
                        <img
                                alt="image"
                                src="https://play.teleporthq.io/static/svg/default-img.svg"
                                class="likes-image"
                        />
                    </div>
                    <div class="likes-container2">
                        <span class="likes-text2"><span>Username</span></span>
                        <img
                                alt="image"
                                src="https://play.teleporthq.io/static/svg/default-img.svg"
                                class="likes-image1"
                        />
                    </div>
                    <div class="likes-container3">
                        <span class="likes-text3"><span>Username</span></span>
                        <img
                                alt="image"
                                src="https://play.teleporthq.io/static/svg/default-img.svg"
                                class="likes-image2"
                        />
                    </div>
                </li>
            </ul>
        </div>
    </div>
`;
