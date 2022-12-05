import { icon } from "@fortawesome/fontawesome-svg-core";
import { html, ref, when } from "@microsoft/fast-element";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { FollowStatus } from "../../libs/core/PageModel";
import { Profile } from "./Profile";

const editProfileModal = html<Profile>`
    <form ${ref("form")} @submit="${(x, c) => x.editProfile(c.event)}" id="edit-profile" class=" ${x => x.modalStateStyle}">
        <div class="modal-content">
            <div class="edit-header">
                <button type="button" @click=${x => x.closeEditModal()}>
                    X
                </button>
                <h4>Edit Profile</h4>
                <button class="save-edit">Save</button>
            </div>
            <div class="edit-form">
                <div class="form-element">
                    <fast-text-field type="text" value="${x => x.user?.displayName}" name="display_name" required>Display Name</fast-text-field>
                    <fast-text-field type="url" value="${x => x.user?.githubHandle}" name="github_handle">GitHub</fast-text-field>
                    <label>Profile Image</label>
                    <img class="profile-image" src="${x => x.user?.profileImage}">
                    <input class="image-upload" type="file" name="image" accept="image/png, image/jpeg">
                </div>
            </div>
        </div>
    </form>
`;

export const ProfilePageTemplate = html<Profile>`
    <page-layout
        :userId="${x => x.userId}"
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
    ${when(x => x.profile, html<Profile>`
        ${editProfileModal}
        <div class="profile-background ${x => LayoutHelpers.getLayoutStyle(x.layoutType)}"></div>
        <div class="profile-info">
            <img class="profile-image" src="${x => x.profile?.profileImage}">
            <div class="display-name">
                <div class="profile-info-display">
                    <h2>${x => x.profile?.displayName}</h2>
                    <h4>
                        <a href="${x => x.profile?.githubHandle}" target="_blank">
                            <div class="profile-info-icon" :innerHTML="${_ => icon({ prefix: "fas", iconName: "code-pull-request" }).html}"></div>
                            <span class="profile-link-text">GitHub Handle</span>
                        </a>
                    </h4>
                </div>
                ${when(x => x.user?.id == x.profile?.id, html<Profile>`
                <button @click=${x => x.openEditModal()}>
                    Edit Profile
                </button>
                `)}
                ${when(x => x.user?.id != x.profile?.id, html<Profile>`
                <button class=" ${x => x.followStatus == FollowStatus.NotFollowing}" @click=${(x, c) => x.followRequest()}>
                    ${x => LayoutHelpers.parseFollowStatus(x.followStatus)}
                </button>
                `)}
            </div>
            <div class="user-buttons">
            ${when(x => x.user?.id == x.profile?.id, html<Profile>`
                <a class="logout" href="/logout/">
                    Logout
                </a>
            `)}
                <a class="followers" href="${x => x.profile?.id}/followers/">
                    Followers
                </a>
            </div>
        </div>
    `)}
    ${when(x => !x.profile, html<Profile>`
        <h1>${x => x.loadedProfileText}</h1>
    `)}
    </page-layout>
`;