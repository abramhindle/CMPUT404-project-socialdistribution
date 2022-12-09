import { css } from "@microsoft/fast-element";

export const AuthorInfoStyles = css`
    h4 {
        display: flex;
        align-items: center;
        margin: 0;
    }

    h4 a{
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