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

export const FeedType = Object.freeze({
    All: "All",
    Stream: "Stream"
} as const);

export type FeedType = keyof typeof FeedType;

