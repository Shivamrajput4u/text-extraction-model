document.addEventListener('DOMContentLoaded', function() {
    
    // Get all the elements we need, with checks
    const fileUpload = document.getElementById('file-upload');
    const fileNameSpan = document.getElementById('file-name');
    const ocrForm = document.getElementById('ocr-form');
    const loader = document.getElementById('loader');
    const uploadArea = document.getElementById('upload-area');

    // --- Function to update the file name display ---
    function updateFileName(inputElement) {
        if (fileNameSpan) { // Check if the span exists
             if (inputElement.files && inputElement.files.length > 0) {
                fileNameSpan.textContent = inputElement.files[0].name;
                fileNameSpan.classList.remove('text-gray-600'); // Use default text color
                fileNameSpan.classList.add('text-blue-700'); // Make it blue to show selection
             } else {
                fileNameSpan.textContent = 'No file chosen';
                fileNameSpan.classList.remove('text-blue-700');
                fileNameSpan.classList.add('text-gray-600'); // Back to muted color
             }
        } else {
            console.error("File name display element ('file-name') not found.");
        }
    }

    // 1. Update file name when a file is chosen via CLICK
    if (fileUpload) {
        fileUpload.addEventListener('change', function() {
            // 'this' refers to the fileUpload element here
            updateFileName(this); 
        });
    } else {
        console.error("File input element ('file-upload') not found.");
    }

    // 2. Show the loader when the form is submitted
    if (ocrForm && loader) {
        ocrForm.addEventListener('submit', function() {
            // Check loader exists before trying to show it
            if(loader) { 
                loader.style.display = 'flex';
            } else {
                console.error("Loader element ('loader') not found on submit.");
            }
        });
    } else {
        if (!ocrForm) console.error("Form element ('ocr-form') not found.");
        if (!loader) console.error("Loader element ('loader') not found.");
    }

    // 3. Drag & Drop functionality
    if (uploadArea && fileUpload) { 
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false); // Prevent browser opening file
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
        });

        // Remove highlight when item leaves drop zone
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
        });

        // Handle dropped files
        uploadArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            let dt = e.dataTransfer;
            let files = dt.files;

            if (files.length > 0) {
                 // Assign dropped files to the hidden input
                 fileUpload.files = files; 
                 // Manually trigger the 'change' event on the file input
                 // so our other listener updates the file name display
                 const changeEvent = new Event('change', { bubbles: true }); 
                 fileUpload.dispatchEvent(changeEvent);
            }
        }
        
        // Make the whole area clickable to trigger the hidden file input
        uploadArea.addEventListener('click', () => {
            fileUpload.click();
        });

    } else {
         if (!uploadArea) console.error("Upload area element ('upload-area') not found.");
         // fileUpload check already done above
    }
});

