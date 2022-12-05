import {css} from "@microsoft/fast-element";
import {ResetStyles} from "./reset.styles";
import {DefaultStyles} from "./default.styles";
import {GeneralStyles} from "./general.styles";
import { typeRampPlus1FontSize, typeRampPlus2FontSize } from "@microsoft/fast-components";


export const LikesModalComponentStyles = css`
  ${ResetStyles}
  ${DefaultStyles}
  ${GeneralStyles}
  
  .likes-container {
    width: 100%;
    height: 400px;
    display: flex;
    position: relative;
    align-items: flex-start;
    flex-direction: column;
    background-color: var(--dl-color-gray-white);
    z-index: 10;
  }

  .likes-banner {
    display: flex;
    width: 100%;
    padding: 10px;
    justify-content: space-between;
    align-items: center;
    font-size: ${typeRampPlus2FontSize};
    font-weight: bold;
    background-image: linear-gradient(93.58deg, #9F83C7 0%, #ABD9FF 100%);
  }

  .likes-text {
    color: black;
    font-size: 3rem;
    align-self: center;
    text-align: center;
  }

  .likes-ul {
    width: 90%;
    height: 90%;
    overflow: auto;
    align-self: center;
    padding-left: 0px;
  }

  .likes-li {
    margin-right: 0px;
  }

  .likes-container {
    gap: var(--dl-space-space-unit);
    flex: 0 0 auto;
    width: 100%;
    height: auto;
    display: flex;
    position: relative;
    align-items: flex-start;
    border-radius: 4px;
    margin-bottom: var(--dl-space-space-unit);
    padding-right: 0px;
    justify-content: flex-start;
    background-color: #d9d9d9;
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .likes-text {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    margin-bottom: var(--dl-space-space-halfunit);
  }

  .likes-image {
    top: 0px;
    right: 0px;
    width: auto;
    height: 100%;
    position: absolute;
    object-fit: cover;
  }

  .likes-container2 {
    gap: var(--dl-space-space-unit);
    flex: 0 0 auto;
    width: 100%;
    height: auto;
    display: flex;
    position: relative;
    align-items: flex-start;
    border-radius: 4px;
    margin-bottom: var(--dl-space-space-unit);
    padding-right: 0px;
    justify-content: flex-start;
    background-color: #d9d9d9;
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .close-modal {
    border-radius: 50px;
    padding: 8px 20px;
    border: 0;
    background-color: black;
    color: white;
    font-size: ${typeRampPlus1FontSize};
    cursor: pointer;
  }

  .likes-text2 {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    margin-bottom: var(--dl-space-space-halfunit);
  }

  .likes-image1 {
    top: 0px;
    right: 0px;
    width: auto;
    height: 100%;
    position: absolute;
    object-fit: cover;
  }

  .likes-container3 {
    gap: var(--dl-space-space-unit);
    flex: 0 0 auto;
    width: 100%;
    height: auto;
    display: flex;
    position: relative;
    align-items: flex-start;
    border-radius: 4px;
    margin-bottom: var(--dl-space-space-unit);
    padding-right: 0px;
    justify-content: flex-start;
    background-color: #d9d9d9;
    border-top-left-radius: var(--dl-radius-radius-radius4);
    border-top-right-radius: var(--dl-radius-radius-radius4);
    border-bottom-left-radius: var(--dl-radius-radius-radius4);
    border-bottom-right-radius: var(--dl-radius-radius-radius4);
  }

  .likes-text3 {
    margin-top: var(--dl-space-space-halfunit);
    margin-left: var(--dl-space-space-unit);
    margin-bottom: var(--dl-space-space-halfunit);
  }

  .likes-image2 {
    top: 0px;
    right: 0px;
    width: auto;
    height: 100%;
    position: absolute;
    object-fit: cover;
  }

  @media (max-width: 991px) {
    .likes-container1 {
      position: relative;
    }

    .likes-image {
      top: 0px;
      right: 0px;
      width: auto;
      height: 100%;
      position: absolute;
    }

    .likes-container2 {
      position: relative;
    }

    .likes-image1 {
      top: 0px;
      right: 0px;
      width: auto;
      height: 100%;
      position: absolute;
    }

    .likes-container3 {
      position: relative;
    }

    .likes-image2 {
      top: 0px;
      right: 0px;
      width: auto;
      height: 100%;
      position: absolute;
    }
  }
  @media (max-width: 767px) {
    .likes-banner {
      padding-left: var(--dl-space-space-twounits);
      padding-right: var(--dl-space-space-twounits);
    }
  }
  @media (max-width: 479px) {
    .likes-banner {
      padding-top: var(--dl-space-space-twounits);
      padding-left: var(--dl-space-space-unit);
      padding-right: var(--dl-space-space-unit);
      padding-bottom: var(--dl-space-space-twounits);
    }
  }
`;
