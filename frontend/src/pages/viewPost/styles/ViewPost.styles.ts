import {css} from "@microsoft/fast-element";
import {ResetStyles} from "./reset.styles";
import {DefaultStyles} from "./default.styles";
import {GeneralStyles} from "./general.styles";
import { accentForegroundActive, typeRampPlus1FontSize } from "@microsoft/fast-components";


export const ViewPostPageStyles = css`
  ${ResetStyles}
  ${DefaultStyles}
  ${GeneralStyles}
  
  .post-container {
    width: 100%;
    display: flex;
    overflow: auto;
    min-height: 100vh;
    align-items: center;
    flex-direction: column;
    background-color: white;
  }

  .post-container1 {
    flex: 0 0 auto;
    width: 80%;
    height: 100px;
    display: flex;
    margin-top: var(--dl-space-space-twounits);
    align-items: center;
    padding-top: var(--dl-space-space-halfunit);
    padding-left: var(--dl-space-space-halfunit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-twounits);
    padding-right: var(--dl-space-space-halfunit);
    padding-bottom: var(--dl-space-space-halfunit);
    justify-content: flex-start;
    background-color: #d9d9d9;
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-image {
    flex: 1 1 0;
    max-width: 100px;
    object-fit: cover;
    margin-right: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-container2 {
    flex: 3 1 0;
    width: 930px;
    height: 100%;
    display: flex;
    position: relative;
    align-items: flex-start;
    flex-direction: column;
    justify-content: flex-start;
  }

  .post-text {
    margin-top: var(--dl-space-space-halfunit);
  }

  .post-container3 {
    flex: 0 0 auto;
    right: 0px;
    width: 50%;
    bottom: 0px;
    height: 30%;
    display: flex;
    position: absolute;
    align-items: center;
    justify-content: flex-end;
  }
  
  .like-post-icon {
    width: 20px;
    height: 20px;
    margin-left: 10px;
  }

  .post-ul {
    width: 80%;
    height: 80%;
    overflow: auto;
    align-self: center;
    padding-left: 0px;
    border-radius: var(--dl-radius-radius-radius4);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-li {
    border-radius: var(--dl-radius-radius-radius4);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .comment-container {
    gap: var(--dl-space-space-unit);
    flex: 0 0 auto;
    width: 100%;
    height: auto;
    display: flex;
    position: relative;
    align-items: flex-start;
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-unit);
    padding-right: 0px;
    justify-content: flex-start;
    background-color: #d9d9d9;
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .comment-display-name {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .comment-content {
    margin-top: var(--dl-space-space-halfunit);
    margin-right: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .comment-profile-icon {
    top: 0px;
    right: 0px;
    width: auto;
    height: 100%;
    position: absolute;
    object-fit: cover;
    border-radius: var(--dl-radius-radius-radius4);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .edit-post-button {
    border-radius: 50px;
    font-size: ${typeRampPlus1FontSize};
    padding: 0 16px;
    height: 5vh;
    font-weight: bold;

    display: flex;
    place-content: center;
    align-items: center;
    cursor: pointer;

    background-color: white;
    border: 2px solid lightgrey;
    color: black;

    width: 90%;
  }

  @media (max-width: 991px) {
    .post-container4 {
      position: relative;
    }

    .post-image1 {
      top: 0px;
      right: 0px;
      width: auto;
      height: 100%;
      position: absolute;
    }

    .post-container5 {
      position: relative;
    }

    .post-image2 {
      top: 0px;
      right: 0px;
      width: auto;
      height: 100%;
      position: absolute;
    }

    .post-container6 {
      position: relative;
    }

    .post-image3 {
      top: 0px;
      right: 0px;
      width: auto;
      height: 100%;
      position: absolute;
    }
  }
`;
