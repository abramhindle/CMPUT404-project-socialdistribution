import { html, when, repeat } from "@microsoft/fast-element";
import { logoComponent } from "../../../components/logo";
import { LayoutHelpers } from "../../../libs/core/Helpers";
import { LayoutType } from "../../../libs/core/PageModel";
import { HomeNavigation, NavItem } from "./HomeNavigation";

logoComponent;

const navigationItemsTemplate = html<HomeNavigation>`
    <div class="navigation-items ${x => x.layoutStyleClass}">
    ${repeat(x => x.navigationItems, html<NavItem>`
        <a class="navigation-item ${(x, c) => c.parent.layoutStyleClass}" href="${(x, c) => c.parent.getNavigationUrl(x)}">
            <img src="${(x, c) => c.parent.getNavigationIconUrl(x)}"/>
            ${when((x, c) => c.parent.layoutType == LayoutType.Desktop, html<string>`
                ${x => x}
            `)}
        </a>
    `)}
    </div>
`

const navProfileTemplate = html<HomeNavigation>`

`;

const callToActionTemplate = html<HomeNavigation>`
`;

export const HomeNavigationTemplate = html<HomeNavigation>`
    <header class="navigation-container ${x => x.layoutStyleClass}">
        ${when(x => x.layoutType != LayoutType.Mobile, html<HomeNavigation>`
            <site-logo
                :layoutType=${x => x.layoutType}
                :layoutStyleClass=${x => LayoutHelpers.getLayoutStyle(x.layoutType)}>
            </site-logo>
        `)}
        ${when(x => x.user, html<HomeNavigation>`
            ${navigationItemsTemplate}
            ${navProfileTemplate}
        `)}
        ${when(x => !x.user, html<HomeNavigation>`
            ${callToActionTemplate}
        `)}
    </header>
`;