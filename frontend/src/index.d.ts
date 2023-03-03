export interface Author {
    type: string;
    id: string;
    host: string;
    displayName: string;
    url: string;
    github: string;
    profileImage: string;
}

export interface Post {
    type: string;
    id: string;
    title: string;
    description: string;
    source: string;
    origin: string;
    contentType: string;
    content: string;
    author: Author;
    categories: string[];
    count: number;
    comments: string;
    commentSrc: [];
    visibility: boolean;
    unlisted: boolean;
}