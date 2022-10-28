import { accentForegroundRest, typeRampPlus1FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const FollowerStyles = css`
    .follower {
        background-color: white;
        border-radius: 20px;
        margin: 16px 0px;
        filter: drop-shadow(0 8px 8px rgba(0, 0, 0, 0.25));
        padding: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    button {
        border-radius: 20px;
        padding: 8px 20px;
        margin-bottom: 4px;
        font-size: ${typeRampPlus1FontSize};
        border: 0;
        cursor: pointer;
    }

    button.accept, button.follow-request.true {
        background-color: ${accentForegroundRest};
        color: white;
    }

    button.decline, button.follow-request.false {
        background-color: white;
        border: 2px solid lightgrey;
        color: black;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;