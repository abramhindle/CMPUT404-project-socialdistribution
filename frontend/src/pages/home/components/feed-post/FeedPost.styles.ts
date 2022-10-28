import { controlCornerRadius } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../../../libs/core/PageModel";

LayoutStyleClass

export const FeedPostStyles = css`
    .post {
        background-color: white;
        border-radius: 20px;
        margin: 16px 0px;
        filter: drop-shadow(0 8px 8px rgba(0, 0, 0, 0.25));
        padding: 8px;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;