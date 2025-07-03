# EasySeg: Interactive Segmentation on WMS Imagery

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/Frontend-HTML/JS-orange.svg)](#)

EasySeg is a proof-of-concept web application that enables interactive semantic segmentation on geospatial imagery loaded from a Web Map Service (WMS). It leverages the power of Meta AI's Segment Anything Model (SAM) and performs all heavy computation on the user's own device, ensuring data privacy and utilizing modern hardware capabilities like GPUs/NPUs.

## About The Project

While individual components for web-based mapping and machine learning exist, a comprehensive, proven solution for interactive, on-device segmentation of WMS imagery has been lacking. The primary challenge lies in the complex integration of cutting-edge ML models with established geospatial data standards.

EasySeg bridges this gap by providing a seamless workflow from data ingestion to feature extraction.

### Key Objectives & Features

-   **OGC Compatibility:** Ingests imagery from any OGC-compliant WMS service.
-   **Interactive Segmentation:** Allows users to select features of interest by placing points or drawing bounding boxes directly on the map.
-   **On-Device AI:** Utilizes the Segment Anything Model (SAM) running locally in the backend, making maximum use of the user's desktop GPU/NPU for fast inference.
-   **Geospatial Export:** Converts the segmented raster masks into a vector format (GeoJSON), ready for use in any standard GIS software (like QGIS, ArcGIS).

### Tech Stack

-   **Backend:** Flask (Python)
-   **Frontend:** Plain HTML, CSS, JavaScript (using a mapping library like OpenLayers or Leaflet to handle WMS)
-   **AI Model:** [Segment Anything Model (SAM)](https://github.com/facebookresearch/segment-anything) by Meta AI
-   **Geospatial Processing:** GDAL, Rasterio, Shapely
-   **WMS Service Example:** [Bhuvan ISRO Portal](https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms)

## Getting Started

Follow these instructions to get a local copy of EasySeg up and running on your machine.

### Prerequisites

You will need the following software installed on your system:
-   [Python](https://www.python.org/downloads/) (version 3.9 or higher)
-   [Pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
-   [Git](https://git-scm.com/downloads/) (for cloning the repository)
-   It is **highly recommended** to use a virtual environment to manage dependencies.

### Installation

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/EasySeg.git
    cd EasySeg
    ```

2.  **Set up the Backend**

    a. Navigate to the backend directory and create a virtual environment:
    ```sh
    cd backend
    python -m venv venv
    ```
    Activate it:
    -   On Windows: `venv\Scripts\activate`
    -   On macOS/Linux: `source venv/bin/activate`

    b. Install the required Python packages. This includes Flask, PyTorch, and the SAM model library.
    ```sh
    pip install -r requirements.txt
    ```
    > **Note:** A typical `requirements.txt` for this project would look like this:
    > ```
    > flask
    > flask-cors
    > torch
    > torchvision
    > git+https://github.com/facebookresearch/segment-anything.git
    > opencv-python
    > numpy
    > rasterio
    > gdal
    > shapely
    > ```

    c. **Download the SAM Model Checkpoint:** The SAM model requires a pre-trained model file (a "checkpoint"). Download one of the official checkpoints from the [SAM repository](https://github.com/facebookresearch/segment-anything#model-checkpoints). The `vit_h` is the largest and most accurate, while `vit_b` is the smallest and fastest.

    **Place the downloaded `.pth` file inside the `backend/models/` directory.** (You may need to create the `models` folder).

3.  **Frontend Setup**
    The frontend is a simple `index.html` file located in the `frontend/` directory. It requires **no installation or build steps**.

## How to Run the Application

1.  **Start the Backend Server**
    Make sure you are in the `backend/` directory with your virtual environment activated. Run the Flask application:
    ```sh
    python app.py
    ```
    You should see output indicating that the server is running, typically on `http://127.0.0.1:5000`.

2.  **Launch the Frontend**
    Navigate to the `frontend/` directory and open the `index.html` file directly in your web browser (e.g., Chrome, Firefox).
    -   You can simply double-click the file.
    -   Or right-click -> "Open with" -> Your Browser.

## How It Works (Methodology)

The user workflow follows four simple steps:

1.  **Import WMS Image:** The frontend loads a map view with an imagery layer from the configured WMS service (e.g., Bhuvan). The map view allows panning and zooming.
2.  **Perform Segmentation:** The user interacts with the map by clicking on an object of interest. The coordinates of this click are sent to the Flask backend along with the current map view's bounding box.
    -   The backend fetches a high-resolution image of that bounding box from the WMS service.
    -   It loads the SAM model and performs segmentation using the user's click as an input prompt.
    -   The resulting binary mask is returned to the frontend.
3.  **Visualize and Refine:** The frontend overlays the received mask on the map, showing the user the segmented feature. The user can continue selecting other features.
4.  **Export to GeoJSON:** Once the user is satisfied, they can click an "Export" button. The backend takes all the generated masks, converts them from raster to vector polygons, georeferences them correctly, and serves them as a single GeoJSON file for the user to download.

## Conclusion

EasySeg successfully demonstrates the integration of a state-of-the-art AI model with standard geospatial services. It provides a powerful, easy-to-use tool for interactive feature extraction, proving that complex on-device computation is viable within a web-based GIS framework.

### Acknowledgments
*   **Meta AI** for the groundbreaking [Segment Anything Model](https://ai.facebook.com/blog/segment-anything-project/).
*   **NRSC/ISRO** for providing the public [Bhuvan WMS service](https://bhuvan.nrsc.gov.in/bhuvan_links.php) for demonstration.
