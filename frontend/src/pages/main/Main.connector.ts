import { FASTElement } from "@microsoft/fast-element";
import { Main } from "./Main";
import { MainPageStyles as styles } from "./Main.styles";
import { MainPageTemplate as template } from "./Main.template";

export const mainPageDefinition = {
    name: "main-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

export class MainPageComponent extends Main {};
FASTElement.define(MainPageComponent, mainPageDefinition);
