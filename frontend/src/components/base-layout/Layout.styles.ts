import { bodyFont, neutralLayer2, neutralLayer3, typeRampPlus1FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

export const LayoutStyles = css`
    :host {
        display: flex;
        justify-content: flex-end;
        background-color: ${neutralLayer3};
        max-height: 100%;
        min-height: 100vh;
        width: 100%;
        font-family: ${bodyFont}
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
        width: 90%;
        margin-top: 16px;
    }

    .psa-feed {
        width: 21.875%;
        display: flex;
        flex-direction: column;
        align-items: center;
        place-content: flex-start;
        position: fixed;
        right: 0;
    }

    .psa-feed.${LayoutStyleClass.Mobile} {
        display: none;
    }

    .psa-post-container {
        display: flex;
        place-content: center;
        align-items: center;
        width: 90%;
        margin-top: 16px;
        flex-direction: column;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.25));
    }

    .psa-header {
        font-size: ${typeRampPlus1FontSize};
        background-color: white;
        border-radius: 20px 20px 0 0;
        width: 90%;
        padding: 5%;
        text-align: center;
        border-bottom: 2px solid lightgrey;
    }

    .psa-post {
        background-color: white;
        border-radius: 0 0 20px 20px;
        width: 90%;
        padding: 5%;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;