import { accentForegroundRest, typeRampPlus1FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

export const FollowerStyles = css`
    h3 {
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        margin: 10px 0;
    }

    h3 a {
        display: flex;
        place-content: center;
        align-items: center;
        justify-content: space-evenly;
    }
    
    h3 a img {
        margin-right: 10px;
    }

    .follower {
        background-color: white;
        border-radius: 20px;
        margin: 16px 0px;
        filter: drop-shadow(0 8px 8px rgba(0, 0, 0, 0.25));
        padding: 8px;
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .follower.${LayoutStyleClass.Desktop} {
        justify-content: space-between;
        align-items: center;
        flex-direction: row;
    }

    .follow-decision {
        display: flex;
        align-items: center;
        flex-direction: column;
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

    .profile-image {
        margin-top: 5px;
        margin-bottom: 5px;
        width: 50px;
        height: 50px;
        object-fit: cover;
        object-position: 50%;
        background-color: lightgrey;
        border: solid lightgrey 3px;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;
