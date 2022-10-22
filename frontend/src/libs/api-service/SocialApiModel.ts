const ContentType = Object.freeze({
    Markdown: "markdown",
    Plain: "plain"
});

export type ContentType = typeof ContentType[keyof typeof ContentType];

export class Author {
    id: string;
    displayName: string;
    profileImage?: string;
    githubHandle?: string;

    constructor(id: string, displayName: string) {
        this.id = id;
        this.displayName = displayName;
    }
}

export class Post {
    id: string;
    
    title?: string;

    source?: string;

    origin?: string;

    description?: string;

    contentType?: ContentType;

    author?: Author;

    categories?: string[];

    likes?: number;

    comments?: number;

    unlisted?: boolean;

    published?: Date;

    visibility?: string;

    constructor(id: string) {
        this.id = id;
    }
}