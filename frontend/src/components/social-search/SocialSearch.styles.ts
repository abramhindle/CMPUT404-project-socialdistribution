import { neutralFillStrongHover, typeRampPlus1FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const SocialSearchStyles = css`
    .search-container {
        background-color: ${neutralFillStrongHover};
        border-radius: 20px;
        color: white;
        width: 100%;
        display: flex;
        place-content: center;
        align-items: center;
        text-align: center;
        z-index: 0;
    }

    .results-container {
        margin-top: -50px;
        padding-top: 50px;
        width: 100%;
        background-color: ${neutralFillStrongHover};
        display: flex;
        flex-direction: column;
        place-content: center;
        align-items: center;
        text-align: center;
        border-radius: 20px;
        z-index: -1;
    }

    .results-container follower-component {
        width: 90%;
    }

    .search-icon {
        height: 20px;
        width: 20px;
        padding-left: 16px;
    }

    input {
        width: 100%;
        height: 100%;
        background: none;
        border: none;
        color: white;
        padding: 16px;
        font-size: ${typeRampPlus1FontSize};
    }

    input:focus {
        outline: none;
    }

    input::placeholder {
        color: white;
        font-size: ${typeRampPlus1FontSize};
    }
`;