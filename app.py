

# from flask import Flask, render_template, request, send_file
# import requests
# import numpy as np
# import cv2
# import os
# import torch
# from segment_anything import sam_model_registry, SamPredictor

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static'

# # WMS Endpoint
# WMS_URL = "https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms"

# # SAM model setup
# sam_checkpoint = "sam_vit_b_01ec64.pth"
# model_type = "vit_b"
# device = "cpu"
# sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
# sam.to(device=device)
# predictor = SamPredictor(sam)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     masked_region_image = None
#     if request.method == "POST":
#         bbox = request.form.get("bbox")
#         layer = request.form.get("layer")
#         input_box = request.form.get("input_box")  # Bounding box for SAM processing

#         # WMS parameters
#         params = {
#             "SERVICE": "WMS",
#             "VERSION": "1.3.0",
#             "REQUEST": "GetMap",
#             "LAYERS": layer,
#             "STYLES": "",
#             "CRS": "EPSG:4326",
#             "BBOX": bbox,
#             "WIDTH": 512,
#             "HEIGHT": 512,
#             "FORMAT": "image/png",
#         }

#         # Fetch the WMS image
#         response = requests.get(WMS_URL, params=params)
#         if response.status_code == 200:
#             # Save the fetched WMS image
#             image_path = os.path.join(app.config['UPLOAD_FOLDER'], "map.png")
#             with open(image_path, "wb") as file:
#                 file.write(response.content)

#             # Process the image using SAM if input_box is provided
#             if input_box:
#                 try:
#                     # Convert input_box from string to numpy array
#                     input_box = np.array(list(map(int, input_box.split(','))))

#                     # Load and prepare the image for SAM
#                     image = cv2.imread(image_path)
#                     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#                     predictor.set_image(image)

#                     # Perform segmentation using SAM
#                     masks, _, _ = predictor.predict(
#                         point_coords=None,
#                         point_labels=None,
#                         box=input_box[None, :],
#                         multimask_output=False,
#                     )

#                     # Create an image showing only the masked region
#                     masked_region = extract_masked_region(image, masks[0])
#                     masked_region_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "masked_region.png")
#                     cv2.imwrite(masked_region_image_path, cv2.cvtColor(masked_region, cv2.COLOR_RGB2BGR))
#                     masked_region_image = "static/masked_region.png"
#                 except Exception as e:
#                     return f"Error during SAM processing: {str(e)}"

#             return render_template("index.html", image="static/map.png", masked_region=masked_region_image)
#         else:
#             return f"Error: {response.status_code} - {response.text}"

#     return render_template("index.html", image=None, masked_region=None)

# @app.route("/download")
# def download():
#     return send_file("static/map.png", as_attachment=True)

# def extract_masked_region(image, mask):
#     """
#     Extracts and returns only the masked region of the image.
#     The non-masked areas will have a white background.
#     """
#     mask_bool = mask.astype(bool)

#     # Create a new image with white background
#     masked_region = np.ones_like(image) * 255

#     # Copy the original colors only for the masked region
#     masked_region[mask_bool] = image[mask_bool]

#     return masked_region


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, send_file, jsonify
import requests
import numpy as np
import cv2
import os
import torch
import json
from shapely.geometry import Polygon, mapping
from segment_anything import sam_model_registry, SamPredictor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# WMS Endpoint
WMS_URL = "https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms"

# SAM model setup
sam_checkpoint = "sam_vit_b_01ec64.pth"
model_type = "vit_b"
device = "cpu"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)

@app.route("/", methods=["GET", "POST"])
def index():
    masked_region_image = None
    geojson_file = None
    if request.method == "POST":
        bbox = request.form.get("bbox")
        layer = request.form.get("layer")
        input_box = request.form.get("input_box")  # Bounding box for SAM processing

        # WMS parameters
        params = {
            "SERVICE": "WMS",
            "VERSION": "1.3.0",
            "REQUEST": "GetMap",
            "LAYERS": layer,
            "STYLES": "",
            "CRS": "EPSG:4326",
            "BBOX": bbox,
            "WIDTH": 512,
            "HEIGHT": 512,
            "FORMAT": "image/png",
        }

        # Fetch the WMS image
        response = requests.get(WMS_URL, params=params)
        if response.status_code == 200:
            # Save the fetched WMS image
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], "map.png")
            with open(image_path, "wb") as file:
                file.write(response.content)

            # Process the image using SAM if input_box is provided
            if input_box:
                try:
                    # Convert input_box from string to numpy array
                    input_box = np.array(list(map(int, input_box.split(','))))

                    # Load and prepare the image for SAM
                    image = cv2.imread(image_path)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    predictor.set_image(image)

                    # Perform segmentation using SAM
                    masks, _, _ = predictor.predict(
                        point_coords=None,
                        point_labels=None,
                        box=input_box[None, :],
                        multimask_output=False,
                    )

                    # Create an image showing only the masked region
                    masked_region = extract_masked_region(image, masks[0])
                    masked_region_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "masked_region.png")
                    cv2.imwrite(masked_region_image_path, cv2.cvtColor(masked_region, cv2.COLOR_RGB2BGR))
                    masked_region_image = "static/masked_region.png"

                    # Generate GeoJSON
                    geojson_data = generate_geojson(masks[0], bbox, params["WIDTH"], params["HEIGHT"])
                    geojson_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "masked_region.geojson")
                    with open(geojson_file_path, "w") as file:
                        json.dump(geojson_data, file)
                    geojson_file = "static/masked_region.geojson"

                except Exception as e:
                    return f"Error during SAM processing: {str(e)}"

            return render_template("index.html", image="static/map.png", masked_region=masked_region_image, geojson_file=geojson_file)
        else:
            return f"Error: {response.status_code} - {response.text}"

    return render_template("index.html", image=None, masked_region=None, geojson_file=None)

@app.route("/download_geojson")
def download_geojson():
    return send_file("static/masked_region.geojson", as_attachment=True)

def extract_masked_region(image, mask):
    """
    Extracts and returns only the masked region of the image.
    The non-masked areas will have a white background.
    """
    mask_bool = mask.astype(bool)

    # Create a new image with white background
    masked_region = np.ones_like(image) * 255

    # Copy the original colors only for the masked region
    masked_region[mask_bool] = image[mask_bool]

    return masked_region

def generate_geojson(mask, bbox, width, height):
    """
    Converts the binary mask into a GeoJSON object.
    """
    # Convert bbox to float and calculate resolution
    bbox = list(map(float, bbox.split(',')))
    x_res = (bbox[2] - bbox[0]) / width
    y_res = (bbox[3] - bbox[1]) / height

    # Find contours of the mask
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    polygons = []

    for contour in contours:
        coords = []
        for point in contour:
            x_pixel, y_pixel = point[0]
            x_coord = bbox[0] + x_pixel * x_res
            y_coord = bbox[3] - y_pixel * y_res  # Invert y-axis for geospatial coordinates
            coords.append((x_coord, y_coord))
        polygons.append(coords)

    # Create GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    for polygon in polygons:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon]
            },
            "properties": {}
        }
        geojson["features"].append(feature)

    return geojson

if __name__ == "__main__":
    app.run(debug=True)
