import {css} from "@microsoft/fast-element";
import {ResetStyles} from "./reset.styles";
import {DefaultStyles} from "./default.styles";
import {GeneralStyles} from "./general.styles";


export const CommentModalComponentStyles = css`
  ${ResetStyles}
  ${DefaultStyles}
  ${GeneralStyles}

  .comment-container {
    width: 100%;
    height: 400px;
    display: flex;
    position: relative;
    align-items: flex-start;
    flex-direction: column;
    background-color: var(--dl-color-gray-white);
  }
  .comment-banner {
    width: 100%;
    display: flex;
    padding: var(--dl-space-space-threeunits);
    align-items: center;
    flex-direction: column;
    justify-content: space-between;
    background-image: linear-gradient(93.58deg, #9F83C7 0%, #ABD9FF 100%);;
  }
  .comment-text {
    color: rgb(39, 123, 192);
    font-size: 3rem;
    text-align: center;
  }
  .comment-textarea {
    width: 80%;
    height: 80%;
    padding: var(--dl-space-space-halfunit);
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    padding-top: 0px;
    border-width: 0px;
    padding-left: 0px;
    padding-right: 0px;
    padding-bottom: 0px;
    background-color: #d9d9d9;
  }
  .comment-button {
    color: #277bc0;
    align-self: center;
    font-style: normal;
    margin-top: var(--dl-space-space-unit);
    font-weight: 700;
    border-width: 0px;
    border-radius: var(--dl-radius-radius-radius8);
    margin-bottom: var(--dl-space-space-unit);
    text-transform: capitalize;
    background-color: #b4cde6;
  }
  @media(max-width: 991px) {
    .comment-textarea {
      width: 80%;
      height: 80%;
    }
  }
  @media(max-width: 767px) {
    .comment-banner {
      padding-left: var(--dl-space-space-twounits);
      padding-right: var(--dl-space-space-twounits);
    }
    .comment-textarea {
      width: 80%;
      height: 50%;
    }
  }
  @media(max-width: 479px) {
    .comment-banner {
      padding-top: var(--dl-space-space-twounits);
      padding-left: var(--dl-space-space-unit);
      padding-right: var(--dl-space-space-unit);
      padding-bottom: var(--dl-space-space-twounits);
    }
  }
`;
