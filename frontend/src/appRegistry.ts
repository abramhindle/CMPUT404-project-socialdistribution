import { MyTemplateComponent } from "./components/templateComponent/TemplateComponent.connector";
import { MainPageComponent } from "./pages/main/Main.connector";
import { ProfilePageComponent } from "./pages/profile/Profile.connector";

const pageDictionary = {
    "main-page": MainPageComponent,
    "profile-page": ProfilePageComponent
}

const componentDictionary = {
    "my-template-component": MyTemplateComponent
}

const libraryDictionary = {};

export const appRegistry = { pageDictionary, componentDictionary, libraryDictionary };
