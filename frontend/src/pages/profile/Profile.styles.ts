import { css } from "@microsoft/fast-element";
import { accentColor, bodyFont, controlCornerRadius, neutralColor, neutralFillStrongHover, typeRampPlus2FontSize } from "@microsoft/fast-components";
export const ProfilePageStyles = css`
  
    :img {
        border-radius: 50%;
      }
    .top{
        background: linear-gradient(to bottom right, ${neutralColor}, ${accentColor});
        top: 0;
        width: 100%;
    }

    .whole {
        width: 100%;
        height: 2160px;
        background: rgba(255,255,255,1);
        opacity: 1;
        position: relative;
        top: 0px;
        left: 0px;
        overflow: hidden;
      }
    .top {
        width: 100%;
        height: 480px;
        background: linear-gradient(rgba(159,130,198,1), rgba(171,217,255,1));
        opacity: 1;
        position: relative;
        top: 0px;
        left: 0px;
        overflow: hidden;
      }
   
   
    .btn {
        width: 50px;
        color: rgba(39,123,192,1);
        position: absolute;
        top: 74px;
        left: 101px;
        font-family: Inter;
        font-weight: Semi Bold;
        font-size: 20px;
        opacity: 1;
        text-align: center;
    }
    .form-element {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-content: center;
      align-items: center;
  }
`;