
export default class utils {

    static getStripedEscapedAuthorId(authorId) {
        if(authorId) {
            // copy from https://shafiqul.wordpress.com/2014/07/11/javascript-how-to-remove-http-from-url/
            authorId = authorId.replace(/^https?:\/\//,'');
            return encodeURIComponent(authorId);
        }
        throw new Error("getStripedEscapedAuthorId");
    }


	static GetShortAuthorId(authorId){
        if(authorId) {
            let tmp = authorId.split("/author/");
            if(tmp.length === 2) {
                return tmp[1];
            } else {
                throw new Error("GetShortAuthorId invalid argument");
            }
        }
        throw new Error("GetShortAuthorId invalid argument");
	}
}
