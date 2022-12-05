import { typeRampPlus2FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

LayoutStyleClass

export const FeedPostStyles = css`
    .post {
        background-color: white;
        border-radius: 20px;
        margin: 16px 0px;
        filter: drop-shadow(0 8px 8px rgba(0, 0, 0, 0.25));
        padding: 8px;
    }

    .post h4 {
        display: flex;
        align-items: center;
    }

    .post h4 a{
        margin-right: 5px;
    }

    .profile-image {
        margin: 10px 10px 10px 0;
        width: 30px;
        height: 30px;
        object-fit: cover;
        object-position: 50%;
        background-color: lightgrey;
        border: solid lightgrey 2px;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;