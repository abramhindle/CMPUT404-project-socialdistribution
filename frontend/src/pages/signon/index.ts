import { parseColorHexRGB } from "@microsoft/fast-colors";
import { accentColor, baseHeightMultiplier, baseLayerLuminance, bodyFont, controlCornerRadius, fastTextField, neutralColor, provideFASTDesignSystem, SwatchRGB, textFieldStyles, typeRampBaseFontSize, typeRampPlus1FontSize, typeRampPlus2FontSize } from "@microsoft/fast-components";
import { css } from "@microsoft/fast-element";
import { Colors } from "../../libs/core/Colors";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { SignOn } from "./SignOn";
import { SignOnPageStyles as styles } from "./SignOn.styles";
import { SignOnPageTemplate as template } from "./SignOn.template";

export const signOnPage = {
    name: "signon-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(signOnPage, SignOn));

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

neutralColor.withDefault(SwatchRGB.from(parseColorHexRGB(Colors.NEUTRAL)!));
accentColor.withDefault(SwatchRGB.from(parseColorHexRGB(Colors.ACCENT)!));
controlCornerRadius.withDefault(10);
typeRampBaseFontSize.withDefault('12px');
baseHeightMultiplier.withDefault(15);
baseLayerLuminance.withDefault(1.0);
bodyFont.withDefault("Inter");
