import { SocialApiConstants } from "./SocialApiConstants";
import { Author, PaginatedResponse, Post } from "./SocialApiModel";
import { SocialApiTransform } from "./SocialApiTransform";
import { SocialApiUrls } from "./SocialApiUrls";
import { textFieldStyles } from "@microsoft/fast-components";


export type PostVisibility = 'PUBLIC' | 'PRIVATE' | 'FRIENDS';
export type ContentTypes = 'text/plain';

export namespace SocialApi {
    export function serializeForm(formData: FormData) {
        var obj: { [key: string]: any; } = {};
        formData.forEach((value: any, key: string, formData: FormData) => {
            obj[key] = value;
        })
        return obj;
    }

    export function authHeader(): string {
        const authentication = localStorage.getItem(SocialApiConstants.AUTHENTICATION_STORAGE);
        if (!authentication) {
            return ""
        }
        const parsedAuthentication = JSON.parse(authentication);

        if (parsedAuthentication) {
            return `Basic ${parsedAuthentication}`;
        }

        return "";
    }

    export async function register(registerForm: FormData) {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json; charset=UTF-8" },
            body: JSON.stringify(serializeForm(registerForm))
        };

        const response = await fetch(SocialApiUrls.REGISTER, requestOptions);
        const text = await response.text();
        const data = text && JSON.parse(text);
        if (!response.ok) {
            const messages = [];
            if (data) {
                if (data.username) {
                    messages.push(...data.username);
                }

                if (data.password) {
                    messages.push(data.password);
                }
            }

            throw messages;
        }

        return data;
    }

    export async function login(loginForm: FormData) {
        const serializedForm = serializeForm(loginForm);
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json; charset=UTF-8" },
            body: JSON.stringify(serializedForm)
        };

        const response = await fetch(SocialApiUrls.LOGIN, requestOptions);
        const text = await response.text();
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (data) {
                throw data.message;
            }
        }

        if (data) {
            localStorage.setItem(
                SocialApiConstants.AUTHENTICATION_STORAGE,
                JSON.stringify(window.btoa(serializedForm.username + ":" + serializedForm.password)));
        }

        return data;
    }


    export async function logout() {
        const requestOptions = {
            method: "POST"
        };

        const response = await fetch(SocialApiUrls.LOGOUT, requestOptions);
        const text = await response.text();
        const data = text && JSON.parse(text);
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        if (data) {
            localStorage.removeItem(SocialApiConstants.AUTHENTICATION_STORAGE);
        }

        return data;
    }

    export async function fetchAuthor(id: string): Promise<Author | null> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());

        const requestOptions = {
            method: "GET",
            credentials: credentialType,
            headers: headers
        };

        const response = await fetch(SocialApiUrls.AUTHORS + id + "/", requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return SocialApiTransform.parseJsonAuthorData(text);
    }

    export async function fetchAuthors(): Promise<any[] | null> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());

        const requestOptions = {
            method: "GET",
            credentials: credentialType,
            headers: headers
        };

        const response = await fetch(SocialApiUrls.AUTHORS, requestOptions);
        const json = await response.json();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return json;
    }

    export async function editProfile(userId: string, profileDataForm: FormData): Promise<Author | null> {
        const url = new URL(SocialApiUrls.AUTHORS + userId + "/", window.location.origin)

        return SocialApiTransform.authorDataTransform(await fetchAuthorized(url, "POST", JSON.stringify(serializeForm(profileDataForm))));
    }

    export async function fetchPaginatedInbox(authorId: string, page: number, size: number) {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.INBOX, window.location.origin);
        url.searchParams.append("page", page.toString())
        url.searchParams.append("size", size.toString())

        return fetchPaginatedResponseInternal(url);
    }

    export async function fetchPaginatedFollowers(authorId: string, page: number, size: number) {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS, window.location.origin)
        url.searchParams.append("page", page.toString())
        url.searchParams.append("size", size.toString())

        return fetchPaginatedResponseInternal(url);
    }

    export async function fetchAuthorPosts(authorId: string, page: number, size: number): Promise<PaginatedResponse | null> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.POSTS, window.location.origin);
        url.searchParams.append("page", page.toString())
        url.searchParams.append("size", size.toString())

        return fetchPaginatedResponseInternal(url);
    }

    export async function fetchPublicPosts(): Promise<PaginatedResponse | null> {
        const url = new URL(SocialApiUrls.PUBLIC_POSTS, window.location.origin);

        return fetchPaginatedResponseInternal(url);
    }

    export async function fetchPaginatedNext(nextUrl: string): Promise<PaginatedResponse | null> {
        const url = new URL(nextUrl);

        return fetchPaginatedResponseInternal(url);
    }

    async function fetchPaginatedResponseInternal(url: URL): Promise<PaginatedResponse | null> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());

        const requestOptions = {
            method: "GET",
            credentials: credentialType,
            headers: headers
        };

        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return SocialApiTransform.parseJsonPaginatedData(text);
    }

    export async function fetchPost(postId: string, authorId: string): Promise<Post | null> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());
        headers.set("Content-Type", "application/json; charset=UTF-8");

        const requestOptions = {
            method: "GET",
            credentials: credentialType,
            headers: headers,
        };

        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.POSTS + postId, window.location.origin);

        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return SocialApiTransform.parseJsonPostData(text);
    }

    export async function updatePost(
        postId: string,
        authorId: string,
        formData: FormData
    ) {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());
        headers.set("Content-Type", "application/json; charset=UTF-8");

        const body: string = JSON.stringify(serializeForm(formData));

        const requestOptions = {
            method: "POST",
            credentials: credentialType,
            headers,
            body
        };

        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.POSTS + postId + '/', window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return SocialApiTransform.parseJsonPostData(text);
    }

    export async function createPost(
        authorId: string,
        formData: FormData
    ): Promise<Post | null> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());
        headers.set("Content-Type", "application/json; charset=UTF-8");

        const data = serializeForm(formData);

        const body: string = JSON.stringify(data);

        const requestOptions = {
            method: "POST",
            credentials: credentialType,
            headers: headers,
            body: body
        };

        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.POSTS, window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return SocialApiTransform.parseJsonPostData(text);
    }

    export async function deletePost(
        authorId: string,
        postId: string
    ): Promise<{ 'message': 'Object deleted!' } | null> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());
        headers.set("Content-Type", "application/json; charset=UTF-8");

        const requestOptions = {
            method: 'DELETE',
            credentials: credentialType,
            headers
        };

        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.POSTS + postId, window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return JSON.parse(text);
    }

    export async function fetchAuthorized(url: URL, method: string, body?: string): Promise<any> {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", SocialApi.authHeader());
        if (method !== "GET") {
            headers.set("Content-Type", "application/json; charset=UTF-8");
        }

        const requestOptions = {
            method: method,
            credentials: credentialType,
            headers: headers,
            body: body,
        };

        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return JSON.parse(text);
    }

    export async function likePost(
        postId: string,
        likeAuthorId: string,
        likeAuthorUrl: string,
        postAuthorId: string,
        postAuthorUrl: string
    ) {
        const body = JSON.stringify({
            type: 'like',
            author: {
                id: likeAuthorId,
                url: likeAuthorUrl
            },
            post: {
                id: postId,
                author: {
                    id: postAuthorId,
                    url: postAuthorUrl
                }
            }
        });

        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());
        headers.set("Content-Type", "application/json; charset=UTF-8");

        const requestOptions = {
            method: "POST",
            credentials: credentialType,
            headers: headers,
            body: body
        };

        const url = new URL(SocialApiUrls.AUTHORS + postAuthorId + SocialApiUrls.INBOX, window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return text;
    }

    export async function getPostLikes(postId: string, authorId: string) {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());

        const requestOptions = {
            method: "GET",
            credentials: credentialType,
            headers: headers,
        };

        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.POSTS + postId + SocialApiUrls.LIKES, window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        console.log("Success:", JSON.parse(text));
        return JSON.parse(text);
    }

    export async function getComments(postAuthorId: string, postId: string) {
        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());

        const requestOptions = {
            method: "GET",
            credentials: credentialType,
            headers: headers,
        };

        const url = new URL(SocialApiUrls.AUTHORS + postAuthorId + SocialApiUrls.POSTS + postId + SocialApiUrls.COMMENTS, window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        console.log("Success:", JSON.parse(text));
        return JSON.parse(text);
    }

    export async function postComment(
        authorId: string,
        authorUrl: string,
        postId: string,
        postAuthorId: string,
        postAuthorUrl: string,
        commentForm: FormData) {
        const comment = serializeForm(commentForm)["comment"];
        const body = JSON.stringify({
            type: "comment",
            author: {
                id: authorId,
                url: authorUrl
            },
            post: {
                id: postId,
                author: {
                    id: postAuthorId,
                    url: postAuthorUrl
                }
            },
            comment,
            content_type: "text/plain"
        });

        const credentialType: RequestCredentials = "include";
        const headers: HeadersInit = new Headers();
        headers.set("Authorization", authHeader());
        headers.set("Content-Type", "application/json; charset=UTF-8");

        const requestOptions = {
            method: "POST",
            credentials: credentialType,
            headers: headers,
            body: body
        };

        const url = new URL(SocialApiUrls.AUTHORS + postAuthorId + SocialApiUrls.INBOX, window.location.origin);
        const response = await fetch(url, requestOptions);
        const text = await response.text();
        if (!response.ok) {
            throw new Error(response.statusText)
        }

        return text;
    }
}

