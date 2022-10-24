import { html } from "@microsoft/fast-element";
import {ViewPost} from "./ViewPost";


export const ViewPostPageTemplate = html<ViewPost>`
    <div class="post-container">
        <div class="post-container1">
            <img
                    src="https://play.teleporthq.io/static/svg/default-img.svg"
                    alt="image"
                    class="post-image"
            />
            <div class="post-container2">
                <span class="post-text">Text</span>
                <div class="post-container3">
                    <span>Zebra Zigby | 2022-10-13</span>
                </div>
            </div>
        </div>
        <ul class="post-ul list">
            <li class="post-li list-item">
                <div class="post-container4">
                    <span class="post-text2">Text:</span>
                    <span class="post-text3">Text</span>
                    <img
                            alt="image"
                            src="https://play.teleporthq.io/static/svg/default-img.svg"
                            class="post-image1"
                    />
                </div>
                <div class="post-container5">
                    <span class="post-text4">Text:</span>
                    <span class="post-text5">Text</span>
                    <img
                            alt="image"
                            src="https://play.teleporthq.io/static/svg/default-img.svg"
                            class="post-image2"
                    />
                </div>
                <div class="post-container6">
                    <span class="post-text6">Text:</span>
                    <span class="post-text7">Text</span>
                    <img
                            alt="image"
                            src="https://play.teleporthq.io/static/svg/default-img.svg"
                            class="post-image3"
                    />
                </div>
            </li>
        </ul>
    </div>
`;
