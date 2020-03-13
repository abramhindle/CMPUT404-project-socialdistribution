//function to show comments
//Reference: https://stackoverflow.com/questions/29321494/show-input-field-only-if-a-specific-option-is-selected/29321711
//Author: https://stackoverflow.com/users/4721273/josephus87
function displayCommentsCheck(that) {
    if (document.getElementById(that).style.display == "block") {
        document.getElementById(that).style.display = "none";
    } else {
        document.getElementById(that).style.display = "block";
    }
}

function showDropdown(that) {
	document.getElementById(that).classList.toggle("show-dropdown");
}


function confirmDelete() {
	var yes = confirm("Are you sure you want to delete this post?");
}


function simpleText() {
	var simple = document.getElementById("orange-button");
	simple.style.borderColor = "black";

	var markup = document.getElementById("blue-button");
	markup.style.borderColor = "lightgray";
}

function markupText() {
	var simple = document.getElementById("orange-button");
	simple.style.borderColor = "lightgray";

	var markup = document.getElementById("blue-button");
	markup.style.borderColor = "black";
}


