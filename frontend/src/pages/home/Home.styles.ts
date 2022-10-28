import { neutralColor, neutralStrokeActive, typeRampPlus1FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const HomePageStyles = css`
    .loading {
        height: 100px;
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

    .post-container {
        width: 90%;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;