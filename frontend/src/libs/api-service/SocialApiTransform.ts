import { Author } from "./SocialApiModel";

export namespace SocialApiTransform {
    export function jsonDataAuthorTransform(jsonData: string): Author | null {
        const authorData = JSON.parse(jsonData);
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
}