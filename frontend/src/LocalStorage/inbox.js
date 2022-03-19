export function setInboxInStorage(inbox) {
    localStorage.setItem("inbox", JSON.stringify(inbox));
}

export function getInboxFromStorage() {
    const inboxStr = localStorage.getItem("inbox");
    return JSON.parse(inboxStr);
}