import jsCookies from "js-cookies";
import React, { useContext, useState } from "react";
import authorService from "../services/author";
import { UserContext } from '../UserContext';

const Profile = () => {
    const { user } = useContext(UserContext);
    const [ displayName, setDisplayName ] = useState("")
    const [ profileImage, setProfileImage ] = useState("")

    const handleProfileChange = async (event) => {
    try {
        // get self object
        const response = await authorService.getAuthor(user.id);
        const author = response.data;
        console.log(author)
        author.displayName = displayName;
        author.profileImage = profileImage;

        console.log(author)

        console.log(await authorService.updateAuthor(jsCookies.getItem("csrftoken"), user.id, author));
        } catch (e) {
       setDisplayName("");
        setProfileImage("");
        } 
    }


    return (
        <div>
            <p>Display Name: { user.displayName }</p>
            <p>Profile Image Link: { user.profilePicture }</p>
        <label>
            new display name: 
            <input 
            type="text"
            onChange={(e) => {setDisplayName(e.target.value)}}
            >
            </input>
        </label>

        <label>
            new profile image link: 
            <input 
            type="text"
            onChange={(e) => {setProfileImage(e.target.value)}}
            >
            </input>
        </label>
        <button onClick={handleProfileChange}>submi</button>
        </div>
    )
}

export default Profile;