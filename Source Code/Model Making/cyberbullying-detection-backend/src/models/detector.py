import warnings
warnings.filterwarnings('ignore')

import logging
import base64
from PIL import Image
from io import BytesIO
import numpy as np
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
import torch
import cv2

class BullyingDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)  # Enable debug logging
        
        try:
            # Initialize text classifier
            self.logger.info("Initializing text classifier...")
            self.text_classifier = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                return_all_scores=True
            )
            
            # Initialize BLIP model with explicit content detection
            self.logger.info("Initializing BLIP model...")
            self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
            self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.blip_model.to(self.device)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {str(e)}")
            raise

    def analyze_text(self, text):
        try:
            if not text or not isinstance(text, str):
                return {
                    'is_bullying': False,
                    'confidence': 0.0,
                    'severity': 'LOW',
                    'categories': []
                }

            # Get classification scores
            results = self.text_classifier(text)
            toxic_score = max([score['score'] for score in results[0] if score['label'] == 'toxic'], default=0)
            
            # Get categories
            categories = self._get_categories(text)
            
            return {
                'is_bullying': toxic_score > 0.5,
                'confidence': float(toxic_score),
                'severity': self._get_severity(toxic_score),
                'categories': categories
            }
            
        except Exception as e:
            self.logger.error(f"Text analysis error: {str(e)}")
            raise

    def analyze_image(self, image_data):
        try:
            # Validate input
            if not image_data:
                raise ValueError("No image data provided")

            # Clean base64 data
            if isinstance(image_data, str) and ',' in image_data:
                image_data = image_data.split(',')[1]

            # Decode image with error handling
            try:
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                if image.mode != 'RGB':
                    image = image.convert('RGB')
            except Exception as e:
                self.logger.error(f"Image decode error: {str(e)}")
                raise ValueError(f"Invalid image format: {str(e)}")

            # BLIP analysis with error handling
            try:
                inputs = self.blip_processor(image, return_tensors="pt").to(self.device)
                outputs = self.blip_model.generate(
                    **inputs,
                    max_new_tokens=150,
                    num_beams=5,
                    temperature=1.0,
                    repetition_penalty=1.5
                )
                image_description = self.blip_processor.decode(outputs[0], skip_special_tokens=True)
                self.logger.info(f"Generated description: {image_description}")
            except Exception as e:
                self.logger.error(f"BLIP analysis error: {str(e)}")
                raise ValueError(f"BLIP analysis failed: {str(e)}")

            # Content analysis
            result = {
                'is_bullying': False,
                'confidence': 0.0,
                'severity': 'LOW',
                'categories': [],
                'image_description': image_description
            }

            # Check for NSFW content
            image_np = np.array(image)
            nsfw_check = self._check_nsfw_content(image_np)
            
            if nsfw_check['is_nsfw']:
                result.update({
                    'is_bullying': True,
                    'confidence': float(nsfw_check['confidence']),
                    'severity': 'HIGH',
                    'categories': ['explicit_content', 'nsfw']
                })
            else:
                # Analyze description for potential issues
                text_analysis = self.analyze_text(image_description)
                result.update({
                    'is_bullying': text_analysis['is_bullying'],
                    'confidence': float(text_analysis['confidence']),
                    'severity': text_analysis['severity'],
                    'categories': text_analysis['categories']
                })

            return result

        except Exception as e:
            self.logger.error(f"Image analysis failed: {str(e)}")
            return {
                'error': str(e),
                'is_bullying': False,
                'confidence': 0.0,
                'severity': 'LOW',
                'categories': [],
                'image_description': 'Analysis failed'
            }

    def _check_nsfw_content(self, image_np):
        try:
            # Convert to HSV for better skin detection
            hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
            
            # Multiple skin tone ranges
            skin_ranges = [
                (np.array([0, 20, 70]), np.array([20, 150, 255])),    # Light skin
                (np.array([170, 20, 70]), np.array([180, 150, 255])), # Dark skin
            ]
            
            # Combine skin masks
            skin_mask = np.zeros(image_np.shape[:2], dtype=np.uint8)
            for lower, upper in skin_ranges:
                skin_mask = cv2.bitwise_or(skin_mask, cv2.inRange(hsv, lower, upper))
            
            # Calculate metrics
            total_pixels = skin_mask.size
            skin_pixels = np.sum(skin_mask > 0)
            skin_ratio = skin_pixels / total_pixels
            
            # Image properties
            height, width = image_np.shape[:2]
            aspect_ratio = width / height
            image_size = width * height
            
            # Refined NSFW detection criteria
            is_nsfw = (
                skin_ratio > 0.30 and          # Reduced skin threshold
                (0.4 < aspect_ratio < 2.5) and # Wider aspect ratio range
                image_size > 50000 and         # Lower minimum size
                skin_pixels > 10000            # Minimum skin pixel count
            )
            
            # Confidence calculation
            base_confidence = skin_ratio * 0.7  # Base on skin ratio
            size_factor = min(1.0, image_size / 1000000) * 0.15  # Size factor
            aspect_confidence = 0.15 if (0.5 < aspect_ratio < 2.0) else 0  # Aspect ratio factor
            
            confidence = base_confidence + size_factor + aspect_confidence
            
            self.logger.debug(
                f"NSFW metrics - "
                f"Skin ratio: {skin_ratio:.3f}, "
                f"Aspect ratio: {aspect_ratio:.2f}, "
                f"Size: {image_size}, "
                f"Confidence: {confidence:.3f}"
            )
            
            return {
                'is_nsfw': is_nsfw,
                'confidence': float(confidence)
            }
            
        except Exception as e:
            self.logger.error(f"NSFW check error: {str(e)}")
            return {'is_nsfw': False, 'confidence': 0.0}

    def _get_severity(self, score):
        if score > 0.8:
            return 'HIGH'
        elif score > 0.5:
            return 'MEDIUM'
        return 'LOW'

    def _get_categories(self, text):
        categories = []
        text = text.lower()
        
        category_keywords = {
            'harassment': ['bully', 'harass', 'threaten'],
            'hate_speech': ['hate', 'racist', 'discriminate'],
            'sexual': ['nsfw', 'explicit', 'nude', 'porn'],
            'profanity': ['fuck', 'shit', 'damn'],
            'threat': ['kill', 'hurt', 'die']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                categories.append(category)
                
        return categories

    def analyze_content(self, data):
        result = {
            'text_analysis': None,
            'image_analysis': None,
            'combined_result': None
        }
        
        try:
            # Process text if provided
            if 'text' in data and data['text']:
                text_analysis = self.analyze_text(data['text'])
                result['text_analysis'] = text_analysis
                result['combined_result'] = text_analysis  # Set as combined if only text
        
            # Process image if provided
            if 'image' in data:
                image_analysis = self.analyze_image(data['image'])
                result['image_analysis'] = image_analysis
                
                # If no text was provided, set image analysis as combined result
                if not result['combined_result']:
                    result['combined_result'] = image_analysis
        
            # If both text and image provided, correlate them
            if result['text_analysis'] and result['image_analysis']:
                result['combined_result'] = self._correlate_text_and_image(
                    data['text'],
                    result['text_analysis'],
                    result['image_analysis']
                )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Content analysis error: {str(e)}")
            raise

    def _correlate_text_and_image(self, user_text, text_analysis, image_analysis):
        """
        Correlate text input with image content to detect relationships
        """
        try:
            # Get image description
            image_description = image_analysis.get('image_description', '')
            
            # Analyze relationship between user text and image
            combined_text = f"{user_text} {image_description}"
            
            # Get confidence scores
            text_confidence = float(text_analysis['confidence'])
            image_confidence = float(image_analysis['confidence'])
            
            # Calculate combined confidence
            # If both are bullying, confidence increases significantly
            if text_analysis['is_bullying'] and image_analysis['is_bullying']:
                combined_confidence = min(1.0, (text_confidence + image_confidence) * 0.6)
                combined_severity = 'HIGH'
                combined_bullying = True
            # If one is bullying and they correlate, increase confidence
            elif text_analysis['is_bullying'] or image_analysis['is_bullying']:
                # Check correlation between text and image
                correlation_score = self._calculate_correlation(user_text, image_description)
                combined_confidence = max(text_confidence, image_confidence) * (0.8 + correlation_score * 0.2)
                combined_confidence = min(1.0, combined_confidence)
                combined_bullying = True
                combined_severity = 'HIGH' if combined_confidence > 0.7 else 'MEDIUM'
            else:
                combined_confidence = (text_confidence + image_confidence) / 2
                combined_bullying = False
                combined_severity = 'LOW'
            
            # Combine categories
            categories = list(set(
                text_analysis.get('categories', []) + 
                image_analysis.get('categories', [])
            ))
            
            result = {
                'is_bullying': combined_bullying,
                'confidence': float(combined_confidence),
                'severity': combined_severity,
                'categories': categories,
                'analysis': {
                    'text_content': user_text,
                    'image_description': image_description,
                    'text_analysis': text_analysis,
                    'image_analysis': image_analysis,
                    'correlation_score': self._calculate_correlation(user_text, image_description)
                }
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Correlation error: {str(e)}")
            # Fallback to simple combination
            return self._combine_analyses(text_analysis, image_analysis)

    def _calculate_correlation(self, text, image_description):
        """
        Calculate semantic correlation between user text and image description
        Returns score between 0 and 1
        """
        try:
            if not text or not image_description:
                return 0.0
            
            text_lower = text.lower()
            image_lower = image_description.lower()
            
            # Define semantic relationships
            semantic_groups = {
                'selfie_related': ['selfie', 'posting', 'photo', 'picture', 'image', 'face', 'person', 'people', 'cell phone', 'phone', 'smartphone'],
                'appearance': ['face', 'look', 'looks', 'appearance', 'ugly', 'pretty', 'beautiful', 'stupid', 'dumb'],
                'social': ['post', 'posting', 'share', 'social', 'media', 'profile', 'account'],
                'people': ['person', 'people', 'girl', 'guy', 'boy', 'woman', 'man']
            }
            
            # Count semantic matches
            matches = 0
            total_groups = len(semantic_groups)
            
            for group, keywords in semantic_groups.items():
                group_in_text = any(keyword in text_lower for keyword in keywords)
                group_in_image = any(keyword in image_lower for keyword in keywords)
                
                if group_in_text and group_in_image:
                    matches += 1
                    self.logger.debug(f"Semantic match in group '{group}'")
            
            # Calculate semantic correlation
            semantic_correlation = matches / total_groups if total_groups > 0 else 0.0
            
            # Also calculate word overlap (Jaccard)
            text_words = set(text_lower.split())
            image_words = set(image_lower.split())
            
            if len(text_words.union(image_words)) > 0:
                intersection = len(text_words.intersection(image_words))
                union = len(text_words.union(image_words))
                word_correlation = intersection / union
            else:
                word_correlation = 0.0
            
            # Combine both methods (semantic is more important)
            combined_correlation = (semantic_correlation * 0.7) + (word_correlation * 0.3)
            combined_correlation = min(1.0, max(0.0, combined_correlation))
            
            self.logger.debug(f"Correlation breakdown - Semantic: {semantic_correlation:.2f}, "
                             f"Word: {word_correlation:.2f}, Combined: {combined_correlation:.2f}")
            
            return float(combined_correlation)
            
        except Exception as e:
            self.logger.error(f"Correlation calculation error: {str(e)}")
            return 0.0

    def _combine_analyses(self, text_result, image_result):
        """
        Fallback method to combine text and image analyses
        """
        if text_result and not image_result:
            return text_result
        if image_result and not text_result:
            return image_result
        
        if text_result and image_result:
            # Take the higher severity
            severity_order = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
            text_severity = severity_order.get(text_result['severity'], 0)
            image_severity = severity_order.get(image_result['severity'], 0)
            
            severity_map = {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
            max_severity = max(text_severity, image_severity)
            
            return {
                'is_bullying': text_result['is_bullying'] or image_result['is_bullying'],
                'confidence': max(text_result['confidence'], image_result['confidence']),
                'severity': severity_map[max_severity],
                'categories': list(set(text_result.get('categories', []) + image_result.get('categories', [])))
            }
        
        return {
            'is_bullying': False,
            'confidence': 0.0,
            'severity': 'LOW',
            'categories': []
        }

    def analyze_text_image(self, image_data):
        """Specialized method for handling images containing text"""
        try:
            # Clean and decode image data
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            # Decode image
            try:
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                self.logger.debug(f"Text image opened: {image.format}, {image.size}")
            except Exception as e:
                self.logger.error(f"Text image decode error: {str(e)}")
                raise ValueError(f"Cannot decode text image: {str(e)}")

            # Convert to RGB and numpy array
            image_rgb = image.convert('RGB')
            image_np = np.array(image_rgb)

            # Initialize result
            result = {
                'is_bullying': False,
                'confidence': 0.0,
                'severity': 'LOW',
                'categories': [],
                'extracted_text': '',
                'ocr_confidence': 0.0
            }

            try:
                # Convert to grayscale
                gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
                
                # Enhanced preprocessing for text images
                # 1. Denoise
                denoised = cv2.fastNlMeansDenoising(gray)
                
                # 2. Increase contrast
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(denoised)
                
                # 3. Thresholding
                _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # OCR with optimized parameters for text images
                ocr_results = self.image_reader.readtext(
                    binary,
                    paragraph=True,
                    detail=1,
                    min_size=10,
                    text_threshold=0.2,
                    low_text=0.25,
                    link_threshold=0.2,
                    add_margin=0.15,
                    width_ths=0.7,
                    height_ths=0.7,
                    decoder='beamsearch',
                    beamWidth=5
                )

                if ocr_results:
                    # Process OCR results
                    extracted_text = ' '.join([res[1] for res in ocr_results])
                    ocr_confidence = sum([res[2] for res in ocr_results]) / len(ocr_results)
                    
                    self.logger.debug(f"Extracted text from image: '{extracted_text}'")
                    
                    if extracted_text.strip():
                        # Update result with extracted text
                        result.update({
                            'extracted_text': extracted_text,
                            'ocr_confidence': float(ocr_confidence)
                        })

                        # Analyze extracted text for bullying
                        text_analysis = self.analyze_text(extracted_text)
                        result.update({
                            'is_bullying': text_analysis['is_bullying'],
                            'confidence': float(text_analysis['confidence']),
                            'severity': text_analysis['severity'],
                            'categories': text_analysis['categories']
                        })
                    else:
                        result['extracted_text'] = 'No text detected'
                else:
                    result['extracted_text'] = 'No text detected'

            except Exception as e:
                self.logger.error(f"Text extraction error: {str(e)}")
                result['extracted_text'] = 'No text detected'

            return result

        except Exception as e:
            self.logger.error(f"Text image analysis error: {str(e)}")
            return {
                'is_bullying': False,
                'confidence': 0.0,
                'severity': 'LOW',
                'categories': [],
                'extracted_text': 'Error processing text image',
                'ocr_confidence': 0.0
            }