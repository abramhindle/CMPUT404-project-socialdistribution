import Headers from "../components/Headers";
import "./SignUpPage.css"

function SignUpPage() {
    return (
    <div className="SignUpPage">
        <Headers />
        <div class="sign_up_wrap">
            <form id="user_signup" action="">
                <ol class="sign_up_title">Creat a new account</ol>
                <tr>
                    <ol class="sign_up_text">username:</ol>
                    <td width="100%">
                        <input class="sign_up_box" name="" id="accountName" type="text"/>
                    </td>
                </tr>

                <tr>
                    <ol class="sign_up_text">email:</ol>
                    <td width="100%">
                        <input class="sign_up_box" name="email" id="email" type="text"/>
                    </td>
                </tr>


                <tr>
                    <ol class="sign_up_text">password:</ol>
                    <td width="100%">
                        <input class="sign_up_box" name="password" id="password" type="text"/>
                    </td>
                </tr>

                <tr>
                    <ol class="sign_up_text">confirm_password:</ol>
                    <td width="100%">
                        <input class="sign_up_box" name="confirm_password" id="confirm_password" type="text"/>
                    </td>
                </tr>
        
                <button class="sign_up_btn" onclick="return check(this.form);">Create account</button>


                <div id="CheckMsg" class="sign_up_msg"></div>
            </form>
        </div>

    </div>
  
    );
}
export default SignUpPage;

  
function check(form){
    return true;
}
function register(form){
    return true;
}