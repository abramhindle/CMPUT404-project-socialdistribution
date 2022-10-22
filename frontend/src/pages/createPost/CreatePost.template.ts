import { html } from "@microsoft/fast-element";
import { CreatePost } from './CreatePost';


export const CreatePostPageTemplate = html<CreatePost>`
    <div class="create-post-container">
        <div class="create-post-banner">
            <h1 class="create-post-text">Create A Post</h1>
        </div>
        <div class="create-post-container1">
            <input
                    type="text"
                    required=""
                    autofocus=""
                    placeholder="Title"
                    class="create-post-textinput input"
            />
            <textarea
                    placeholder="Content"
                    class="create-post-textarea textarea"
            ></textarea>
            <button class="create-post-button button">
            <span class="create-post-text1">
              <span class="create-post-text2">Upload Image</span>
              <br/>
            </span>
            </button>
            <div class="create-post-container2">
                <span class="create-post-text4">Visibility:</span>
                <select class="create-post-select">
                    <option value="Public">Public</option>
                    <option value="Private">Private</option>
                    <option value="Friends Only">Friends Only</option>
                </select>
            </div>
            <button class="create-post-button1 button">
            <span class="create-post-text5">
              <span class="create-post-text6">Create</span>
              <br/>
            </span>
            </button>
        </div>
    </div>
`;
