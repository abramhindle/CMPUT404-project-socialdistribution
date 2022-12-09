import { accentColor, accentFillRest, accentForegroundActive, neutralColor, neutralLayer2, typeRampPlus1FontSize, typeRampPlus1LineHeight, typeRampPlus2FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { LayoutStyleClass } from "../../libs/core/PageModel";

export const ProfilePageStyles = css`
    .profile-background {
        height: 17.5vh;
        width: 56.25%;
        position: absolute;
        background: linear-gradient(to bottom right, ${neutralColor}, ${accentColor});
        z-index: 0;
        border-top-left-radius: 20px;
    }

    .profile-background.${LayoutStyleClass.Mobile} {
        width: 100%;
        border-radius: 0;
    }

    .profile-info {
        z-index: 1;
        padding-top: 7.5vh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        align-content: center;
    }

    .profile-info-display {
        margin-top: 20px;
        margin-bottom: 20px;
        color: black;
    }

    .profile-info-display h2, h4 {
        margin: 0;
        color: black;
    }

    .profile-info-icon {
        display: inline-block;
        height: 15px;
        width: 15px;
    }
    
    .profile-link-text {
        color: ${accentForegroundActive};
    }
    
    .profile-image {
        margin-top: 10px;
        margin-bottom: 10px;
        width: 150px;
        height: 150px;
        object-fit: cover;
        object-position: 50%;
        background-color: lightgrey;
        border: solid lightgrey 3px;
    }

    .display-name {
        display: flex;
        width: 90%;
        justify-content: space-between;
        align-items: center;
    }

    .display-name button, .user-buttons a {
        border-radius: 50px;
        font-size: ${typeRampPlus1FontSize};
        padding: 0 16px;
        height: 5vh;
        background-color: ${accentForegroundActive};
        color: white;
        border: 0;
        font-weight: bold;

        display: flex;
        place-content: center;
        align-items: center;
        cursor: pointer;
    }

    .display-name button.true {
        background-color: ${accentForegroundActive};
        color: white;
    }

    .display-name button.false {
        background-color: white;
        border: 2px solid lightgrey;
        color: black;
    }

    .user-buttons {
        display: flex;
        width: 90%;
        justify-content: space-between;
        align-items: center;
        color: white;
    }

    .followers {
        margin-left: auto;
    }

    #edit-profile {
        position: fixed;
        z-index: 5;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto; 
        background-color: rgba(0, 0, 0, 0.4);
    }

    .modal-content {
        background-color: white;
        margin: 15% auto;
        padding: 20px;
        border-radius: 20px;
        width: 70%;
        linear-gradient(to bottom right, ${neutralLayer2}, ${accentFillRest});
    }

    .edit-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: ${typeRampPlus2FontSize};
        font-weight: bold;
    }

    .edit-header button {
        border-radius: 50px;
        padding: 8px 20px;
        border: 0;
        background-color: black;
        color: white;
        font-size: ${typeRampPlus1FontSize};
        cursor: pointer;
    }

    fast-text-field {
        width: 100%;
        margin-bottom: 12px;
    }

    .form-element {
        display: flex;
        flex-direction: column;
        place-content: center;
        align-items: flex-start;
    }

    .image-upload {
        font-size: ${typeRampPlus1FontSize};
    }

    .modal-open {
        display: block;
    }

    .modal-close {
        display: none;
    }

    .post-container {
        width: 90%;
    }

    .loading {
        height: 100px;
    }

    a, a:hover, a:visited, a:active {
        text-decoration: none;
        color: inherit;
    }
`;