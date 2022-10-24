import { FASTElement, observable } from "@microsoft/fast-element";
import { Author } from "../../../libs/api-service/SocialApiModel";

const NavItem = Object.freeze({
    Home: "Home",
    Inbox: "Inbox",
    Friends: "Friends"
});

type NavItem = typeof NavItem[keyof typeof NavItem];

export class HomeNavigation extends FASTElement {
    @observable
    public user?: Author | null;

    public readonly navigationItems = [
        NavItem.Home,
        NavItem.Inbox,
        NavItem.Friends
    ];

    public getNavigationIconUrl(navigationItem: string) {
        switch(navigationItem) {
            case(NavItem.Home):
                return require('../../../assets/images/home.png').default
            case (NavItem.Inbox):
                return require('../../../assets/images/inbox.png').default
            case (NavItem.Friends):
                return require('../../../assets/images/friends.png').default
        }
    }
}