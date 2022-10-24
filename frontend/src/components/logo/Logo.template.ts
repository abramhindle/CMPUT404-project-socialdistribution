import { html, when } from "@microsoft/fast-element";
import { LayoutType } from "../../libs/core/PageModel";
import { Logo } from "./Logo";

const siteName = "14Degrees";
LayoutType

export const LogoTemplate = html<Logo>`
    <span class="logo-container ${x => x.layoutStyleClass}">
        <img src="${x => x.logoUrl}"/>
        ${when(x => x.layoutType == LayoutType.Desktop, html`
            ${siteName}
        `)}
    </span>
`;