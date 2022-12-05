export const ContentType = Object.freeze({
    Markdown: "markdown",
    Plain: "plain"
});

export type ContentType = keyof typeof ContentType;

export const ApiObjectType = Object.freeze({
    follow: "follow",
    post: "post"
});

export type ApiObjectType = keyof typeof ApiObjectType;

export class Author {
    id: string;
    displayName: string;
    url?: string;
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

    content?: string;

    url?: string;

    constructor(id: string) {
        this.id = id;
    }
}

export class FollowRequest {
    sender?: Author;
}

export class PaginatedResponse {
    count?: number;

    next?: string;

    previous?: string;

    results?: any[];
}

export interface ApiObject {
    type?: ApiObjectType;
}

export class FollowRequestBody implements ApiObject {
    type: ApiObjectType = ApiObjectType.follow;

    sender?: FollowInfo;

    receiver?: FollowInfo;
}

export class FollowDecisionBody {
    follow_request_sender?: FollowInfo
}

export class FollowRemovalBody {
    follower?: FollowInfo;
}


export class FollowInfo {
    url: string;

    id: string;

    constructor(url: string, id: string) {
        this.url = url;
        this.id = id;
    }
}