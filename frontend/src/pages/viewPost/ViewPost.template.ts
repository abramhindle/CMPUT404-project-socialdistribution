import { html, when } from "@microsoft/fast-element";
import { layoutComponent } from "../../components/base-layout";
import { ContentType } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { ViewPost } from "./ViewPost";

layoutComponent;

export const ViewPostPageTemplate = html<ViewPost>`
    <page-layout
        :userId="${x => x.userId}"
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        ${when(x => x.post, html<ViewPost>`
        <div class="post-container">
            <div class="post-container1">
                <img
                        src="https://play.teleporthq.io/static/svg/default-img.svg"
                        alt="post image"
                        class="post-image"
                />
                <div class="post-container2">
                    ${when(x => x.post?.contentType == ContentType.Markdown && import('../../components/markdown-component'), html<ViewPost>`
                        <markdown-component
                            :content=${x => x.post?.content}
                        ></markdown-component>
                    `)}
                    ${when(x => x.post?.contentType == ContentType.Plain, html<ViewPost>`
                        <span class="post-text">${x => x.post?.content}</span>
                    `)}
                    <div class="post-container3">
                        <span>${x => x.post?.author?.displayName} | ${x => new Date(x.post?.published || new Date()).toLocaleDateString()}</span>
                    </div>
                </div>
            </div>
            ${when(x => x.userId == x.profileId, html<ViewPost>`
                <a class="edit-post-button" href="/edit-post/${x => x.userId}/${x => x.post?.id}">Edit Post</a>
            `)}
        </div>
        `)}
        ${when(x => !x.post, html<ViewPost>`
            <h1>${x => x.loadedPostText}</h1>
        `)}
    </page-layout>
`;

//         <ul class="post-ul list">
//             <li class="post-li list-item">
//                 ${repeat(x => x.post?.comments || [], html<string>`
//                     <div class="comment-container">
//                         <span class="comment-display-name">${x.display_name}</span>
//                         <span class="comment-content">${x.content}</span>
//                         <img
//                                 alt="image"
//                                 src="https://play.teleporthq.io/static/svg/default-img.svg"
//                                 class="comment-profile-icon"
//                         />
//                     </div>
//                 `)}
//             </li>
//         </ul>
