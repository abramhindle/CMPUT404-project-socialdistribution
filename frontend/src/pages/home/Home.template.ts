import { html } from "@microsoft/fast-element";
import { templateComponent } from "../../components/templateComponent";
import { homeNavigation } from "./components";
import { Home } from "./Home";

templateComponent;
homeNavigation;

const navigationTemplate = html<Home>`
    <home-navigation
        :isAuth=${x => true}>
    </home-navigation>
`;

export const HomePageTemplate = html<Home>`
    ${navigationTemplate}
    <main class="feed-container">
    </main>
`;