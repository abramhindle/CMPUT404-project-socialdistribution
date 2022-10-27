import { html } from "@microsoft/fast-element";
import { templateComponent } from "../../components/templateComponent";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { homeNavigation } from "./components";
import { Home } from "./Home";

templateComponent;
homeNavigation;

const navigationTemplate = html<Home>`
    <home-navigation
        :user=${x => x.user}
        :layoutType=${x => x.layoutType}
        :layoutStyleClass=${x => LayoutHelpers.getLayoutStyle(x.layoutType)}
        :className="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
    </home-navigation>
`;

export const HomePageTemplate = html<Home>`
    ${navigationTemplate}
    <main class="feed-container ${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
    </main>
`;