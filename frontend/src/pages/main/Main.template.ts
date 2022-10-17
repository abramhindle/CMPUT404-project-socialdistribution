import { html } from "@microsoft/fast-element";
import { MyTemplateComponent } from "../../components/templateComponent/TemplateComponent.connector";
import { Main } from "./Main";

MyTemplateComponent;

export const MainPageTemplate = html<Main>`
    <my-template-component></my-template-component>
    <div>${x => x.greeting} world!</div>
`;