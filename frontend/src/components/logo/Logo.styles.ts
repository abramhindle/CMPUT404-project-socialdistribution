import { bodyFont, neutralColor } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

export const LogoStyles = css`
    .logo-container {
        display: flex;
        align-content: center;
        justify-content: center;
        align-items: center;
        font-family: ${bodyFont};
        width: 100%;
        height: 60px;
        background-color: ${neutralColor};
        color: white;
        border-radius: 20px;
        font-size: 24px;
    }

    img {
        width: 45px;
    }

    .${LayoutStyleClass.Desktop} img {
        margin-right: 20px;
    }
`;