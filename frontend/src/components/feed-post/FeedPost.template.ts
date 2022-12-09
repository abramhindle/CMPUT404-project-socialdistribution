import { html, when } from "@microsoft/fast-element";
import { ContentType } from "../../libs/api-service/SocialApiModel";
import { authorInfo } from "../author-info";
import { FeedPost } from "./FeedPost";

authorInfo;

export const FeedPostTemplate = html<FeedPost>`
    <article class="post">
        <a href="${x => x.getPostUrl()}"><h2>${x => x.post?.title}</h2></a>
        <author-info
            :authorId=${x => x.post?.author?.id}
            :author=${x => x.post?.author}
            :published=${x => x.post?.published}
        ></author-info>
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