import { html, repeat } from "@microsoft/fast-element";
import {ViewPost} from "./ViewPost";


export const ViewPostPageTemplate = html<ViewPost>`
    <div class="post-container">
        <div class="post-container1">
            <img
                    src="https://play.teleporthq.io/static/svg/default-img.svg"
                    alt="post image"
                    class="post-image"
            />
            <div class="post-container2">
                <span class="post-text">${x => x.post?.content}</span>
                <div class="post-container3">
                    <span>${x => x.post?.author?.displayName} | ${x => new Date(x.post?.published || new Date()).toLocaleDateString()}</span>
                </div>
            </div>
        </div>
    </div>
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
