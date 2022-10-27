import { bodyFont, neutralLayer2, neutralLayer3, neutralStrokeRest, typeRampPlus1LineHeight } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

export const HomePageStyles = css`
    :host {
        display: flex;
        justify-content: flex-end;
        background-color: ${neutralLayer3};
        max-height: 100%;
        min-height: 100vh;
        width: 100%;
        font-family: ${bodyFont}
    }

    .loading {
        height: 100px;
    }

    .feed-container {
        width: 78.125%;
        max-height: 100%;
        min-height: 100vh;
        border-radius: 16px 0px 0px 0px;
        background-color: ${neutralLayer2};
        display: flex;
    }

    .feed-container.${LayoutStyleClass.Mobile} {
        width: 100%;
        border-radius: 0;
        background-color: ${neutralLayer2}
    }

    .main-feed {
        padding-top: 24px;
        width: 72%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        align-content: center;
    }

    .main-feed.${LayoutStyleClass.Mobile} {
        width: 100%;
    }
    
    social-search {
        height: 5vh;
        width: 90%;
        margin-bottom: 16px;
    }

    .tab-container {
        display: flex;
        justify-content: space-evenly;
        width: 90%;
        align-items: center;
        align-content: center;
    }

    button {
        cursor: pointer;
    }

    .tab {
        font-size: ${typeRampPlus1LineHeight}
        cursor: pointer;
        padding: 8px 12px;
        border-radius: 16px;
        border: 0;
        background-color: transparent;
    }

    .tab.tab-active {
        background-color: rgb(177, 167, 191);
    }

    .psa-feed {
        width: 28%;
    }

    .psa-feed.${LayoutStyleClass.Mobile} {
        display: none;
    }

    .post-container {
        width: 90%;
    }
`;