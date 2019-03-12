function addCategories(){
	var div = document.getElementById("append");
	var option = document.createElement("input");
	option.name = "categories";
	option.value = "";
	div.appendChild(option);
}