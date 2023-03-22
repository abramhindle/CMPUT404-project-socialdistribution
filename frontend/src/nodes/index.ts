import API from "./api";
import NodeManager from "./node_manager";

const LocalNode = new API(process.env.API_URL || 'http://localhost:8000/services', undefined, 'local');
const RemoteNode = new API('https://sd7-api.herokuapp.com/api', undefined, 'remote');


const nodeManager = new NodeManager({
    local: LocalNode,
    remote: RemoteNode
});

export default nodeManager;