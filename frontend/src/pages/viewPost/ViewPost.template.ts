import { html, repeat } from "@microsoft/fast-element";
import {ViewPost} from "./ViewPost";


export const ViewPostPageTemplate = html<ViewPost>`
    <div class="post-container">
        <div class="post-container1">
            <img
                    src="${x => x.post_image_url}"
                    alt="post image"
                    class="post-image"
            />
            <div class="post-container2">
                <span class="post-text">${x => x.post_text}</span>
                <div class="post-container3">
                    <span>${x => x.post_author} | ${x => x.post_edit_date}</span>
                </div>
            </div>
        </div>
        <ul class="post-ul list">
            <li class="post-li list-item">
                ${repeat(x => x.comments, html<string>`
                    <div class="comment-container">
                        <span class="comment-display-name">${x.display_name}</span>
                        <span class="comment-content">${x.content}</span>
                        <img
                                alt="image"
                                src="https://play.teleporthq.io/static/svg/default-img.svg"
                                class="comment-profile-icon"
                        />
                    </div>
                `)}
            </li>
        </ul>
    </div>
`;
