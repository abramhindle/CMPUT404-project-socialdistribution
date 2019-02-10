export const fetchNotes = () => {
/*
    return dispatch => {
        let headers = {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test12" + ':' + "test1")};
        return fetch("/api/dummy_post/", {headers, })
            .then(res => res.json())
            .then(notes => {
                console.log(notes, "oof")
                return dispatch({
                    type: 'FETCH_NOTES',
                    notes
                })
            })
    }
    */
    return dispatch => {
        /*
        let headers = {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
        console.log(headers);
        return fetch("/api/post/", {headers, })
            .then(res => res.json())
            .then(notes => {
                console.log(notes, "oof")
                return dispatch({
                    type: 'FETCH_NOTES',
                    notes
                })
            })
            */

        let headers = {"Content-Type": "application/json", 'Authorization': 'Basic ' + window.btoa("test1" + ':' + "test1")};
        let body = JSON.stringify({text: "test1_text_number1"});
        return fetch("/api/post/", {headers, body, method: "POST"})
        //return fetch("/api/post/", {headers, })
            .then(res => res.json())
            .then(notes => {
                console.log(notes, "oof")
                return dispatch({
                    type: 'FETCH_NOTES',
                    notes
                })
            })
    }
}

export const addNote = text => {
    return dispatch => {
        let headers = {"Content-Type": "application/json"};
        let body = JSON.stringify({username: "test1", password: "test1" });
        console.log(body);
        return fetch("/api/auth/login/", {headers, method: "POST", body})
            .then(res => res.text())
            .then(note => {
                return dispatch({
                    type: 'ADD_NOTE',
                    note
                })
            })
    }
}
export const updateNote = (index, text) => {
    return (dispatch, getState) => {

        let headers = {"Content-Type": "application/json"};
        let body = JSON.stringify({text, });
        let noteId = getState().notes[index].id;

        return fetch(`/api/dummy_post/${noteId}/`, {headers, method: "PUT", body})
            .then(res => res.text())
            .then(note => {
                return dispatch({
                    type: 'UPDATE_NOTE',
                    note,
                    index
                })
            })
    }
}

export const deleteNote = index => {
    return (dispatch, getState) => {

        let headers = {"Content-Type": "application/json"};
        let noteId = getState().notes[index].id;

        return fetch(`/api/dummy_post/${noteId}/`, {headers, method: "DELETE"})
            .then(res => {
                if (res.ok) {
                    return dispatch({
                        type: 'DELETE_NOTE',
                        index
                    })
                }
            })
    }
}