// DOM Elements
const fileInput = document.getElementById('fileInput');
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const dropZone = document.getElementById('dropZone');
const loadingOverlay = document.getElementById('loadingOverlay');
const inputSection = document.getElementById('inputSection');
const resultsSection = document.getElementById('resultsSection');
const backBtn = document.getElementById('backBtn');
const modeBtns = document.querySelectorAll('.mode-btn');
const viewPanes = document.querySelectorAll('.view-pane');

// Event Listeners for Drag & Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-active');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-active');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-active');
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    dropZone.querySelector('p').textContent = `Selected: ${file.name}`;
}

// Main Analyze Button Logic
analyzeBtn.addEventListener('click', async () => {
    let reportText = textInput.value.trim();
    const file = fileInput.files[0];

    // Reset previous inputs if needed? No, just checking what to prioritize.
    // If text is present, use that. If text is empty but file is present, process file.

    // Priority: User inputted Text directly > File.
    if (!reportText && !file) {
        alert("Please upload a PDF/TXT or paste report text.");
        return;
    }

    loadingOverlay.hidden = false;

    try {
        if (!reportText && file) {
            reportText = await processFile(file);
        }

        if (!reportText.trim()) {
            throw new Error("Could not extract text from the input.");
        }

        // Send to Backend
        await fetchAnalysis(reportText);

    } catch (err) {
        alert(`Error: ${err.message}`);
        loadingOverlay.hidden = true;
    }
});

// File Processing (PDF.js specific)
async function processFile(file) {
    if (file.type === 'application/pdf') {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
        let fullText = '';

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(' ');
            fullText += pageText + '\n';
        }
        return fullText;
    } else if (file.type === 'text/plain') {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    } else {
        throw new Error("Unsupported file type. Please use PDF or TXT.");
    }
}

// API Call
async function fetchAnalysis(text) {
    const response = await fetch('/explain-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ report_text: text })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Analysis failed');
    }

    const data = await response.json();
    displayResults(data);
    loadingOverlay.hidden = true;
}

// UI Helpers
function displayResults(data) {
    inputSection.hidden = true;
    resultsSection.hidden = false;

    // Reset view to default
    updateMode('patient');

    document.getElementById('patientContent').innerHTML = parseMarkdown(data.patient_explanation);
    document.getElementById('clinicianContent').innerHTML = parseMarkdown(data.clinician_explanation);

    const citationList = document.getElementById('citationList');
    citationList.innerHTML = data.citations.map(c => `<li><a href="${c}" target="_blank">${c}</a></li>`).join('');

    document.getElementById('disclaimerText').textContent = data.disclaimer;
}

function parseMarkdown(text) {
    if (!text) return '';
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

// Mode Toggling
modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;
        updateMode(mode);
    });
});

function updateMode(mode) {
    // Update Buttons
    modeBtns.forEach(btn => {
        const isSelected = btn.dataset.mode === mode;
        if (isSelected) {
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
        } else {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        }
    });

    // Update Panes
    viewPanes.forEach(pane => {
        pane.classList.remove('active');
        pane.hidden = true;
    });

    const activePane = document.getElementById(`${mode}View`);
    activePane.classList.add('active');
    activePane.hidden = false;
    activePane.focus();
}

// Reset
backBtn.addEventListener('click', () => {
    resultsSection.hidden = true;
    inputSection.hidden = false;
    fileInput.value = '';
    textInput.value = '';
    dropZone.querySelector('p').textContent = 'Drag & drop PDF/TXT or click to browse';
});
