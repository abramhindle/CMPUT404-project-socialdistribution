import { FASTElement, observable } from "@microsoft/fast-element";

const NavItem = Object.freeze({
    Home: "Home",
    Inbox: "Inbox",
    Friends: "Friends"
});

type NavItem = typeof NavItem[keyof typeof NavItem];

export class HomeNavigation extends FASTElement {
    @observable
    public isAuth: boolean = false;

    public readonly navigationItems = [
        NavItem.Home,
        NavItem.Inbox,
        NavItem.Friends
    ];

    public connectedCallback() {
        super.connectedCallback();
    }

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