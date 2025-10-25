from django.shortcuts import render
from .ocr_utils import run_prediction
import base64
from PIL import Image
import io

def index(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Pass the uploaded file to the prediction function
        results = run_prediction(image_file)
        
        # Also, get a base64 version of the *original* uploaded image
        # This is just to show the user what they uploaded
        img_bytes = image_file.read()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        
        context['results'] = results
        context['original_image'] = img_b64

    return render(request, 'index.html', context)
