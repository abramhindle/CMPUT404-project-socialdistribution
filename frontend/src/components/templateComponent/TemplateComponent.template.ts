import { html } from "@microsoft/fast-element";
import { TemplateComponent } from "./TemplateComponent";


export const TemplateComponentTemplate = html<TemplateComponent>`
    <div>${x => x.greeting} world!</div>
`;