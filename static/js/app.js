// DOM Elements
const registerForm = document.getElementById('registerForm');
const recognizeForm = document.getElementById('recognizeForm');
const userImages = document.getElementById('userImages');
const recognizeImage = document.getElementById('recognizeImage');
const imagePreview = document.getElementById('imagePreview');
const recognizePreview = document.getElementById('recognizePreview');
const registerLoading = document.getElementById('registerLoading');
const recognizeLoading = document.getElementById('recognizeLoading');
const registerResult = document.getElementById('registerResult');
const recognizeResult = document.getElementById('recognizeResult');

// Image preview for registration
userImages.addEventListener('change', function(e) {
    const files = Array.from(e.target.files);
    imagePreview.innerHTML = '';
    
    if (files.length < 4) {
        showAlert('Please select at least 4 images for better recognition accuracy.', 'warning', imagePreview);
        return;
    }
    
    files.forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'image-preview';
                img.alt = 'Preview';
                imagePreview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
});

// Image preview for recognition
recognizeImage.addEventListener('change', function(e) {
    const file = e.target.files[0];
    recognizePreview.innerHTML = '';
    
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'image-preview mx-auto d-block';
            img.alt = 'Preview';
            recognizePreview.appendChild(img);
        };
        reader.readAsDataURL(file);
    }
});

// Register form submission
registerForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(registerForm);
    const files = userImages.files;
    
    // Validate minimum 4 images
    if (files.length < 4) {
        showAlert('Please upload at least 4 face images for better recognition accuracy.', 'danger', registerResult);
        return;
    }
    
    // Show loading
    registerLoading.style.display = 'block';
    registerResult.innerHTML = '';
    
    try {
        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert(data.message, 'success', registerResult);
            registerForm.reset();
            imagePreview.innerHTML = '';
        } else {
            showAlert(data.error || 'Registration failed', 'danger', registerResult);
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger', registerResult);
    } finally {
        registerLoading.style.display = 'none';
    }
});

// Recognize form submission
recognizeForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(recognizeForm);
    
    // Show loading
    recognizeLoading.style.display = 'block';
    recognizeResult.innerHTML = '';
    
    try {
        const response = await fetch('/recognize', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayRecognitionResults(data.matches);
        } else {
            showAlert(data.error || 'Recognition failed', 'danger', recognizeResult);
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger', recognizeResult);
    } finally {
        recognizeLoading.style.display = 'none';
    }
});

// Display recognition results
function displayRecognitionResults(matches) {
    let html = '<h4 class="mb-3"><i class="fas fa-users"></i> Recognition Results</h4>';
    
    if (matches && matches.length > 0) {
        matches.forEach((match, index) => {
            const confidence = Math.round(match.similarity * 100);
            let badgeClass = 'bg-success';
            
            if (confidence < 60) {
                badgeClass = 'bg-warning';
            } else if (confidence < 80) {
                badgeClass = 'bg-info';
            }
            
            html += `
                <div class="result-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-1">
                                <i class="fas fa-user"></i> ${match.name}
                            </h5>
                            <p class="mb-1">
                                <i class="fas fa-id-card"></i> ID: ${match.user_id}
                            </p>
                            <p class="mb-0">
                                <i class="fas fa-envelope"></i> ${match.email}
                            </p>
                        </div>
                        <div class="text-end">
                            <span class="badge ${badgeClass} similarity-badge">
                                ${confidence}% Match
                            </span>
                            <br>
                            <small class="text-muted">Rank #${index + 1}</small>
                        </div>
                    </div>
                </div>
            `;
        });
    } else {
        html += '<div class="alert alert-info"><i class="fas fa-info-circle"></i> No matching faces found.</div>';
    }
    
    recognizeResult.innerHTML = html;
}

// Show alert function
function showAlert(message, type, container) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas fa-${getIconForType(type)}"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    container.innerHTML = alertHtml;
}

// Get icon for alert type
function getIconForType(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'danger': return 'exclamation-triangle';
        case 'warning': return 'exclamation-circle';
        case 'info': return 'info-circle';
        default: return 'info-circle';
    }
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
