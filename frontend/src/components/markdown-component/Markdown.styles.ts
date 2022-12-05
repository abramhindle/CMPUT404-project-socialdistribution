import { accentForegroundRest, neutralLayer2 } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const MarkdownStyles = css`
    :host {
        width: 100%;
    }

    .markdown-root {
        overflow: hidden;
        position: relative;
    }

    img {
        margin: 10px;
        max-width: 100%;
        object-fit: cover;
        object-position: 50%;
        background-color: darkgrey;
        border-radius: 8px;
    }

    pre {
        background-color: ${neutralLayer2};
        overflow: auto;
        border-radius: 8px;
        padding: 16px;
    }

    a, a:hover, a:visited, a:active {
        text-decoration: none;
        color: ${accentForegroundRest};
    }
`;