# EasySeg: Interactive Segmentation on WMS Imagery with React & Flask

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2-green.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EasySeg is a web application that enables interactive semantic segmentation on geospatial imagery loaded from a Web Map Service (WMS). It leverages the power of Meta AI's Segment Anything Model (SAM) and performs all heavy computation on the user's own device, ensuring data privacy and utilizing modern hardware capabilities like GPUs/NPUs.

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
-   **Frontend:** React
-   **AI Model:** [Segment Anything Model (SAM)](https://github.com/facebookresearch/segment-anything) by Meta AI
-   **Geospatial Processing:** GDAL, Rasterio, Shapely
-   **WMS Service Example:** [Bhuvan ISRO Portal](https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms)

## Getting Started

Follow these instructions to get a local copy of EasySeg up and running on your machine.

### Prerequisites

You will need the following software installed on your system:
-   [Python](https://www.python.org/downloads/) (version 3.9 or higher)
-   [Pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
-   [Node.js](https://nodejs.org/) (version 16 or higher, which includes `npm`)
-   [Git](https://git-scm.com/downloads/) (for cloning the repository)
-   It is **highly recommended** to use a Python virtual environment.

### Installation

The project is structured into a `frontend` (React) and a `backend` (Flask) directory. You will need to install dependencies for both.

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/EasySeg.git
    cd EasySeg
    ```

2.  **Set up the Backend (Flask)**

    a. Navigate to the backend directory and create a virtual environment:
    ```sh
    cd backend
    python -m venv venv
    ```
    Activate it:
    -   On Windows: `venv\Scripts\activate`
    -   On macOS/Linux: `source venv/bin/activate`

    b. Install the required Python packages from `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

    c. **Download the SAM Model Checkpoint:** The SAM model requires a pre-trained model file. Download one of the official checkpoints from the [SAM repository](https://github.com/facebookresearch/segment-anything#model-checkpoints). We recommend `vit_b.pth` for a balance of speed and performance.

    **Place the downloaded `.pth` file inside the `backend/models/` directory.** (You may need to create the `models` folder).

3.  **Set up the Frontend (React)**

    a. In a new terminal, navigate to the frontend directory:
    ```sh
    cd frontend  # from the root EasySeg directory
    ```

    b. Install the Node.js dependencies:
    ```sh
    npm install
    ```

## How to Run the Application

You need to run the backend and frontend servers simultaneously in two separate terminals.

1.  **Start the Backend Server (Terminal 1)**
    -   Navigate to the `backend/` directory.
    -   Make sure your Python virtual environment is activated (`source venv/bin/activate` or `venv\Scripts\activate`).
    -   Run the Flask application:
    ```sh
    python app.py
    ```
    The backend server will start, typically on `http://127.0.0.1:5000`.

2.  **Start the Frontend Server (Terminal 2)**
    -   Navigate to the `frontend/` directory.
    -   Run the React development server:
    ```sh
    npm start
    ```
    This will automatically open the EasySeg application in your default web browser, usually at `http://localhost:3000`. The React app is configured to communicate with the backend server running on port 5000.

## How It Works (Methodology)

The user workflow follows four simple steps:

1.  **Import WMS Image:** The React frontend loads an interactive map (e.g., using Leaflet or OpenLayers) with an imagery layer from the configured WMS service.
2.  **Perform Segmentation:** The user interacts with the map by clicking on an object. The coordinates and current map bounds are sent to the Flask backend. The backend fetches the corresponding image, runs the SAM model, and returns the resulting mask.
3.  **Visualize and Refine:** The React frontend receives the mask and overlays it on the map. The user can continue selecting features.
4.  **Export to GeoJSON:** The user clicks an "Export" button. The backend processes all generated masks, converts them to georeferenced vector polygons, and provides a single GeoJSON file for download.

## Conclusion

EasySeg successfully demonstrates the integration of a state-of-the-art AI model with standard geospatial services in a modern web stack. It provides a powerful, easy-to-use tool for interactive feature extraction, proving that complex on-device computation is viable within a web-based GIS framework.

### Acknowledgments
*   **Meta AI** for the groundbreaking [Segment Anything Model](https://ai.facebook.com/blog/segment-anything-project/).
*   **NRSC/ISRO** for providing the public [Bhuvan WMS service](https://bhuvan.nrsc.gov.in/bhuvan_links.php) for demonstration.
