import { parseColorHexRGB } from "@microsoft/fast-colors";
import { accentColor, baseHeightMultiplier, baseLayerLuminance, bodyFont, controlCornerRadius, fastTextField, neutralColor, provideFASTDesignSystem, SwatchRGB, textFieldStyles, typeRampBaseFontSize, typeRampPlus1FontSize, typeRampPlus2FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { Colors } from "../../libs/core/Colors";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { Profile } from "./Profile";
import { ProfilePageStyles as styles } from "./Profile.styles";
import { ProfilePageTemplate as template } from "./Profile.template";

export const profilePage = {
    name: "profile-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(profilePage, Profile));

provideFASTDesignSystem()
      .register(
        fastTextField({
            prefix: "",
            styles: (ctx, def) => css`
                .root input {
                    font-size: ${typeRampPlus2FontSize};
                }

                ${textFieldStyles(ctx, def)}
            `
        })
      );
