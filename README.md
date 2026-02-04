# 🚀 DB7 – Multimodal Cyberbullying Detection  
### Using Inter-Modal Attention-Based Deep Learning

---

## 👥 Team Information

### **Project Lead**
- **Tatapudi Rajesh — 22471A05O5**  
  🔗 [LinkedIn Profile](https://linkedin.com/in/rajesh-tatapudi)  
  **Contribution:**  
  - Complete end-to-end implementation  
  - Dataset preprocessing & analysis  
  - BERT text pipeline  
  - BLIP image captioning integration  
  - Inter-modal attention model design  
  - Training, evaluation & result analysis  
  - API development & documentation  
  - Deployment workflow

### Supporting Members
- **Panchumarthi Lakshmi Gopinath — 22471A05N7**  
  🔗 [LinkedIn Profile](https://linkedin.com/in/panchumarthi-gopinath)  
  Contribution: Dataset collection support, module testing, presentation preparation

- **Chilaka Santhosh — 23475A0511**  
  🔗 [LinkedIn Profile](https://linkedin.com/in/santhosh-chilaka-a20544348)  
  Contribution: UI testing assistance and report formatting

---

## 📌 Abstract

Cyberbullying on social media causes serious emotional and social harm, demanding intelligent automated detection systems capable of understanding **both text and images**.  

This project presents a **multimodal deep learning framework** that uses:

- **BERT** → textual understanding  
- **BLIP** → image caption & visual semantics  
- **Inter-modal Attention** → cross-modal fusion  
- **BiLSTM** → contextual sequence learning  

### Additional Capabilities
- Input validation  
- NSFW content screening  
- Severity estimation  
- Category classification  

### Performance on MMHS150K Dataset

| Metric | Score |
|------|-------|
| Accuracy | **87.2%** |
| Precision | **85.6%** |
| Recall | **84.9%** |
| F1-Score | **85.2%** |

✔ Outperforms SAFE, MCNN, and LBP-sim baselines  
✔ Lightweight & deployable for real-time moderation

---

## 📖 Inspiration Paper

**An inter-modal attention-based deep learning framework using unified modality for multimodal fake news, hate speech, and offensive language detection – Ayetiran & Ozgobek**  

🔗 [Paper Reference Link](https://www.sciencedirect.com/science/article/pii/S0306437924000378)

---

## ✨ Improvements Over Existing Work

1. **BLIP instead of OCR**
   - Cleaner semantic extraction  
   - Faster processing  
   - Less noise

2. **Cyberbullying-specific tuning**
   - Detects sarcasm & coded abuse  
   - Handles memes effectively

3. **Production-ready output**
   - JSON moderation response  
   - Severity & category tagging

4. **Lightweight architecture**
   - Lower computational cost  
   - Real-time capable

---

## 🧠 About the Project

### What It Does
Analyzes social media posts containing:
- 📝 Text  
- 🖼 Images  
- 🧩 Both modalities  

and predicts:

- Is it bullying?  
- How severe?  
- What category?  

---

### Why It Matters

- Protects users from online harassment  
- Assists moderators  
- Reduces manual review load  
- Understands memes + sarcasm

---

### System Workflow

```
Input → Preprocessing  
      → BERT (Text) + BLIP (Image)  
      → Inter-Modal Attention  
      → BiLSTM Classifier  
      → Structured Output
```

**Output Includes**
- bullying flag  
- confidence score  
- severity level  
- categories  
- image description

---

## 📂 Dataset

### MMHS150K – Multimodal Hate Speech Dataset  
🔗 [Dataset Reference Link](https://www.kaggle.com/datasets/victorcallejasf/multimodal-hate-speech)

**Statistics**

- 🧮 Total: 150,000 posts  
- 🧩 Modalities: Text + Images  
- 🏷 Classes: Hate / Not Hate  

**Split**

- Train: 134,823  
- Validation: 5,000  
- Test: 10,000  

**Distribution**

- Hate: 44,001  
- Not Hate: 105,999  

> Includes memes, sarcasm, abusive and neutral content.

---

## 🛠 Technologies & Dependencies

- Python 3.10  
- PyTorch  
- HuggingFace Transformers  
- BERT Base  
- BLIP  
- OpenCV  
- Pillow  
- Scikit-learn  
- NumPy, Pandas  
- Matplotlib  
- Flask

---

## 🔎 EDA & Preprocessing

### Text Pipeline
- URL / emoji / mention removal  
- Lowercasing  
- BERT tokenization (128)  
- Attention masks

### Image Pipeline
- Resize → 224×224  
- RGB normalization  
- BLIP captions

### Input Modes
- Text only → BERT  
- Image only → BLIP  
- Both → Fusion

---

## 🧪 Model Training

| Component | Method |
|---|---|
| Text Encoder | BERT (768-d) |
| Image Encoder | BLIP → 768 |
| Fusion | Inter-modal Attention |
| Classifier | BiLSTM + Dense |
| Loss | BCEWithLogits |
| Optimizer | Adam |
| Platform | Colab – Tesla T4 |

---

## 📊 Evaluation

### Metrics
- Accuracy  
- Precision  
- Recall  
- F1  
- AUC  
- Confusion Matrix

### Ablation Study

| Setup | Accuracy |
|---|---|
| Text only | 82.1% |
| Image only | 76.4% |
| Text + Image | 84.9% |
| + Captions | **87.2%** |

---

## 🏆 Results

| Metric | Value |
|---|---|
| Accuracy | 0.872 |
| Precision | 0.856 |
| Recall | 0.849 |
| F1 | 0.852 |
| AUC | 0.912 |

### Strengths
- Meme & sarcasm detection  
- Works with missing modality  
- Low false positives  
- Explainable attention

---

## ⚠ Limitations & Future Work

**Limitations**
- English-centric  
- Struggles with extreme slang

**Future**
- XLM-R multilingual  
- SHAP explainability  
- Quantization  
- Cross-platform tests

---

## 🚀 Deployment

### Features
- Flask REST API  
- NSFW filter  
- Real-time inference

### Sample Response

```json
{
  "is_bullying": true,
  "confidence": 0.91,
  "severity": "high",
  "category": ["harassment", "body_shaming"],
  "image_description": "meme with insulting text"
}
```

### Applications
- Social media moderation  
- Forum monitoring  
- College grievance systems

---

## 👨‍💻 Developed By

**Tatapudi Rajesh – Lead Developer & Researcher**  
🔗 [LinkedIn Profile](https://linkedin.com/in/rajesh-tatapudi)
