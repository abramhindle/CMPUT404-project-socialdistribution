function addCategories(){
	var div = document.getElementById("append");
	var option = document.createElement("input");
	option.name = "categories";
	option.value = "";
	option.size = 6;
	div.appendChild(option);
}

function addImages(){
	return;
}

// not working, cant handle redirects
function submitForm(url){
	var formElement = document.querySelector("form");
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status==201) {
	       // Typical action to be performed when the document is ready:
	       var resp = request.getAllResponseHeaders();
	       alert(resp);
	       //window.location.href = "post/" +resp["id"]

	    }
    }
	request.open("POST", url);
	request.send(new FormData(formElement));
}