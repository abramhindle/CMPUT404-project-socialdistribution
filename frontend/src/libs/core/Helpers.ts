import { LayoutStyleClass, LayoutType } from "./PageModel";

export namespace LayoutHelpers {
    export function getLayoutStyle(layoutType: LayoutType) {
        switch (layoutType) {
            case LayoutType.Desktop:
                return LayoutStyleClass.Desktop
            case LayoutType.Tablet:
                return LayoutStyleClass.Tablet
            default:
                return LayoutStyleClass.Mobile
        }
    }
}