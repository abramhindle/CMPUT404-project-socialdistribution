import {css} from "@microsoft/fast-element";
import {ResetStyles} from "./reset.styles";
import {DefaultStyles} from "./default.styles";
import {GeneralStyles} from "./general.styles";


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
    width: 100px;
    object-fit: cover;
    margin-right: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-container2 {
    flex: 0 0 auto;
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
    justify-content: flex-start;
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

  .post-container4 {
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

  .post-text2 {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-text3 {
    margin-top: var(--dl-space-space-halfunit);
    margin-right: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-image1 {
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

  .post-container5 {
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

  .post-text4 {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-text5 {
    margin-top: var(--dl-space-space-halfunit);
    margin-right: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-image2 {
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

  .post-container6 {
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

  .post-text6 {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-text7 {
    margin-top: var(--dl-space-space-halfunit);
    margin-right: var(--dl-space-space-unit);
    border-radius: var(--dl-radius-radius-radius4);
    margin-bottom: var(--dl-space-space-halfunit);
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .post-image3 {
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
