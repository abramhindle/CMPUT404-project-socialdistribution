import { parseColorHexRGB } from "@microsoft/fast-colors";
import { accentColor, baseLayerLuminance, bodyFont, controlCornerRadius, neutralColor, provideFASTDesignSystem, SwatchRGB, typeRampBaseFontSize } from "@microsoft/fast-components";
import { Colors } from "../../libs/core/Colors";
import { ComponentEntry, defineComponent } from "../../pages/AppRegistry";
import { Layout } from "./Layout";
import { LayoutStyles as styles } from "./Layout.styles";
import { LayoutTemplate as template } from "./Layout.template";

export const layoutComponent = {
    name: "page-layout",
    template,
    styles,
    shadowOptions: {
        delegatesFocus: true,
    },
};

defineComponent(new ComponentEntry(layoutComponent, Layout));

provideFASTDesignSystem()
    .register();

neutralColor.withDefault(SwatchRGB.from(parseColorHexRGB(Colors.NEUTRAL)!));
accentColor.withDefault(SwatchRGB.from(parseColorHexRGB(Colors.ACCENT)!));
controlCornerRadius.withDefault(2);
typeRampBaseFontSize.withDefault('12px');
baseLayerLuminance.withDefault(1.0);
bodyFont.withDefault("Inter");


