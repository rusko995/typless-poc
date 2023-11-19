// TODO - make this nicer with controller.js and functions.js files

function processFile() {
    const fileInput = document.getElementById('fileInput');
    const processButton = document.getElementById('processButton');
    const imputProblem = document.getElementById('imputProblem');
    const dropAreaText = document.getElementById('dropAreaText');
    const saveButton = document.getElementById('saveButton');

    const file = fileInput.files[0];

    processButton.disabled = true;
    processButton.textContent = 'Processing...';
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:5000/process', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error processing data');
            }
            return response.json();
        })
        .then(data => {
            displayExtractedFields(data["data"]["extracted_fields"]);
            saveButton.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            imputProblem.style.display = 'block';
            dropAreaText.textContent = 'Drag file here or click to choose';
            processButton.style.display = 'none';
        })
        .finally(() => {
            processButton.disabled = false;
            processButton.textContent = 'PROCESS';
        });
    } else {
        console.error('No file selected.');
        processButton.style.display = 'none';
        dropAreaText.textContent = 'Drag file here or click to choose';
        processButton.disabled = false;
        processButton.textContent = 'PROCESS';
    }
}

function displayExtractedFields(extractedFields) {
    const displayDiv = document.getElementById('extractedFieldsDisplay');
    displayDiv.innerHTML = '';
    const ul = document.createElement('ul');

    for (const field of extractedFields) {
        const li = document.createElement('li');
        li.textContent = `${field.name}: ${field.values[0].value}`;
        ul.appendChild(li);
    }

    displayDiv.appendChild(ul);
}

function saveData() {
    const extractedFields = getExtractedFields();
    const successfullySaved = document.getElementById('successfullySaved');
    const savingFailed = document.getElementById('savingFailed');
    const dropAreaText = document.getElementById('dropAreaText');
    const processButton = document.getElementById('processButton');
    const extractedFieldsDisplay = document.getElementById('extractedFieldsDisplay');
    const saveButton = document.getElementById('saveButton');

    if (extractedFields) {
        fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ extractedFields }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error saving data');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data saved:', data);
            successfullySaved.style.display = 'block';
        })
        .catch(error => {
            savingFailed.style.display = 'block';
            console.error('Error saving data:', error);
        });
    } else {
        console.error('No extracted data to save.');
    }

    dropAreaText.textContent = 'Drag file here or click to choose';
    processButton.style.display = 'none';
    saveButton.style.display = 'none';
    extractedFieldsDisplay.innerHTML = '';
}

function getExtractedFields() {
    const ul = document.querySelector('#extractedFieldsDisplay ul');
    if (ul) {
        const extractedFields = {};
        
        // Iterate through the list items and populate the object
        Array.from(ul.children).forEach(li => {
            const [name, value] = li.textContent.split(': ');
            extractedFields[name] = value;
        });

        return extractedFields;
    }
    return null;
}

function handleFileSelection() {
    const fileInput = document.getElementById('fileInput');
    const processButton = document.getElementById('processButton');

    if (fileInput.files.length === 1) {
        const file = fileInput.files[0];

        const maxSizeInBytes = 10 * 1024 * 1024; // 10 MB
        if (file.size > maxSizeInBytes) {
            alert('File size exceeds the maximum allowed size (5 MB). Please choose a smaller file.');
            fileInput.value = ''; // Clear the file input
            processButton.style.display = 'none';
        } else {
            processButton.style.display = 'block';
        }
    } else {
        processButton.style.display = 'none';
    }
}

// Drag box & handling input file
function handleDragOver(event) {
    event.preventDefault();
    document.getElementById('fileDropArea').classList.add('drag-over');
}

function handleFileDrop(event) {
    event.preventDefault();
    document.getElementById('fileDropArea').classList.remove('drag-over');

    const fileInput = document.getElementById('fileInput');
    const file = event.dataTransfer.files[0];

    fileInput.files = event.dataTransfer.files;
    handleFile(file);
}

function handleClickToChoose() {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
}

function handleFileSelection() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    handleFile(file);
}

function handleFile(file) {
    if (file) {
        const dropArea = document.getElementById('fileDropArea');
        document.getElementById('processButton').style.display = 'block';
        document.getElementById('successfullySaved').style.display = 'none';
        document.getElementById('imputProblem').style.display = 'none';
        document.getElementById('savingFailed').style.display = 'none';
        dropArea.querySelector('span').textContent = `File: ${file.name}`;
    } else {
        console.error('No file selected.');
    }
}