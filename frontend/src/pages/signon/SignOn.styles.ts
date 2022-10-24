import { accentColor, bodyFont, controlCornerRadius, neutralColor, neutralFillStrongHover, typeRampPlus2FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";

export const SignOnPageStyles = css`
    :host {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100vw;
        background: linear-gradient(to bottom right, ${neutralColor}, ${accentColor});
        font-family: ${bodyFont};
    }

    h1 {
        font-weight: lighter;
        text-align: center;
        color: white;
        margin-bottom: 60px;
    }

    site-logo {
        width: 70%;
        margin-bottom: 12px;
    }

    .form-container {
        width: 26%;
        height: 65%;
        border-radius: 20px;
        background-color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-content: center;
        align-items: center;
        padding: 16px 0px;
    }

    #register-form, #login-form {
        width: 90%;
    }

    fast-text-field {
        width: 100%;
        margin-bottom: 12px;
    }

    .form-element {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-content: center;
        align-items: center;
    }

    button {
        width: 100%;
        height: 60px;
        border-radius: calc(${controlCornerRadius} * 1px);
        font-size: ${typeRampPlus2FontSize};
        cursor: pointer;
    }

    .form-element button {
        border: 0;
        color: white;
        background: linear-gradient(to right, ${neutralFillStrongHover} , ${neutralColor});
    }

    .form-element button:hover {
        background: ${neutralColor}
    }

    .logout {
        color: ${neutralColor};
        background-color: white;
        border: 1px solid ${neutralColor};
        margin-bottom: 12px;
    }

    .cancel {
        border: 0;
        color: white;
        background-color: ${neutralColor};
    }
`;