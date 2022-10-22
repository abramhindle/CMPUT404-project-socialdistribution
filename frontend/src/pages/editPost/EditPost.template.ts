import {html} from "@microsoft/fast-element";
import {EditPost} from "./EditPost";


export const EditPostPageTemplate = html<EditPost>`
    <div class="edit-post-container">
        <div class="edit-post-banner">
            <h1 class="edit-post-text">Edit A Post</h1>
        </div>
        <div class="edit-post-container1">
            <input
                    type="text"
                    required=""
                    autofocus=""
                    placeholder="Title"
                    class="edit-post-textinput input"
            />
            <textarea
                    placeholder="Content"
                    class="edit-post-textarea textarea"
            ></textarea>
            <button class="edit-post-button button">
            <span class="edit-post-text01">
              <span class="edit-post-text02">Upload Image</span>
              <br/>
            </span>
            </button>
            <div class="edit-post-container2">
                <span class="edit-post-text04">Visibility:</span>
                <select class="edit-post-select">
                    <option value="Public">Public</option>
                    <option value="Private">Private</option>
                    <option value="Friends Only">Friends Only</option>
                </select>
            </div>
            <div class="edit-post-container3">
                <button class="edit-post-button1 button">
              <span class="edit-post-text05">
                <span class="edit-post-text06">Delete</span>
                <br/>
              </span>
                </button>
                <button class="edit-post-button2 button">
              <span class="edit-post-text08">
                <span class="edit-post-text09">Done</span>
                <br/>
              </span>
                </button>
            </div>
        </div>
    </div>
`;
