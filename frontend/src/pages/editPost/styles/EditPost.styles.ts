import {css} from "@microsoft/fast-element";
import {ResetStyles} from "./reset.styles";
import {DefaultStyles} from "./default.styles";
import {GeneralStyles} from "./general.styles";


export const EditPostPageStyles = css`
  ${ResetStyles}
  ${DefaultStyles}
  ${GeneralStyles}

  .edit-post-container {
    width: 100%;
    display: flex;
    overflow: auto;
    min-height: 100vh;
    align-items: center;
    flex-direction: column;
  }
  .edit-post-banner {
    width: 100%;
    height: 100%;
    display: flex;
    padding: var(--dl-space-space-threeunits);
    align-self: center;
    align-items: center;
    flex-direction: column;
    justify-content: space-between;
    background-image: linear-gradient(93.58deg, #9F83C7 0%, #ABD9FF 100%);;
  }
  .edit-post-text {
    color: #277bc0;
    font-size: 3rem;
    text-align: center;
  }
  .edit-post-container1 {
    width: 60%;
    height: auto;
    display: flex;
    align-items: flex-end;
    flex-direction: column;
    justify-content: flex-start;
  }
  .edit-post-textinput {
    width: 100%;
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    background-color: #d9d9d9;
  }
  .edit-post-textarea {
    width: 100%;
    height: 147px;
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    background-color: #d9d9d9;
  }
  .edit-post-button {
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    border-radius: var(--dl-radius-radius-radius8);
    background-color: #b4cde6;
  }
  .edit-post-text01 {
    color: #277bc0;
  }
  .edit-post-text02 {
    font-weight: 700;
  }
  .edit-post-container2 {
    width: 50%;
    height: 35px;
    display: flex;
    position: relative;
    align-self: center;
    margin-top: var(--dl-space-space-threeunits);
    align-items: center;
    margin-right: var(--dl-space-space-twounits);
    justify-content: flex-start;
  }
  .edit-post-text04 {
    flex: 1;
    align-self: center;
    text-align: right;
    font-weight: 700;
    padding-right: var(--dl-space-space-oneandhalfunits);
  }
  .edit-post-select {
    flex: 1;
    width: 50%;
    height: 24px;
    align-self: center;
  }
  .edit-post-container3 {
    gap: 30%;
    flex: 0 0 auto;
    width: 100%;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .edit-post-button1 {
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    border-radius: var(--dl-radius-radius-radius8);
    background-color: #b4cde6;
  }
  .edit-post-text05 {
    color: #277bc0;
  }
  .edit-post-text06 {
    font-weight: 700;
  }
  .edit-post-button2 {
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    border-radius: var(--dl-radius-radius-radius8);
    background-color: #b4cde6;
  }
  .edit-post-text08 {
    color: #277bc0;
  }
  .edit-post-text09 {
    font-weight: 700;
  }
  @media(max-width: 991px) {
    .edit-post-text {
      color: rgb(39, 123, 192);
    }
    .edit-post-container3 {
      gap: 30%;
      height: 100%;
      align-items: center;
      justify-content: center;
    }
    .edit-post-text05 {
      color: rgb(39, 123, 192);
    }
    .edit-post-text06 {
      font-weight: 700;
    }
    .edit-post-text08 {
      color: rgb(39, 123, 192);
    }
    .edit-post-text09 {
      font-weight: 700;
    }
  }
  @media(max-width: 767px) {
    .edit-post-banner {
      padding-left: var(--dl-space-space-twounits);
      padding-right: var(--dl-space-space-twounits);
    }
    .edit-post-container3 {
      gap: 30%;
    }
  }
  @media(max-width: 479px) {
    .edit-post-banner {
      padding-top: var(--dl-space-space-twounits);
      padding-left: var(--dl-space-space-unit);
      padding-right: var(--dl-space-space-unit);
      padding-bottom: var(--dl-space-space-twounits);
    }
  }
`;
