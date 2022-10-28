import {css} from "@microsoft/fast-element";
import {ResetStyles} from "./reset.styles";
import {DefaultStyles} from "./default.styles";
import {GeneralStyles} from "./general.styles";

export const CreatePostPageStyles = css`
  ${ResetStyles}
  ${DefaultStyles}
  ${GeneralStyles}
    
  //:host {
  //  display: flex;
  //  flex-direction: column;
  //  align-items: center;
  //  justify-content: center;
  //  height: 100vh;
  //  width: 100vw;
  //}

  .create-post-container {
    width: 100%;
    display: flex;
    overflow: auto;
    min-height: 100vh;
    align-items: center;
    flex-direction: column;
  }
  .create-post-banner {
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
  .create-post-text {
    color: #277bc0;
    font-size: 3rem;
    text-align: center;
  }
  .create-post-container1 {
    width: 60%;
    height: auto;
    display: flex;
    align-items: flex-end;
    flex-direction: column;
    justify-content: flex-start;
  }
  .create-post-textinput {
    width: 100%;
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    background-color: #d9d9d9;
  }
  .create-post-textarea {
    width: 100%;
    height: 147px;
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    background-color: #d9d9d9;
  }
  .create-post-button {
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    border-radius: var(--dl-radius-radius-radius8);
    background-color: #b4cde6;
  }
  .create-post-text1 {
    color: #277bc0;
  }
  .create-post-text2 {
    font-weight: 700;
  }
  .create-post-container2 {
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
  .create-post-text4 {
    flex: 1;
    align-self: center;
    text-align: right;
    font-weight: 700;
    padding-right: var(--dl-space-space-oneandhalfunits);
  }
  .create-post-select {
    flex: 1;
    width: 50%;
    height: 24px;
    align-self: center;
  }
  .create-post-button1 {
    align-self: center;
    margin-top: var(--dl-space-space-unit);
    border-width: 0px;
    border-radius: var(--dl-radius-radius-radius8);
    background-color: #b4cde6;
  }
  .create-post-text5 {
    color: #277bc0;
  }
  .create-post-text6 {
    font-weight: 700;
  }
  @media(max-width: 767px) {
    .create-post-banner {
      padding-left: var(--dl-space-space-twounits);
      padding-right: var(--dl-space-space-twounits);
    }
  }
  @media(max-width: 479px) {
    .create-post-banner {
      padding-top: var(--dl-space-space-twounits);
      padding-left: var(--dl-space-space-unit);
      padding-right: var(--dl-space-space-unit);
      padding-bottom: var(--dl-space-space-twounits);
    }
  }
`;
