import { PartialFASTElementDefinition } from "@microsoft/fast-element";
import { TemplateComponent } from "./components/templateComponent/TemplateComponent";
import { templateComponent } from "./components/templateComponent/TemplateComponent.connector";
import { mainPage, MainPageComponent } from "./pages/main/Main.connector";
import { profilePage, ProfilePageComponent } from "./pages/profile/Profile.connector";

export class ComponentEntry {
    public definition: PartialFASTElementDefinition;
    public type: any;

    constructor(definition: PartialFASTElementDefinition, type: any) {
        this.definition = definition;
        this.type = type;
    }
}

// Pages
const pages: ComponentEntry[] = [
    new ComponentEntry(mainPage, MainPageComponent),
    new ComponentEntry(profilePage, ProfilePageComponent)
]

// Common Components
const webComponents: ComponentEntry[] = [
    new ComponentEntry(templateComponent, TemplateComponent)
]

export const appRegistry = [ ...pages, ...webComponents ];
