import { html, when, repeat } from "@microsoft/fast-element";
import { logoComponent } from "../../../components/logo";
import { HomeNavigation } from "./HomeNavigation";

logoComponent;

const navigationItemsTemplate = html<HomeNavigation>`
    <div class="navigation-items">
    ${repeat(x => x.navigationItems, html<string>`
        <div class="navigation-item">
            <img src="${(x, c) => c.parent.getNavigationIconUrl(x)}"/>
            ${x => x}
        </div>
    `)}
    </div>
`

const navProfileTemplate = html<HomeNavigation>`

`;

const callToActionTemplate = html<HomeNavigation>`
`;

export const HomeNavigationTemplate = html<HomeNavigation>`
    <header class="navigation-container">
    <site-logo></site-logo>
    ${when(x => x.user, html<HomeNavigation>`
        ${navigationItemsTemplate}
        ${navProfileTemplate}
    `)}
    ${when(x => !x.user, html<HomeNavigation>`
        ${callToActionTemplate}
    `)}
    </header>
`;