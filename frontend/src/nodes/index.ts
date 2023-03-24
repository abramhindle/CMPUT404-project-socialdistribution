import API from "./api";
import NodeManager from "./node_manager";

const LocalNode = new API(process.env.API_URL || 'http://localhost:8000/services', {
    auth:{
        username: 'tkuye',
        password: 'Ayodeji31#'
    },
    headers:{
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
}, 'local');

const RemoteNode = new API('https://sd7-api.herokuapp.com/api', {
    auth:{
        username:'node01',
        password: 'P*ssw0rd!'
    }, 
    headers:{
        'Content-Type': 'application/json',
        'Accept': 'application/json',
         'Access-Control-Allow-Credentials':true
    }
}, 'remote');

const nodeManager = new NodeManager({
    local: LocalNode,
    remote: RemoteNode
});

export default nodeManager;