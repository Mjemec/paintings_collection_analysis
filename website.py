
from flask import Flask, render_template, send_file, request
import os
import re
import json

img_dir = "./img"
tag_dir = "./img"

app = Flask(__name__)

@app.route('/')
def index():
	return 'go to /images'

@app.route('/image')
def get_image():
	filePath = request.args.get('filePath')
	return send_file(filePath, mimetype='image/jpg')

@app.route('/images')
def indexImages():
	selected_image = request.args.get("image")
	if selected_image is None:
		sidebarContent = getSidebarContent()
		mainContent = "<p>Main content</p>"
		return render_template("website.html", sidebarContent=sidebarContent, mainContent=mainContent)
	else:
		sidebarContent = getSidebarContent()
		mainContent = getMainContent(selected_image) # "<p>Main content</p>"
		return render_template("website.html", sidebarContent=sidebarContent, mainContent=mainContent)

def getMainContent(selected_image: str) -> str:

	mainContent = ""
	mainContent +=	"<div class=\"imageContainer\">"
	mainContent +=		"<img src=\"" + "/image?filePath=" + img_dir + "/" + selected_image + "\" alt=\"neki\">"
	mainContent +=	"</div>"

	details = getImageDetails(selected_image)


	mainContent +=	"<div class=\"tablesContainer\" align=\"center\">"
	mainContent +=		"<div class=\"colorDetails\" align=\"center\">"
	mainContent +=	f"""	<table>
								<tr>
									<th>Color</th>
									<th>Mean</th>
									<th>Standard deviation</th>
								</tr>
								<tr>
									<td>Color 0</td>
									<td>{details["color_0_mean"]}</td>
									<td>{details["color_0_std"]}</td>
								</tr>
								<tr>
									<td>Color 1</td>
									<td>{details["color_1_mean"]}</td>
									<td>{details["color_1_std"]}</td>
								</tr>
								<tr>
									<td>Color 2</td>
									<td>{details["color_2_mean"]}</td>
									<td>{details["color_2_std"]}</td>
								</tr>
							</table>
						"""
	mainContent +=		"</div>"
	mainContent +=		"<div class=\"otherDetails\" align=\"center\">"
	mainContent +=	f"""	<table>
								<tr>
									<th>Feature</th>
									<th>Count</th>
								</tr>
								<tr>
									<td>Lines</td>
									<td>{details["line_count"]}</td>
								</tr>
								<tr>
									<td>Faces</td>
									<td>{details["face_count"]}</td>
								</tr>
								<tr>
									<td>People</td>
									<td>{details["people_count"]}</td>
								</tr>
								<tr>
									<td>Contours</td>
									<td>{details["contour_count"]}</td>
								</tr>
							</table>
						"""
	mainContent +=		"</div>"
	mainContent +=	"</div>"
	return mainContent

def getImageDetails(selected_image: str):
	jsonFileName = tag_dir + "/" + re.sub("\.jpg$", ".json", selected_image)
	print(jsonFileName)
	return json.load(open(jsonFileName))

def getSidebarContent() -> str:
	sidebarContent = ""
	for imageFile in getImageNames():
		sidebarContent += "<a href=\"/images?image=" + imageFile + "\">" + imageFile + "</a>"
	return sidebarContent

def getImageNames() -> list[str]:
	files = os.listdir(img_dir)
	imageFiles = list(filter(lambda fileName: re.search("\.jpg$", fileName), files))
	return imageFiles

def runWebapp():
	app.run(debug=True)

if __name__ == '__main__':
	runWebapp()
