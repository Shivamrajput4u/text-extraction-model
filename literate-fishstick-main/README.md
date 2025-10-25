# Indic Book Cover OCR Project

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![Ultralytics YOLO](https://img.shields.io/badge/YOLO-Ultralytics-blue?style=for-the-badge)](https://ultralytics.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

This Django web application detects and recognizes text from Indic language book cover images using a combination of a YOLO model for text detection and a fine-tuned CRNN model for text recognition.

## Features

* *Text Detection:* Uses a YOLO model (fine-tuned on the IIIT-ILST dataset) to locate text regions on book cover images.
* *Text Recognition:* Employs a CRNN model (fine-tuned on the Mozhi dataset) to recognize the text within the detected regions.
* *Multi-Language Support:* Designed to work with various Indic scripts and English.
* *Language Identification:* Identifies the language of the recognized text using langdetect.
* *Web Interface:* Simple, responsive frontend built with Tailwind CSS for uploading images and viewing results.
* *CPU Deployment:* Runs entirely on CPU, suitable for deployment in environments like GitHub Codespaces.

## Tech Stack

* *Backend:* Django
* *Frontend:* HTML, Tailwind CSS (via CDN), Vanilla JavaScript
* *Machine Learning:*
    * PyTorch (for model loading and inference)
    * Ultralytics (for YOLO model interaction)
    * CRNN (custom model architecture for OCR)
* *Language Detection:* langdetect
* *Deployment Environment:* GitHub Codespaces (CPU-only)

## Project Structure


.
├── .devcontainer/        # Codespace configuration
├── book_ocr_project/     # Django project settings
├── ocr_app/              # Main Django app
│   ├── models/           # Contains .pt model files and vocabulary.json
│   ├── static/           # Contains CSS/JS (if not embedded)
│   ├── templates/        # Contains index.html
│   ├── ocr_utils.py      # Core ML inference logic
│   └── views.py          # Django view handling requests
├── manage.py             # Django management script
├── README.md             # This file
└── requirements.txt      # Python dependencies

## Setup in a New Codespace

1.  *Clone the Repository:*
    bash
    git clone [https://github.com/Shivamrajput4u/LITERATE-FISHSTICK.git](https://github.com/Shivamrajput4u/LITERATE-FISHSTICK.git)
    cd LITERATE-FISHSTICK
    


    

2.  *Run the Setup Script:* This script installs OS dependencies, downloads LFS models, installs Python packages, and runs migrations.
    bash
    bash .devcontainer/post-create-command.sh
    
    *If the post-create-command.sh isn't present or executable, run these manually:*
    bash
    # Install OS library for OpenCV
    sudo apt-get update && sudo apt-get install -y libgl1

    # Download LFS models
    git lfs install
    git lfs pull

    # Install Python packages
    pip install -r requirements.txt

    # Run migrations
    python manage.py migrate
    

3.  *Run the Django Server:*
    bash
    python manage.py runserver 0.0.0.0:8000
    

4.  Click the "Open in Browser" notification in VS Code to view the application.

## How it Works

1.  User uploads an image via the web interface.
2.  The Django views.py receives the image.
3.  ocr_utils.py is called:
    * The image is loaded using PIL.
    * The YOLO model runs inference to detect bounding boxes around text.
    * For each bounding box:
        * The corresponding image region is cropped.
        * The cropped image is preprocessed (resized, grayscaled, normalized).
        * The CRNN model runs inference on the preprocessed crop.
        * The raw CRNN output is decoded into text using CTC greedy decoding and vocabulary.json.
        * langdetect identifies the language of the recognized text.
    * The results (cropped images as base64, recognized text, language tags) are returned.
4.  The Django view renders the index.html template, displaying the original image and the results.

## Model Information

* *Text Detector (YOLO):* Trained on the IIIT-ILST dataset. Model file: ocr_app/models/yolo_text_detector.pt.
* *Text Recognizer (CRNN):* Trained on the Mozhi dataset (subsampled). Model file: ocr_app/models/crnn_ocr_model.pt. Vocabulary: ocr_app/models/vocabulary.json.

## Developed By

* Kumar Shivam

