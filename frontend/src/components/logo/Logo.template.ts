import { html } from "@microsoft/fast-element";
import { Logo } from "./Logo";

const siteName = "14Degrees";

export const LogoTemplate = html<Logo>`
    <img src="${x => x.logoUrl}"/>
    ${siteName}
`;