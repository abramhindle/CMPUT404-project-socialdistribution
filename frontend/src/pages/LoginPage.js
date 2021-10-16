import Headers from "../components/Headers";
import "./LoginPage.css";

function LoginPage() {
  return (
    <div className="LoginPage">
      <div class="login-wrap">
        <form id="user_login" action="">
          <ol class="title">Login Page</ol>
          <tr>
            <ol class="text">username:</ol>
            <td width="100%">
              <input
                class="username_box"
                name=""
                id="accountName"
                type="text"
              />
            </td>
          </tr>

          <tr>
            <ol class="text">password:</ol>
            <td width="100%">
              <input
                class="password_box"
                name="password"
                id="password"
                type="password"
              />
            </td>
          </tr>

          <button class="btn" onclick="return check(this.form);">
            login
          </button>

          {/* <input type="button" id="register" class="register" value="sign up" onclick="return register(this.form);"/> */}
          {/* <tr>
                    <ol>sign</ol>
                    <td input type="button" id="register" class="register" value="sign up" onclick="return register(this.form);">here</td>
                </tr> */}
          <p class="new_user_text">
            new user? sign up&nbsp;
            <a class="btn_register" onclick="return register(this.form);">
              here
            </a>
          </p>

          <div id="CheckMsg" class="msg"></div>
        </form>
      </div>
    </div>
  );
}
export default LoginPage;

function check(form) {
  return true;
}
function register(form) {
  return true;
}
