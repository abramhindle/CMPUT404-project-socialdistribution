import React, { useState } from "react";
import { Button, Container, Input, Panel, InputGroup } from 'rsuite';
import EyeIcon from '@rsuite/icons/legacy/Eye';
import EyeSlashIcon from '@rsuite/icons/legacy/EyeSlash';
import image from '../assets/socially_distributed.jpg'


function SIGN_IN(){
    // const [username, set_username] =  useState("")
    // const [password, set_password] = useState("")
    const [visible, setVisible] = React.useState(false);

    const handleChange = () => {
      setVisible(!visible);
    };

    const url = 'http://localhost:3000' + '/socially_distributed'

    return (
        <div>
            <Panel header="Login" shaded style={{width: "50%", margin:"auto", textAlign:"center" }}>
                <Input placeholder="username" style={{width: 300, margin: 10}}/>
                <InputGroup inside style={{width: 300, margin:10}}>
                    <Input placeholder="password" type={visible ? 'text' : 'password'} />
                    <InputGroup.Button onClick={handleChange}>
                        {visible ? <EyeIcon /> : <EyeSlashIcon />}
                    </InputGroup.Button>
                </InputGroup>
                <Button apperance="Primary" block style={{width: 300, margin: 10}}>Login</Button>
            </Panel>
        </div>
    )
}

export default SIGN_IN
