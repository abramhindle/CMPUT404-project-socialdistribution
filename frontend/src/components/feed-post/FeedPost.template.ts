import { html, when } from "@microsoft/fast-element";
import { ContentType } from "../../libs/api-service/SocialApiModel";
import { FeedPost } from "./FeedPost";

export const FeedPostTemplate = html<FeedPost>`
    <article class="post">
        <a href="${x => x.getPostUrl()}"><h2>${x => x.post?.title}</h2></a>
        <h4>
            ${when(x => x.post?.author?.profileImage !== "", html<FeedPost>`
                <img class="profile-image" src="${x => x.post?.author?.profileImage}">
            `)}
            <a href="${x => x.getAuthorUrl(x.post?.author?.id)}">${x => x.post?.author?.displayName + " "}</a>
            <small>${x => " | " + x.post?.published?.toLocaleDateString() || " | " + new Date().toLocaleDateString()}</small>
        </h4>
        ${when(x => x.post?.contentType == ContentType.Markdown && import('../markdown-component'), html<FeedPost>`
            <markdown-component
                :content=${x => x.post?.description + "..."}
            ></markdown-component>
        `)}
        ${when(x => x.post?.contentType == ContentType.Plain, html<FeedPost>`
            <p>${x => x.post?.description}...</p>
        `)}
    </article>
`;