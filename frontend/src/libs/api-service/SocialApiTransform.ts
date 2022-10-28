import { Author, PaginatedResponse, Post } from "./SocialApiModel";

export namespace SocialApiTransform {
    export function parseJsonPaginatedData(jsonData: string): PaginatedResponse | null {
        const paginatedData = JSON.parse(jsonData);
        if (!paginatedData) {
            return null;
        }

        if (!paginatedData) {
            return null;
        }

        return paginatedData as PaginatedResponse;
    }

    export function parseJsonAuthorData(jsonData: string): Author | null {
        const authorData = JSON.parse(jsonData);
        if (!authorData) {
            return null;
        }

        if (!authorData.id || !authorData.display_name) {
            return null;
        }

        return authorDataTransform(authorData);
    }

    export function authorDataTransform(authorData: any): Author | null {
        const myAuthor = new Author(authorData.id, authorData.display_name);
        myAuthor.url = authorData.url;
        myAuthor.githubHandle = authorData.github_handle
        myAuthor.profileImage = authorData.profile_image
        return myAuthor;
    }

    export function parseJsonPostData(jsonData: string): Post | null {
        const postData = JSON.parse(jsonData);
        if (!postData) {
            return null;
        }

        if (!postData.id) {
            return null;
        }

        return postDataTransform(postData);
    }

    export function postDataTransform(postData: any): Post | null {
        const myPost = new Post(postData.id);
        const myAuthor = authorDataTransform(postData.author);
        if (myAuthor) {
            myPost.author = myAuthor;
        }
        myPost.title = postData.title;
        myPost.description = postData.description;
        myPost.unlisted = postData.unlisted;
        myPost.contentType = postData.content_type;
        myPost.content = postData.content;
        myPost.published = postData.created_at;
        myPost.source = postData.source;
        myPost.origin = postData.origin;
        return myPost;
    }
}
