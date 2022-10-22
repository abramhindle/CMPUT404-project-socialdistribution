import { bodyFont, neutralColor } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const LogoStyles = css`
    :host {
        display: flex;
        align-content: center;
        justify-content: center;
        align-items: center;
        font-family: ${bodyFont};
        width: 250px;
        height: 60px;
        background-color: ${neutralColor};
        color: white;
        border-radius: 20px;
        font-size: 24px;
    }

    img {
        height: 40px;
        width: 40px;
        margin-right: 24px;
    }
`;