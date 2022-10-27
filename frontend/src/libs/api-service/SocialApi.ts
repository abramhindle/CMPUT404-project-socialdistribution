import { SocialApiConstants } from "./SocialApiConstants";
import { Author } from "./SocialApiModel";
import { SocialApiTransform } from "./SocialApiTransform";
import { SocialApiUrls } from "./SocialApiUrls";

export namespace SocialApi {
    function serializeForm(formData: FormData) {
        var obj: { [key: string]: any; } = {};
        formData.forEach((value: any, key: string, formData: FormData) => {
            obj[key] = value;
        })
        return obj;
    }

    function authHeader(): string {
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

        return SocialApiTransform.jsonDataAuthorTransform(text);
    }
}

