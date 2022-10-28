import { html } from "@microsoft/fast-element";
import { CommentModal } from "./CommentModal";


export const CommentModalTemplate = html<CommentModal>`
    <div>
        <div class="comment-container">
            <div class="comment-banner"><h1 class="comment-text">Comment</h1></div>
            <textarea
                    placeholder="Content"
                    class="comment-textarea textarea"
            ></textarea>
            <button class="comment-button button"><span>Edit</span></button>
        </div>
    </div>
`;
