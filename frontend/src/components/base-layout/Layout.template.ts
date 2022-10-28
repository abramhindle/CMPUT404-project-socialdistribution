import { labToXYZ } from "@microsoft/fast-colors";
import { html } from "@microsoft/fast-element";
import { homeNavigation } from "../home-navigation";
import { socialSearch } from "../social-search";
import { Layout } from "./Layout";

socialSearch;
homeNavigation;

const navigationTemplate = html<Layout>`
    <home-navigation
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => x.layoutStyleClass}"
        :className="${x => x.layoutStyleClass}">
    </home-navigation>
`;

export const LayoutTemplate = html<Layout>`
    ${navigationTemplate}
    <main class="feed-container ${x => x.layoutStyleClass}">
        <div class="main-feed ${x => x.layoutStyleClass}">
            <slot></slot>
        </div>
        <div class="psa-feed ${x => x.layoutStyleClass}">
            <social-search>
            </social-search>
            <div class="psa-post-container">
                <div class="psa-header">
                    Public Service Announcements 
                </div>
                <div class="psa-post">
                    Work in progress...
                </div>
            </div>
        </div>
    </main>
`;