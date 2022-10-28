import { bodyFont, neutralColor, neutralLayer2, neutralLayer3, neutralStrokeActive, typeRampPlus1FontSize } from "@microsoft/fast-components";
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

    .tab {
        font-size: ${typeRampPlus1FontSize};
        cursor: pointer;
        padding: 8px 12px;
        border-radius: 16px;
        border: 0;
        background-color: transparent;
        margin-right: 16px;
    }

    .tab.tab-active {
        background-color: rgb(177, 167, 191);
    }

    .create-a-post {
        margin-left: auto;
        background-color: ${neutralColor};
        border-radius: 16px;
        padding: 8px 50px; 
        color: white;
        display: flex;
        justify-content: center;
        align-content: center;
        align-items: center;
    }

    .create-a-post:hover {
        background-color: ${neutralStrokeActive};
        color: white;
    }

    .create-post-icon {
        width: 20px;
        height: 20px;
        margin-right: 16px;
    }

    .psa-feed {
        width: 28%;
    }

    .psa-feed.${LayoutStyleClass.Mobile} {
        display: none;
    }

    .psa-post-container {
        display: flex;
        place-content: center;
        align-items: center;
        padding-top: 16px;
        width: 90%;
        margin: auto;
    }

    .psa-header {
        font-size: ${typeRampPlus1FontSize};
        background-color: white;
        border-radius: 20px 20px 0 0;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.25));
        padding: 8px;
        text-align: center;
    }

    .post-container {
        width: 90%;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;