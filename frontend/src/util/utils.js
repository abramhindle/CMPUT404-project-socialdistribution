
export default class utils {

    static getStrippedEscapedAuthorId(authorId) {
        if(authorId) {
            // copy from https://shafiqul.wordpress.com/2014/07/11/javascript-how-to-remove-http-from-url/
            authorId = authorId.replace(/^https?:\/\//,'');
            return encodeURIComponent(authorId);
        }
        throw new Error("getStrippedEscapedAuthorId invalid argument");
    }

    static unEscapeAuthorId(escapedAuthorId) {
        if(escapedAuthorId) {
            let authorId = decodeURIComponent(escapedAuthorId);
            authorId = "https://" + authorId;
            return authorId;
        }
        throw new Error("unEscapeAuthorId invalid argument");
    }

    /*
        this takes currently authenticated user and a escaped full author id as arguments
        example:
        currentAuthId: http://127.0.0.1:8000/author/163974c0-b350-4e9b-a708-b570acee826d
        escapedAuthorId: http%3A%2F%2F127.0.0.1%3A8000%2Fauthor%2F163974c0-b350-4e9b-a708-b570acee826d
        when using this to prepare the author id to send to backend,
        it should send 163974c0-b350-4e9b-a708-b570acee826d if it is a local user,
        and send the escaped id if it is a foreign author
     */
    static prepAuthorIdForRequest(currentAuthId, escapedAuthorId) {
        if(escapedAuthorId) {
            let decodedAuthorId = decodeURIComponent(escapedAuthorId);
            if (utils.getHostName(currentAuthId) === utils.getHostName(decodedAuthorId)) {
                let tmp = decodedAuthorId.split("author/")
                return tmp[1];
            } else {
                return escapedAuthorId;
            }

        }
        throw new Error("prepAuthorIdForRequest");
    }


	static getShortAuthorId(authorId){
        if(authorId) {
            let tmp = authorId.split("/author/");
            return tmp.pop();
        }
        throw new Error("getShortAuthorId invalid argument");
    }
    
    static getHostName(authorId){
        if(authorId) {
            let tmp = authorId.split("/");
            if(tmp.length === 5) {
                return tmp[2];
            } else {
                throw new Error("getHostName invalid argument");
            }
        }
        throw new Error("getHostName invalid argument");
	}
}
