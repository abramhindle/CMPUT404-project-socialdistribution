import { Author, ContentType, FollowRequest, PaginatedResponse, Post, Comment, Like } from "./SocialApiModel";

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

    export function followRequestDataTransform(followRequestData: any): FollowRequest | null {
        const myFollowRequest = new FollowRequest();
        const sender = authorDataTransform(followRequestData.sender);
        if (sender) {
            myFollowRequest.sender = sender;
        }

        return myFollowRequest;
    }

    export function authorDataTransform(authorData: any): Author | null {
        if (!authorData) {
            return null;
        }

        if (!authorData.id || !authorData.display_name) {
            return null;
        }

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
        myPost.contentType = parseContentType(postData.content_type);
        myPost.content = postData.content;
        myPost.published = new Date(postData.created_at);
        myPost.source = postData.source;
        myPost.origin = postData.origin;
        myPost.url = postData.url;
        myPost.likes = postData.likes_count;
        return myPost;
    }

    export function commentDataTransform(commentData: any): Comment | null {
        if (!commentData) {
            return null;
        }

        if (!commentData.id) {
            return null;
        }

        const myComment = new Comment(commentData.id)
        const author = SocialApiTransform.authorDataTransform(commentData.author);
        if (author) {
            myComment.author = author
        }
        myComment.comment = commentData.comment
        myComment.contentType = parseContentType(commentData.content_type)
        myComment.published = new Date(commentData.created_at);

        return myComment
    }

    export function likeDataTransform(likeData: any): Like | null {
        if (!likeData) {
            return null;
        }

        const myLike = new Like()
        const author = SocialApiTransform.authorDataTransform(likeData.author);
        if (author) {
            myLike.author = author
        }
        myLike.post = likeData.post;

        return myLike;
    }

    function parseContentType(contentType: string): ContentType {
        switch (contentType) {
            case "text/plain":
                return ContentType.Plain
            case "text/markdown":
                return ContentType.Markdown
            case "image/jpeg;base64":
            case "image/png;base64":
                return ContentType.Image
            default:
                return ContentType.Plain
        }
    }
}
