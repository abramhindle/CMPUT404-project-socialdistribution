import {html, ref} from "@microsoft/fast-element";
import { layoutComponent } from "../../components/base-layout";
import { LayoutHelpers } from "../../libs/core/Helpers";
import {CreatePost} from './CreatePost';

layoutComponent;

export const CreatePostPageTemplate = html<CreatePost>`
    <page-layout
        :userId="${x => x.userId}"
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        <div class="create-post-container">
            <div class="create-post-banner">
                <h1 class="create-post-text">Create A Post</h1>
            </div>
            <form ${ref("form")} @submit="${(x, c) => x.createPost(c.event)}" class="create-post-container1">
                <input
                        type="text"
                        required=""
                        autofocus=""
                        placeholder="Title"
                        class="create-post-textinput input"
                        name="title"
                />
                <textarea
                        placeholder="Content"
                        class="create-post-textarea textarea"
                        name="content"
                ></textarea>
                <button class="create-post-button button">
                <span class="create-post-text1">
                <span class="create-post-text2">Upload Image</span>
                <br/>
                </span>
                </button>
                <div class="create-post-container2">
                    <span class="create-post-text4">Visibility:</span>
                    <select class="create-post-select" name="visibility">
                        <option value="PUBLIC">Public</option>
                        <option value="PRIVATE">Private</option>
                        <option value="FRIENDS">Friends Only</option>
                    </select>
                </div>
                <button class="create-post-button1 button">
                <span class="create-post-text5">
                <span class="create-post-text6">Create</span>
                <br/>
                </span>
                </button>
            </form>
        </div>
    </page-layout>
`;
