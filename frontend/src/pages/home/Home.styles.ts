import { bodyFont, neutralLayer2, neutralLayer3 } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const HomePageStyles = css`
    :host {
        display: flex;
        justify-content: flex-end;
        background-color: ${neutralLayer3};
        height: 100vh;
        width: 100vw;
        font-family: ${bodyFont}
    }

    .feed-container {
        width: 78.125%;
        height: 100%;
        border-radius: 16px 0px 0px 0px;
        background-color: ${neutralLayer2}
    }
`;