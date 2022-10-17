import { FASTElement } from "@microsoft/fast-element";
import { Profile } from "./Profile";
import { ProfilePageStyles as styles } from "./Profile.styles";
import { ProfilePageTemplate as template } from "./Profile.template";

export const profilePageDefinition = {
    name: "profile-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

export class ProfilePageComponent extends Profile {};
FASTElement.define(ProfilePageComponent, profilePageDefinition);
