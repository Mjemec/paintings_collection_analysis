# Paintings collection analysis

## Usage

After installing all the system dependencies, install all the python dependencies with:
```sh
pip install -r requirements.txt
```

After that, run `python main.py` to generate base images.
To run the various filters, run `python generateImages.py`.

After the images are in the `imgCollection` folder, you can now run the website.

Start the server by going into the `website_server` directory, then run `npm install` to install the dependencies. To run the server, run `node server.js`.
<br>
To run the client, head over to `website_client` and run `npm run dev`. The client should now be available [here](http://localhost:1234).

## Dependencies

For this project you will need to install the following:

* NodeJS
* Yarn
* [YoloV8 weights](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiZyNuu4Of-AhUx_rsIHW_UAuYQFnoECBQQAQ&url=https%3A%2F%2Fgithub.com%2FWongKinYiu%2Fyolov7%2Freleases%2Fdownload%2Fv0.1%2Fyolov7-w6-pose.pt&usg=AOvVaw3hJHIPPD8pI1Ft23MY1XzS)
* [YoloV7 weights](https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-w6-pose.pt)
* OpenCV
