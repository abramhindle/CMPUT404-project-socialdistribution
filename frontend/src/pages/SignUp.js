import Headers from "../components/Headers";
import "./SignUp.css"

function SignUp() {
    return (
    <div className="SignUp">
        <Headers />
        <div class="signup-wrap">
            <form id="user_signup" action="">
                <ol class="title">Creat a new account</ol>
                <tr>
                    <ol class="text">username:</ol>
                    <td width="100%">
                        <input class="username_box" name="" id="accountName" type="text"/>
                    </td>
                </tr>

                <tr>
                    <ol class="text">email:</ol>
                    <td width="100%">
                        <input class="email_box" name="email" id="email" type="text"/>
                    </td>
                </tr>


                <tr>
                    <ol class="text">password:</ol>
                    <td width="100%">
                        <input class="password_box" name="password" id="password" type="text"/>
                    </td>
                </tr>

                <tr>
                    <ol class="text">confirm_password:</ol>
                    <td width="100%">
                        <input class="confirm_password_box" name="confirm_password" id="confirm_password" type="text"/>
                    </td>
                </tr>
        
                <button class="btn" onclick="return check(this.form);">Create account</button>


                <div id="CheckMsg" class="msg"></div>
            </form>
        </div>

    </div>
  
    );
}
export default SignUp;

  
function check(form){
    return true;
}
function register(form){
    return true;
}