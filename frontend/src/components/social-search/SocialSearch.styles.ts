import { neutralFillStrongHover } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const SocialSearchStyles = css`
    .search-container {
        background-color: ${neutralFillStrongHover};
        border-radius: 20px;
        color: white;
        width: 100%;
        height: 5vh;
        display: flex;
        place-content: center;
        align-items: center;
        text-align: center;
    }

    .search-icon {
        height: 20px;
        width: 20px;
    }
`;