import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../../libs/core/PageModel";

LayoutStyleClass

export const HomeNavigationStyles = css`
    :host {
        width: 21.875%;
        height: 100%;
        z-index: 3;
        position: relative;
    }

    :host(.${LayoutStyleClass.Mobile}) {
        width: 0;
        height: 0;
        z-index: 3;
        position: fixed;
    }

    .navigation-container {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        flex-direction: column;
        align-content: center;
        padding: 6% 0;
        height: 94%;
    }

    .navigation-container.${LayoutStyleClass.Mobile} {
        display: flex;
        place-content: center flex-start;
        flex-direction: row;
        height: 3.5rem;
        width: 100%;
        bottom: 0px;
        background-color: white;
        left: 0px;
        justify-content: center;
        position: fixed;
        padding: 0;
    }

    site-logo {
        width: 80%;
    }

    .navigation-items {
        margin-top: 16px;
        height: 40%;
        width: 73%;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
    }

    .navigation-items.${LayoutStyleClass.Mobile} {
        margin: 0;
        width: 100%;
        height: 100%;
        flex-direction: row;
    }

    .navigation-item {
        display: flex;
        align-items: center;
        font-size: 28px;
        width: 25%;
        font-weight: lighter;
        justify-content: center;
        padding: 8px 0;
    }

    .navigation-item.${LayoutStyleClass.Tablet} {
        width: 100%;
    }

    .navigation-item.${LayoutStyleClass.Desktop} {
        justify-content: flex-start;
        width: 100%;
    }

    .navigation-item.${LayoutStyleClass.Mobile} img{
        height: 30px;
        width: 30px;
    }

    .navigation-item.${LayoutStyleClass.Tablet} img{
        height: 50px;
        width: 50px;
    }

    .navigation-item.${LayoutStyleClass.Desktop} img{
        height: 50px;
        width: 50px;
        margin-right: 16px;
    }

    a, a:hover, a:visited, a:active {
        color: inherit;
        text-decoration: none;
    }
`;