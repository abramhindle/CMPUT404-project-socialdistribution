import { html, ref, repeat } from "@microsoft/fast-element";
import { SignOn } from "./SignOn";

const errorMessagesTemplate = html<SignOn>`
    <div>
        ${repeat(x => x.errorMessages!, html<string>`
            <div class="alert alert-error">
                ${x => x}
            </div>
        `)}
    </div>
`;

export const SignOnPageTemplate = html<SignOn>`
    ${errorMessagesTemplate}
    <form ${ref("form")} @submit="${(x, c) => x.register(c.event)}" id="register-form" enctype="application/x-www-form-urlencoded">
        <div class="form-element">
            <label for="accountType">Select an account type</label>
            <select name="accountType" form="register-form" class="form-control">
                <option value="Student">Student</option>
                <option value="Instructor">Instructor</option>
            </select>
        </div>
        <div class="form-element">
            <label for="firstname">Enter your first name (alphabetic characters only):</label>
            <input class="form-control" type="text" name="display_name" placeholder="First Name..."
                required>
        </div>
        <div class="form-element">
            <label for="lastname">Enter your last name (alphabetic chracters only):</label>
            <input class="form-control" type="text" name="lastname" placeholder="Last Name..." required>
        </div>
        <div class="form-element">
            <label for="username">Enter your username (More than 6 characters, no special characters or spaces):</label>
            <input class="form-control" type="text" name="username" placeholder="Username..."required minlength="6">
        </div>
        <div class="form-element">
            <!--6 or more characters-->
            <label for="password1">Enter your password (8 or more characters, no whitespace):</label>
            <input type="password" class="form-control" name="password"
                placeholder="Password... (8 or more characters, no whitespace)" required minlength="8">
        </div>
        <div class="form-element">
            <!--6 or more characters-->
            <label for="password2">Confirm your password:</label>
            <input class="form-control" type="password" name="password2" placeholder="Confirm your Password..." required minlength="8">
        </div>
        <div class="form-element">
            <button id="submit">Register</button>
        </div>
    </form>
`;