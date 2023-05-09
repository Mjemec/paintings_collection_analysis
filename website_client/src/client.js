
// intellisense for jquery in vscode
/// <reference path="../node_modules/@types/jquery/index.d.ts" />

const serverUrl = "http://localhost:3000";
const imgCount = 6;

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

function showImages(timePeriodStr) {
	
	console.log("clicked " + timePeriodStr);
	list_a = [];
	for (let i = 0; i < imgCount; i++) {
		list_a.push(document.getElementById("a-" + i));
	}

	let i = 0;
	list_a.forEach(a => {
		a.setAttribute("href", serverUrl + "/img_collection/" + timePeriodStr + "/" + i);
		let img;
		for (const child of a.children) {
			if (child.tagName == "IMG")
				img = child;
		}
		// console.log(img);
		img.src = serverUrl + "/img_collection/" + timePeriodStr + "/" + i;
		i++;
	});

}


