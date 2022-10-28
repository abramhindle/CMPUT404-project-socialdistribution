import { faHouse, faInbox, faUserGroup, faUser } from "@fortawesome/free-solid-svg-icons";
import { FASTElement, observable } from "@microsoft/fast-element";
import { LayoutType } from "../../libs/core/PageModel";
import { Author } from "../../libs/api-service/SocialApiModel";
import { icon, library } from "@fortawesome/fontawesome-svg-core";
import { SocialApiUrls } from "../../libs/api-service/SocialApiUrls";

export const NavItem = Object.freeze({
    Home: "Home",
    Inbox: "Inbox",
    Followers: "Followers",
    Profile: "Profile"
});

export type NavItem = keyof typeof NavItem;

export class HomeNavigation extends FASTElement {
    @observable
    public userId?: string;

    @observable
    public user?: Author | null;

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;

    @observable
    public layoutStyleClass: string = "";

    public readonly navigationItems: NavItem[] = [
        NavItem.Home,
        NavItem.Inbox,
        NavItem.Followers
    ];

    constructor() {
        super();
        this.addIcons()
    }

    public getNavigationUrl(navigationItem: NavItem): string {
        switch (navigationItem) {
            case NavItem.Inbox:
                return "/inbox/";
            case NavItem.Followers:
                return "/profile/" + this.userId + SocialApiUrls.FOLLOWERS;
            case NavItem.Profile:
                return "/profile/" + this.userId;
            default:
                return "/";
        }
    }

    public getNavigationIcon(navigationItem: string) {
        switch (navigationItem) {
            case (NavItem.Home):
                return icon({ prefix: "fas", iconName: "house" }).html
            case (NavItem.Inbox):
                return icon({ prefix: "fas", iconName: "inbox" }).html
            case (NavItem.Followers):
                return icon({ prefix: "fas", iconName: "user-group" }).html
            case (NavItem.Profile):
                return icon({ prefix: "fas", iconName: "user" }).html
        }
    }

    private addIcons() {
        library.add(faHouse, faInbox, faUserGroup, faUser);
    }
}