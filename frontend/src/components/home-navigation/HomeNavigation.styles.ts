import { neutralColor, typeRampPlus1FontSize, typeRampPlus2FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

export const HomeNavigationStyles = css`
    :host {
        width: 21.875%;
        height: 100%;
        z-index: 3;
        position: fixed;
        left: 0px;
    }

    :host(.${LayoutStyleClass.Mobile}) {
        width: 0;
        height: 0;
    }

    .navigation-container {
        display: flex;
        place-content: center flex-start;
        align-items: center;
        flex-direction: column;
        padding: 2vh 0px;
        height: 96vh;
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
        color: black;
        display: flex;
        align-items: center;
        font-size: 28px;
        width: 25%;
        font-weight: lighter;
        justify-content: center;
        padding: 8px 0;
        margin: 16px 0;
    }

    .navigation-item.${LayoutStyleClass.Tablet} {
        width: 100%;
    }

    .navigation-item.${LayoutStyleClass.Desktop} {
        justify-content: flex-start;
        width: 100%;
    }

    .navigation-item.${LayoutStyleClass.Mobile} .nav-icon{
        height: 30px;
        width: 30px;
    }

    .navigation-item.${LayoutStyleClass.Mobile} .profile-nav-icon{
        height: 30px;
        width: 22px;
    }

    .navigation-item.${LayoutStyleClass.Tablet} .nav-icon{
        height: 50px;
        width: 50px;
    }

    .navigation-item.${LayoutStyleClass.Desktop} .nav-icon{
        height: 50px;
        width: 50px;
        margin-right: 16px;
    }

    .profile {
        font-size: ${typeRampPlus2FontSize};
        background-color: white;
        border-radius: 50px;
        padding: 12px 20px;
        margin-top: auto;
        color: black;
    }

    .profile:hover {
        color: lightgrey;
    }
    
    .call-to-action {
        background-color: white;
        border-radius: 20px;
        font-size: ${typeRampPlus2FontSize};
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        align-content: center;
        padding: 12px;
        margin-top: auto;
        text-align: center;
        max-width: 70%;
    }

    .call-to-action.${LayoutStyleClass.Mobile} {
        flex-direction: row;
        place-content: center;
        padding: 0;
        margin: 0;
    }
    
    .action-title {
        margin-bottom: 8px;
    }

    .${LayoutStyleClass.Mobile} .action-title {
        margin: 0;
    }

    .action-button {
        width: 90%;
        border-radius: 20px;
        padding: 4px;
        margin-bottom: 4px;
    }

    .${LayoutStyleClass.Mobile} .action-button {
        margin: 0 8px;
    }

    .login {
        border: 2px solid ${neutralColor};
        color: ${neutralColor};
    }

    .register {
        background-color: ${neutralColor};
        color: white;
    }

    a, a:hover, a:visited, a:active {
        text-decoration: none;
    }
`;