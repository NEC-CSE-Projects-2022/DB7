class FormValidator {
    constructor() {
        this.textMaxLength = 1000;
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedImageTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    }

    validateTextInput(text) {
        if (!text || text.trim().length === 0) {
            return {
                isValid: true, // Allow empty text if image is provided
                message: ''
            };
        }

        if (text.length > this.textMaxLength) {
            return {
                isValid: false,
                message: `Text exceeds maximum length of ${this.textMaxLength} characters`
            };
        }

        return {
            isValid: true,
            message: ''
        };
    }

    validateImageFile(file) {
        if (!file) {
            return {
                isValid: true, // Allow no image if text is provided
                message: ''
            };
        }

        // Check file type
        if (!this.allowedImageTypes.includes(file.type)) {
            return {
                isValid: false,
                message: 'Invalid file type. Please upload JPG, JPEG, or PNG images only.'
            };
        }

        // Check file size
        if (file.size > this.maxFileSize) {
            return {
                isValid: false,
                message: 'File size exceeds 5MB limit.'
            };
        }

        return {
            isValid: true,
            message: ''
        };
    }

    validateForm(textInput, imageFile) {
        // At least one input must be provided
        if (!textInput && !imageFile) {
            return {
                isValid: false,
                message: 'Please provide either text or an image to analyze.'
            };
        }

        // Validate text input if provided
        const textValidation = this.validateTextInput(textInput);
        if (!textValidation.isValid) {
            return textValidation;
        }

        // Validate image if provided
        const imageValidation = this.validateImageFile(imageFile);
        if (!imageValidation.isValid) {
            return imageValidation;
        }

        return {
            isValid: true,
            message: ''
        };
    }

    // Additional validation methods
    validateImageDimensions(width, height) {
        const maxDimension = 4096; // Max dimension 4096px
        if (width > maxDimension || height > maxDimension) {
            return {
                isValid: false,
                message: `Image dimensions exceed maximum limit of ${maxDimension}px`
            };
        }
        return {
            isValid: true,
            message: ''
        };
    }

    validateImageContent(file) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                const dimensionValidation = this.validateImageDimensions(img.width, img.height);
                resolve(dimensionValidation);
            };
            img.onerror = () => {
                resolve({
                    isValid: false,
                    message: 'Failed to load image. Please try another file.'
                });
            };
            img.src = URL.createObjectURL(file);
        });
    }

    showError(elementId, message) {
        const errorElement = document.getElementById(`${elementId}-error`);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = message ? 'block' : 'none';
        }
    }
}

// Add validation to the detection form
document.addEventListener('DOMContentLoaded', () => {
    const validator = new FormValidator();
    const form = document.getElementById('detection-form');
    
    if (form) {
        // Add error message containers if not present
        const textInput = document.getElementById('input-text');
        const fileInput = document.getElementById('input-file');
        
        ['text', 'file'].forEach(id => {
            if (!document.getElementById(`${id}-error`)) {
                const errorDiv = document.createElement('div');
                errorDiv.id = `${id}-error`;
                errorDiv.className = 'error-message';
                document.getElementById(`input-${id}`).parentNode.appendChild(errorDiv);
            }
        });

        // Add input validation
        textInput?.addEventListener('input', (e) => {
            const validation = validator.validateTextInput(e.target.value);
            validator.showError('text', validation.message);
        });

        fileInput?.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            const validation = validator.validateImageFile(file);
            validator.showError('file', validation.message);

            if (validation.isValid && file) {
                const contentValidation = await validator.validateImageContent(file);
                validator.showError('file', contentValidation.message);
            }
        });

        // Add form submission validation
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const textInput = document.getElementById('input-text').value;
            const fileInput = document.getElementById('input-file').files[0];

            const validation = validator.validateForm(textInput, fileInput);
            
            if (!validation.isValid) {
                validator.showError('text', validation.message);
                return;
            }

            if (fileInput) {
                const contentValidation = await validator.validateImageContent(fileInput);
                if (!contentValidation.isValid) {
                    validator.showError('file', contentValidation.message);
                    return;
                }
            }

            // If validation passes, continue with form submission
            form.submit();
        });
    }
});

// Export for use in other modules
export default FormValidator;