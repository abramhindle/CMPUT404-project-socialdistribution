import { useSelector } from "react-redux";
import { useState, useEffect, useNavigate } from "react";
import { send_api, post_api, edit_api } from "../../api/post_display_api";
import { get_followers_for_author } from "../../api/follower_api";
import "./form.css";
import { useLocation } from "react-router-dom";

export default function NewPost() {
    //Get user info
    const user = useSelector((state) => state.user).id;

    const [edit, setEdit] = useState(false);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [contentType, setContentType] = useState("text/plain");
    const [body, setBody] = useState("");
    const [visibility, setVisibility] = useState("PUBLIC");
    const [unlisted, setUnlisted] = useState(false);
    const [categories, setCategories] = useState([]);
    const [id, setId] = useState("");

    const [followers, setFollowers] = useState([]);
    const [posted, setPosted] = useState(null);

    const {state} = useLocation();
    const navigate = useNavigate();

    const populateFollowers = async () => {
        await get_followers_for_author(user, setFollowers);
    }

    const sendPost = async () => {
        await send_api(followers, posted);
        navigate("/");
    }

    const submit = async (e) => {
        console.log("Submitting ...");
        let data = {"title": title,
        "description": description,
        "contentType": contentType,
        "content": body,
        "visibility": visibility,
        "unlisted": unlisted,
        "categories": categories.split(",")};

        e.preventDefault();
        if (edit) {
            console.log(user, "is attempting to edit post", id);
            await edit_api(user, id, data, setPosted);
        } else {
            console.log(user, "is attempting to post", data);
            await post_api(user, data, setPosted);
        }
    };

    const handleCheckbox = (e) => {
        //console.log(e.target.checked);
        let check = e.target.checked ? true : false;
        setUnlisted(check);
    }

    useEffect( () => {
        let data = state;
        if (data) {
            data = data.postInfo;
            setEdit(true);
            setTitle(data.title);
            setDescription(data.description);
            setContentType(data.contentType);
            setBody(data.content);
            setCategories(data.categories);
            setVisibility(data.visibility);
            console.log("id:", data.id);
            setId(data.id.split("/").pop());
        }
    }, []);


    useEffect(() => {
        //only runs once
        populateFollowers();
      }, []);

    useEffect(() => {
        //runs when object posted
        sendPost();
      }, [posted]);

    return (
        <div className="form-container">
            <form className="form" encType="multipart/form-data" method="POST">
                {edit ? <h1>Edit Text Post</h1> : <h1>New Text Post</h1>}
                <div className="form-group">
                    <label for="contentType">Content Type: </label>
                    <select value={contentType} 
                            name="contentType" 
                            className="dropdown"
                            onChange={(e) => setContentType(e.target.value)}>
                        <option
                            value="text/plain">
                        Plain Text
                        </option>
                        <option
                            value="text/markdown">
                        Markdown
                        </option>
                     </select>
                </div>
                <label>Visibility: </label>
                <select value={visibility} 
                        name="visibility" 
                        className="dropdown"
                        onChange={(e) => setVisibility(e.target.value)}
                >
                    <option
                        value="PUBLIC"
                    >
                    Public
                    </option>
                    <option
                        value="FRIENDS"
                        >
                    Friends Only
                    </option>
                </select>
                {!edit && <label>  Unlisted</label>&&
                <input
                    name="unlisted"
                    type="checkbox"
                    defaultChecked={false}
                    onChange={handleCheckbox}
                />}
                <br/>
                <div className="form-group">
                    <input
                        className="form-control"
                        placeholder="Title.."
                        name="title"
                        type="text"
                        value={title}
                        required
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <textarea 
                    className="form-control ta"
                    placeholder="Content.."
                    type="text"
                    rows="4"
                    value={body}
                    required
                    onChange={(e) => setBody(e.target.value)}
                    />
                </div>
                <div className="form-group">
                <textarea
                    className="form-control ta"
                    placeholder="Description.."
                    name="description"
                    type="text"
                    value={description}
                    required
                    onChange={(e) => setDescription(e.target.value)}
                />
                </div>
                <textarea
                    placeholder="Categories.."
                    className="form-control ta"
                    name="categories"
                    type="text"
                    value={categories}
                    required
                    onChange={(e) => setCategories(e.target.value)}
                /><br/>
                <button type="submit" className="btn" onClick={submit}>Submit</button>
            </form>
        </div>

    );
}
