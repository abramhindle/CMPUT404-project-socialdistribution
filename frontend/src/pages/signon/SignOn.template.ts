import { html, ref, repeat } from "@microsoft/fast-element";
import { logoComponent } from "../../components/logo";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { SignOn, SignOnType } from "./SignOn";

logoComponent;

const errorMessagesTemplate = html<SignOn>`
    <div>
        ${repeat(x => x.errorMessages, html<string>`
            <div class="alert alert-error">
                ${x => x}
            </div>
        `)}
    </div>
`;

const SignOnTypeTemplate = (signOnType?: SignOnType) => {
    switch (signOnType) {
        case SignOnType.Register:
            return RegisterTemplate;
        case SignOnType.Login:
            return LoginTemplate;
        case SignOnType.Logout:
            return LogoutTemplate;
        default:
            return "";
    }
}

const RegisterTemplate = html<SignOn>`
    <form ${ref("form")} @submit="${(x, c) => x.register(c.event)}" id="register-form">
        <div class="form-element">
            <fast-text-field type="text" placeholder="Display Name" name="display_name" required></fast-text-field>
        </div>
        <div class="form-element">
            <fast-text-field type="text" placeholder="Username" name="username" required></fast-text-field>
        </div>
        <div class="form-element">
            <fast-text-field type="password" placeholder="Password" name="password" required></fast-text-field>
        </div>
        <div class="form-element">
            <fast-text-field type="password" placeholder="Confirm Your Password" name="password2" required></fast-text-field>
        </div>
        <div class="form-element">
            <button id="submit">Sign Up</button>
        </div>
    </form>
`;

const LoginTemplate = html<SignOn>`
    <form ${ref("form")} @submit="${(x, c) => x.login(c.event)}" id="login-form">
        <div class="form-element">
            <fast-text-field type="text" placeholder="Username" name="username" required></fast-text-field>
        </div>
        <div class="form-element">
            <fast-text-field type="password" placeholder="Password" name="password" required></fast-text-field>
        </div>
        <div class="form-element">
            <button id="submit">Log In</button>
        </div>
    </form>
`;

const LogoutTemplate = html<SignOn>`
    <div id="login-form">
        <button @click="${(x, c) => x.logout(c.event)}" class="logout">
            Log out?
        </button>
        <a href="/">
            <button class="cancel">Cancel</button>
        </a>
    </div>
`;

export const SignOnPageTemplate = html<SignOn>`
    <h1>Find your new best friend, within 14 degrees of separation</h1>
    <div class="form-container ${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        <site-logo
            :layoutType=${x => x.layoutType}
            :layoutStyleClass=${x => LayoutHelpers.getLayoutStyle(x.layoutType)}>
        </site-logo>
        ${errorMessagesTemplate}
        ${x => SignOnTypeTemplate(x.signOnType)}
    </div>
`;