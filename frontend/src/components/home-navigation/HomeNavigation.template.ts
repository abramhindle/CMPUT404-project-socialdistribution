import { html, when, repeat } from "@microsoft/fast-element";
import { logoComponent } from "../logo";
import { siteName } from "../logo/Logo.template";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { LayoutType } from "../../libs/core/PageModel";
import { HomeNavigation, NavItem } from "./HomeNavigation";

logoComponent;

const navigationItemsTemplate = html<HomeNavigation>`
    <div class="navigation-items ${x => x.layoutStyleClass}">
    ${repeat(x => x.navigationItems, html<NavItem>`
        <a class="navigation-item ${(x, c) => c.parent.layoutStyleClass}" href="${(x, c) => c.parent.getNavigationUrl(x)}">
            <div class="nav-icon" :innerHTML="${(x, c) => c.parent.getNavigationIcon(x)}"></div>
            ${when((x, c) => c.parent.layoutType == LayoutType.Desktop, html<string>`
                ${x => x}
            `)}
        </a>
    `)}
    ${when(x => x.layoutType == LayoutType.Mobile, html<HomeNavigation>`
        <a href="/profile/${x => x.user?.id}" class="navigation-item ${x => x.layoutStyleClass}">
            <div class="profile-nav-icon" :innerHTML="${x => x.getNavigationIcon(NavItem.Profile)}"></div>
        </a>
    `)}
    </div>
`

const navProfileTemplate = html<HomeNavigation>`
    ${when(x => x.layoutType != LayoutType.Mobile, html<HomeNavigation>`
        <a href="/profile/${x => x.user?.id}" class="profile ${x => x.layoutStyleClass}">
            @${x => x.user?.displayName}
        </a>
    `)}
`;

const callToActionTemplate = html<HomeNavigation>`
    <div class="call-to-action ${x => x.layoutStyleClass}">
        <div class="action-title">New to ${siteName}?</div>
        <a href="/login/" class="action-button login">Log In</a>
        <a href="/register/" class="action-button register">Sign Up</a>
    </div>
`;

export const HomeNavigationTemplate = html<HomeNavigation>`
    <header class="navigation-container ${x => x.layoutStyleClass}">
        ${when(x => x.layoutType != LayoutType.Mobile, html<HomeNavigation>`
            <site-logo
                :layoutType=${x => x.layoutType}
                :layoutStyleClass=${x => LayoutHelpers.getLayoutStyle(x.layoutType)}>
            </site-logo>
        `)}
        ${when(x => x.userId, html<HomeNavigation>`
            ${navigationItemsTemplate}
            ${navProfileTemplate}
        `)}
        ${when(x => !x.userId, html<HomeNavigation>`
            ${callToActionTemplate}
        `)}
    </header>
`;
