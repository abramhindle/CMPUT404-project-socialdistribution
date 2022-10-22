import { parseColorHexRGB, parseColor } from "@microsoft/fast-colors";
import { accentColor, baseLayerLuminance, bodyFont, controlCornerRadius, neutralColor, neutralFillLayerRecipe, neutralPalette, PaletteRGB, provideFASTDesignSystem, SwatchRGB, typeRampBaseFontSize } from "@microsoft/fast-components";
import { Colors } from "../../libs/core/Colors";
import { ComponentEntry, defineComponent } from "../AppRegistry";
import { Home } from "./Home";
import { HomePageStyles as styles } from "./Home.styles";
import { HomePageTemplate as template } from "./Home.template";



export const homePage = {
    name: "home-page",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(homePage, Home));

provideFASTDesignSystem()
    .register();

neutralColor.withDefault(SwatchRGB.from(parseColorHexRGB(Colors.NEUTRAL)!));
accentColor.withDefault(SwatchRGB.from(parseColorHexRGB(Colors.ACCENT)!));
controlCornerRadius.withDefault(2);
typeRampBaseFontSize.withDefault('12px');
baseLayerLuminance.withDefault(1.0);
bodyFont.withDefault("Inter");

