import Headers from "./Headers";
import "./HomePost.css"

function HomePost() {
    return (
        <div class="HomePost">
            <div class="tweet">
            <div class="tweet__column avatar">
                <img class="avatar__image" src="image.png" />
            </div>
            <div class="tweet__column tweet__main">
                <div class="tweet__main__header">
                    <div class="tweet__main__header__item tweet__main__header__item--name">
                        BlahX
                    </div>
                    <div class="tweet__main__header__item tweet__main__header__item--handle">
                        @blahx
                    </div>
                    <div class="tweet__main__header__item tweet__main__header__item--duration">
                        7h
                    </div>
                </div>
                <div class="tweet__main__message">
                    Blah blah blah Blah blah blah<br />
                    Blah blah blah 
                </div>
                <div class="tweet__footer">
                    <div class="tweet__footer__stats">
                        <img class="tweet__icon tweet__footer__stats__item" src="http://educative.io/udata/nWjylg5XloB/footer_icon.svg" />
                        <div class="tweet__footer__stats__item">
                            likes: 10
                        </div>
                    </div>
                    <div class="tweet__footer__stats">
                        <img class="tweet__icon tweet__footer__stats__item" src="http://educative.io/udata/nWjylg5XloB/footer_icon.svg" />
                        <div class="tweet__footer__stats__item">
                            comments: 900
                        </div>
                    </div>
                </div>
            </div>
            <div class="tweet__menu">
                <img class="tweet__icon tweet__menu__icon" src="http://educative.io/udata/w66j6pMjng6/down_icon.svg"/>
            </div>
            </div>
        </div>
  
    );
}
export default HomePost;

  