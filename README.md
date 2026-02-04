# DB7 – Multimodal Cyberbullying Detection Using Inter-Modal-Attention-Based Deep Learning

## Team Info

- **22471A05O5 — Tatapudi Rajesh**  
  LinkedIn: https://linkedin.com/in/rajesh-tatapudi  
  **Work Done:** Complete project implementation including dataset preprocessing, BERT text pipeline, BLIP image captioning, inter-modal attention model design, training, evaluation, result analysis, API development, and full documentation. Led the entire project from design to deployment.

- **22471A05N7 — Panchumarthi Lakshmi Gopinath**  
  LinkedIn: https://linkedin.com/in/panchumarthi-gopinath  
  **Work Done:** Helped in dataset collection, testing of modules, and preparation of presentation slides.

- **23475A0511 — Chilaka Santhosh**  
  LinkedIn: https://linkedin.com/in/santhosh-chilaka-a20544348  
  **Work Done:** Assisted in basic UI testing and report formatting.

---

## Abstract

Cyberbullying on social media continues to affect users emotionally and socially, creating an urgent need for automated detection systems that can interpret both language and visuals. In this project, we designed a multimodal framework that learns from text and image data using an **inter-modal attention mechanism**.  

The text is represented through **BERT embeddings**, while **BLIP** is applied to generate image captions and visual context. These representations are fused and processed through **BiLSTM layers** to recognize bullying cues.  

Along with classification, the system performs:

- Input validation  
- NSFW screening  
- Severity estimation  
- Category assignment  

Experiments on the **MMHS150K dataset** achieved:

- **Accuracy: 87.2%**  
- **Precision: 85.6%**  
- **Recall: 84.9%**  
- **F1-Score: 85.2%**

which surpass prior methods such as SAFE, MCNN, and LBP-sim.

---

## Our Improvement Over Existing Paper

Our implementation improves earlier approaches in the following ways:

1. **Replaced OCR with BLIP captioning**
   - Faster processing  
   - Better semantic understanding  
   - Less noise than OCR text extraction  

2. **Cyberbullying-focused tuning**
   - Handles sarcasm, slang, and coded hate  
   - Works well on memes and indirect abuse  

3. **Structured moderation output**
   - JSON response with severity & category  
   - Ready for real-time filtering systems  

4. **Lightweight and deployment friendly**
   - Reduced computational overhead  
   - Suitable for social media platforms

---

## About the Project

### What the Project Does
The system automatically detects **cyberbullying content** from social media posts by analyzing:

- Text (tweets, captions, comments)  
- Images (memes, photos)

It identifies:

- Whether the post is bullying  
- Level of severity  
- Type of bullying category

### Why It Is Useful

- Assists social media moderation  
- Protects users from online harassment  
- Reduces manual monitoring effort  
- Detects hidden abuse in memes and sarcasm

### General Workflow

```
Input → Preprocessing → BERT + BLIP → Inter-Modal Attention → Classification → Output
```

**Output Includes**

- is_bullying  
- confidence score  
- severity  
- category  
- image description

---

## Dataset Used

👉 **MMHS150K – Multimodal Hate Speech Dataset**  
Dataset Link: https://www.kaggle.com/datasets/victorcallejasf/multimodal-hate-speech

### Dataset Details

- Total samples: **150,000 posts**  
- Modalities: text + images  
- Classes: Hate / Not Hate  

**Split**

- Training: 134,823  
- Validation: 5,000  
- Testing: 10,000  

**Class Distribution**

- Hate: 44,001  
- Not Hate: 105,999  

Contains memes, sarcastic posts, abusive comments, and neutral content.

---

## Dependencies Used

- Python 3.10  
- PyTorch  
- HuggingFace Transformers  
- BERT Base  
- BLIP Image Captioning  
- OpenCV  
- Pillow  
- Scikit-learn  
- NumPy, Pandas  
- Matplotlib  
- Flask

---

## EDA & Preprocessing

### Text Preprocessing
- Remove URLs, emojis, mentions  
- Lowercasing  
- BERT tokenization  
- Padding to 128 tokens  
- Attention mask creation

### Image Preprocessing
- Resize to 224×224  
- RGB conversion  
- Normalization  
- BLIP caption generation

### Input Handling
- Text only → BERT  
- Image only → BLIP  
- Both → Fusion model

---

## Model Training Info

- **Text Encoder:** BERT (768-dim)  
- **Image Encoder:** BLIP → projected to 768  
- **Fusion:** Inter-modal attention  
- **Classifier:** BiLSTM + Dense  
- **Loss:** BCEWithLogits  
- **Optimizer:** Adam  
- **Environment:** Google Colab – Tesla T4

---

## Model Testing / Evaluation

### Metrics Used
- Accuracy  
- Precision  
- Recall  
- F1 Score  
- AUC  
- Confusion Matrix

### Ablation Study

| Modality | Accuracy |
|---|---|
| Text only | 82.1% |
| Image only | 76.4% |
| Text + Image | 84.9% |
| Text + Image + Captions | **87.2%** |

---

## Results

### Final Performance

| Metric | Score |
|------|-------|
| Accuracy | 0.872 |
| Precision | 0.856 |
| Recall | 0.849 |
| F1 Score | 0.852 |
| AUC | 0.912 |

### Key Strengths

- Detects sarcasm & memes  
- Works with missing modality  
- Low false positives  
- Interpretable attention maps

---

## Limitations & Future Work

### Limitations
- Limited multilingual support  
- Struggles with highly coded slang  
- Dataset bias toward English

### Future Work
- XLM-R for multilingual  
- Explainable AI (SHAP)  
- Model compression  
- Cross-platform testing

---

## Deployment Info

### Features
- REST API  
- JSON moderation output  
- NSFW filter  
- Real-time inference

### Sample Output

```json
{
  "is_bullying": true,
  "confidence": 0.91,
  "severity": "high",
  "category": ["harassment", "body_shaming"],
  "image_description": "meme with insulting text"
}
```

### Usable In
- Twitter / X moderation  
- Instagram filters  
- Forum monitoring  
- College grievance cells

---

## Paper Reference

👉 **An inter-modal attention-based deep learning framework using unified modality for multimodal fake news, hate speech, and offensive language detection – Ayetiran & Ozgobek**  
Link: https://www.sciencedirect.com/science/article/pii/S0306437924000378

---

### Developed By
**Tatapudi Rajesh – Lead Developer & Researcher**  
LinkedIn: https://linkedin.com/in/rajesh-tatapudi
