export const LayoutType = Object.freeze({
    Desktop: "Desktop",
    Tablet: "Tablet",
    Mobile: "Mobile"
} as const);

export type LayoutType = keyof typeof LayoutType;

export const LayoutStyleClass = Object.freeze({
    Desktop: "layout-desktop",
    Tablet: "layout-tablet",
    Mobile: "layout-mobile"
});