import { TemplateComponent } from "./TemplateComponent";
import { TemplateComponentStyles as styles } from "./TemplateComponent.styles";
import { TemplateComponentTemplate as template } from "./TemplateComponent.template";

export const templateComponent = {
    name: "my-template-component",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

export class MyTemplateComponent extends TemplateComponent {};
