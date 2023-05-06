
// intellisense for jquery in vscode
/// <reference path="../node_modules/@types/jquery/index.d.ts" />

const serverUrl = "http://localhost:3000";

window.onload = () => {
	
	console.log("loaded");

	// var promise = getData();
	// promise.done((data, status) => {
	// 	console.log("status: " + status);
	// 	console.log(data);
	// });

};

function getFaceData() {
	return $.get(serverUrl + "/chart/faces");
};

function getData() {
	return $.get(serverUrl + "/chart/sample");
};

function showImages(timePeriodId) {
	
	let leftImageContainer = document.getElementById("leftImageContainer");
	console.log("show images of time period with id: " + timePeriodId);
	console.log(leftImageContainer);

	// remove any existing images
	leftImageContainer.replaceChildren([]);

	// create image and fill bootstrap column
	let newChild = document.createElement("img");
	newChild.style.maxHeight = "100%";
	newChild.style.maxWidth = "100%";

	// get image source from server
	newChild.setAttribute("src", serverUrl + "/time_period_examples/faces/baroque");

	leftImageContainer.appendChild(newChild);

}
