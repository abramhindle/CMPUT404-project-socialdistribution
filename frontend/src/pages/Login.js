import Headers from "../components/Headers";

function Login() {
    return (
    <div className="Login">
        <Headers />
        <div class="login-wrap">
            <form id="user_login" action="">
                <h3>Login page</h3>
                <input class="name" name="" id="accountName" type="text" placeholder="please enter your username"/>
                <input class="code" name="password" id="password" type="password" placeholder="please enter your password"/>
                <div class="btn">
                    <input type="button" id="submit" class="submit" value="login" onclick="return check(this.form);"/>
                    <input type="reset" id="reset" class="reset" value="reset"/>
                </div>
                <div id="CheckMsg" class="msg"></div>
            </form>
        </div>

    </div>
  
    );
}
export default Login;

  
function check(form){
    return true;
}