class BullyingDetector {
    constructor() {
        this.apiEndpoints = {
            ethernet: 'http://192.168.3.193:5000/api/detect',  // Try network IP first
            networkShare: 'http://192.168.137.1:5000/api/detect',
            local: 'http://localhost:5000/api/detect',
            loopback: 'http://127.0.0.1:5000/api/detect'
        };
        this.apiUrl = this.apiEndpoints.ethernet;  // Set network IP as default
        this.form = document.getElementById('detection-form');
        this.results = document.getElementById('results');
        this.loading = document.getElementById('loading');
        this.imagePreview = document.getElementById('image-preview');
        
        // Add connection status display
        this.connectionStatus = document.createElement('div');
        this.connectionStatus.className = 'connection-status';
        this.form.parentElement.insertBefore(this.connectionStatus, this.form);
        
        this.initializeConnection().catch(error => {
            console.warn('Connection initialization failed:', error);
        });
        this.initializeEventListeners();
    }

    async initializeConnection() {
        this.connectionStatus.innerHTML = '<p>Connecting to server...</p>';
        
        for (const [key, url] of Object.entries(this.apiEndpoints)) {
            try {
                const healthUrl = url.replace('/detect', '/health');
                const response = await fetch(healthUrl, {
                    method: 'GET',
                    headers: { 'Accept': 'application/json' },
                    mode: 'cors'
                });
                
                if (response.ok) {
                    console.log(`Connected to API at: ${url}`);
                    this.apiUrl = url;
                    this.connectionStatus.innerHTML = `<p class="connected">Connected to server at: ${new URL(url).host}</p>`;
                    return;
                }
            } catch (error) {
                console.warn(`Failed to connect to ${key} endpoint: ${url}`);
            }
        }
        this.connectionStatus.innerHTML = '<p class="error">Failed to connect to server. Using default endpoint.</p>';
        console.warn('Using default endpoint as fallback');
    }

    initializeEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Image preview
        const imageInput = document.getElementById('input-file');
        imageInput.addEventListener('change', (e) => this.handleImagePreview(e));
    }

    async handleSubmit(e) {
        e.preventDefault();
        this.showLoading();

        try {
            const textInput = document.getElementById('input-text').value.trim();
            const imageInput = document.getElementById('input-file').files[0];

            // Build request data
            const data = {};
            if (textInput) {
                data.text = textInput;
            }
            if (imageInput) {
                data.image = await this.getBase64(imageInput);
            }

            if (!data.text && !data.image) {
                throw new Error("Please provide text, an image, or both.");
            }

            // Send request
            const result = await this.detectBullying(data);
            this.displayResults(result);

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async getBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = error => reject(error);
        });
    }

    handleImagePreview(e) {
        const file = e.target.files[0];
        if (file) {
            // Validate file size before preview
            if (file.size > 5 * 1024 * 1024) { // 5MB limit
                this.showError('File size exceeds 5MB limit');
                e.target.value = ''; // Clear the file input
                this.imagePreview.style.display = 'none';
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    // Image loaded successfully, show preview
                    this.imagePreview.src = e.target.result;
                    this.imagePreview.style.display = 'block';
                    
                    // Log original dimensions
                    console.log(`Original image dimensions: ${img.width}x${img.height}`);
                };
                img.src = e.target.result;
            };
            reader.onerror = () => {
                this.showError('Error loading image preview');
                this.imagePreview.style.display = 'none';
            };
            reader.readAsDataURL(file);
        } else {
            this.imagePreview.style.display = 'none';
        }
    }

    displayResults(result) {
        this.results.style.display = 'block';

        try {
            console.log('Full Analysis result:', result);

            // Get the appropriate analysis result
            const analysis = result.combined_result || result.image_analysis || result.text_analysis;
            
            if (!analysis) {
                throw new Error('No analysis results available');
            }

            const severityClass = analysis.severity.toLowerCase() === 'high' ? 'danger' : 
                                analysis.severity.toLowerCase() === 'medium' ? 'warning' : 'safe';

            // Build detailed analysis section based on what's available
            let detailedAnalysis = '';
            
            // Check if this is a combined analysis
            if (result.combined_result && result.combined_result.analysis) {
                detailedAnalysis = `
                    <div class="correlation-info">
                        <h4>Combined Analysis Details</h4>
                        <p><strong>Text Content:</strong> "${result.combined_result.analysis.text_content}"</p>
                        <p><strong>Image Description:</strong> "${result.combined_result.analysis.image_description}"</p>
                        <p><strong>Correlation Score:</strong> ${(result.combined_result.analysis.correlation_score * 100).toFixed(1)}%</p>
                    </div>
                `;
            }
            // Check if only text analysis
            else if (result.text_analysis && !result.image_analysis) {
                detailedAnalysis = `
                    <div class="analysis-info">
                        <h4>Text Analysis Details</h4>
                        <p><strong>Detection Type:</strong> Text Only</p>
                    </div>
                `;
            }
            // Check if only image analysis
            else if (result.image_analysis && !result.text_analysis) {
                detailedAnalysis = `
                    <div class="analysis-info">
                        <h4>Image Analysis Details</h4>
                        <p><strong>Detection Type:</strong> Image Only</p>
                    </div>
                `;
            }

            // Build image description section if available
            const imageDescriptionSection = analysis.image_description ? 
                `<p><strong>Image Description:</strong> ${analysis.image_description}</p>` : '';

            // Build categories section
            const categoriesSection = analysis.categories && analysis.categories.length > 0 ? 
                `<p><strong>Categories:</strong> ${analysis.categories.join(', ')}</p>` :
                `<p><strong>Categories:</strong> None</p>`;

            this.results.innerHTML = `
                <div class="result-card ${severityClass}">
                    <h3>Detection Results</h3>
                    <p><strong>Bullying Detected:</strong> ${analysis.is_bullying ? 'Yes' : 'No'}</p>
                    <p><strong>Confidence:</strong> ${(analysis.confidence * 100).toFixed(1)}%</p>
                    <p><strong>Severity:</strong> ${analysis.severity}</p>
                    
                    <div class="analysis-section">
                        <h4>Analysis Details</h4>
                        ${detailedAnalysis}
                        ${imageDescriptionSection}
                        ${categoriesSection}
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error displaying results:', error);
            this.showError(`Failed to display results: ${error.message}`);
        }
    }

    showLoading() {
        this.loading.style.display = 'block';
        this.results.style.display = 'none';
    }

    hideLoading() {
        this.loading.style.display = 'none';
    }

    showError(message) {
        this.results.innerHTML = `
            <div class="result-card danger">
                <h3>Error</h3>
                <p>${message}</p>
                <p class="error-details">Please check your input and try again.</p>
            </div>
        `;
        this.results.style.display = 'block';
    }

    async detectBullying(data) {
        let lastError = null;

        // Try each endpoint until one works
        for (const [key, url] of Object.entries(this.apiEndpoints)) {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(data),
                    mode: 'cors'
                });

                if (response.ok) {
                    this.apiUrl = url; // Update to working endpoint
                    return await response.json();
                }
                lastError = `${key} endpoint failed: ${response.status}`;
            } catch (error) {
                lastError = `${key} endpoint error: ${error.message}`;
                console.warn(lastError);
            }
        }
        throw new Error(lastError || 'All endpoints failed');
    }
}

// Initialize once DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new BullyingDetector();
});
