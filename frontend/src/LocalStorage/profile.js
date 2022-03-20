export function setAuthorInStorage(author) {
    localStorage.setItem("author", JSON.stringify(author));
}

export function getAuthorFromStorage() {
    const authorStr = localStorage.getItem("author");
    return JSON.parse(authorStr);
}