import "./posts.css"

export default function PlainPost() {
    return (
        <div className="message">
            <div className="from">
                {/*PLACEHOLDER*/}
                <img alt="author" src="http://coolbears.ca/coolbearspython-color-small.png"></img>
            </div>
            <div className="post">
                Here is some post content
            </div>
        </div>

    );
}