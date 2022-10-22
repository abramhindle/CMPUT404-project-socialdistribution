import { SocialApiUrls } from "./SocialApiUrls";

export namespace SocialApi {
    var serializeForm = function (formData: FormData) {
        var obj: { [key: string]: any; } = {};
        formData.forEach((value: any, key: string, formData: FormData) => {
            obj[key] = value;
        })
        return obj;
    };

    export function register(registerForm: FormData) {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json; charset=UTF-8" },
            body: JSON.stringify(serializeForm(registerForm))
        };

        return fetch(SocialApiUrls.REGISTER, requestOptions)
            .then(handleResponse)
            .then(data => {
                if (data && data.username == registerForm.get("username")
                    && data.display_name == registerForm.get("display_name")) {
                    // window.location.replace("/login/");
                }

                return data;
            });
    }

    function logout() {
        const requestOptions = {
            method: "POST"
        };

        return fetch(SocialApiUrls.LOGOUT, requestOptions)
            .then(handleResponse)
            .then(data => {
                if (data) {
                }

                return data;
            });
    }

    function handleResponse(response: any) {
        return response.text().then((text: string) => {
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

                return messages;
            }

            return data;
        });
    }
}

