import { FASTElement } from "@microsoft/fast-element";
import { TemplateComponent } from "./TemplateComponent";
import { TemplateComponentStyles as styles } from "./TemplateComponent.styles";
import { TemplateComponentTemplate as template } from "./TemplateComponent.template";

export const mainPageDefinition = {
    name: "my-template-component",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

export class MyTemplateComponent extends TemplateComponent {};
FASTElement.define(MyTemplateComponent, mainPageDefinition);
