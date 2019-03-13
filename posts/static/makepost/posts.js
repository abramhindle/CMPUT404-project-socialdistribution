function addCategories(){
	var div = document.getElementById("append");
	var option = document.createElement("input");
	option.name = "categories";
	option.value = "";
	option.size = 6;
	div.appendChild(option);
}