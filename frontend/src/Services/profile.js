import { patch } from "./requests";


export function editAvatar(avatarURL, imageData) {
    return patch(avatarURL, {"content": imageData});
}

export function editGitHub(profileURL, gitHub) {
    return patch(profileURL, {"github": "https://www.github.com/" + gitHub});
}

export function editProfile(profile, imageData, gitHub) {
    return Promise.all([editAvatar(profile.profileImage, imageData), editGitHub(profile.url, gitHub)])
}