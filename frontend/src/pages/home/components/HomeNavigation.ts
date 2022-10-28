import { FASTElement, observable } from "@microsoft/fast-element";
import { Author } from "../../../libs/api-service/SocialApiModel";
import { LayoutType } from "../../../libs/core/PageModel";

export const NavItem = Object.freeze({
    Home: "Home",
    Inbox: "Inbox",
    Friends: "Friends",
    Profile: "Profile"
});

export type NavItem = keyof typeof NavItem;

export class HomeNavigation extends FASTElement {
    @observable
    public user?: Author | null;

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;

    @observable
    public layoutStyleClass: string = "";

    layoutTypeChanged(old: any, newval: any) {
        console.log(old, newval)
    }

    public readonly navigationItems: NavItem[] = [
        NavItem.Home,
        NavItem.Inbox,
        NavItem.Friends,
        NavItem.Profile
    ];

    public getNavigationUrl(navigationItem: NavItem): string {
        switch (navigationItem) {
            case NavItem.Inbox:
                return "/inbox/";
            case NavItem.Friends:
                return "/friends/";
            case NavItem.Profile:
                return "/profile/"
            default:
                return "/";
        }
    }

    public getNavigationIconUrl(navigationItem: string) {
        switch(navigationItem) {
            case(NavItem.Home):
                return require('../../../assets/images/home.png').default
            case (NavItem.Inbox):
                return require('../../../assets/images/inbox.png').default
            case (NavItem.Friends):
                return require('../../../assets/images/friends.png').default
            case (NavItem.Profile):
                return require('../../../assets/images/friends.png').default
        }
    }
}