import { Main } from "./Main";
import { MainPageStyles as styles } from "./Main.styles";
import { MainPageTemplate as template } from "./Main.template";

export const mainPage = {
    name: "main-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

export class MainPageComponent extends Main {};
