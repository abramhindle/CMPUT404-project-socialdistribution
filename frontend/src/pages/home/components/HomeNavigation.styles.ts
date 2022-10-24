import { css } from "@microsoft/fast-element";

export const HomeNavigationStyles = css`
    :host {
        width: 21.875%;
        height: 100%;
        z-index: 3;
        position: relative;
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
    }

    .navigation-item {
        display: flex;
        align-items: center;
        font-size: 28px;
        width: 100%;
        font-weigth: 
    }

    .navigation-item img{
        height: 50px;
        width: 50px;
        margin-right: 16px;
    }
`;