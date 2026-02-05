# 📦 MMHS150K Dataset — Multimodal Hate Speech & Cyberbullying Dataset

🚨 **Public Access Drive Link:**  
🔗 **[Access the MMHS150K Dataset (Google Drive)](https://drive.google.com/drive/folders/1oMPF3PPELnzKImf1pWb4PRKsfXSeY1r5?usp=sharing)**

---

## 📌 Overview

The **MMHS150K dataset** is a large-scale multimodal dataset designed for research and development of models that perform **hate speech, offensive language, and cyberbullying detection** across **text and images**.

This dataset is highly suitable for deep learning, multimodal fusion models, and attention-based architectures that need to interpret both visual and textual cues — especially for social media content containing memes, screenshots, comments, and posts.

---

## 📊 Contents of the Dataset

The MMHS150K dataset includes:

- **Text content** (e.g., tweets, captions, comments)
- **Associated images** (e.g., memes, photos, screenshots)
- **Labels** indicating the presence of hate speech or offensive content
- **Supporting metadata** for each entry

The multimodal format is ideal for training models that require interaction between **visual and textual modalities**, such as:
- BERT + CNN models
- Multimodal transformers
- Inter-modal attention architectures

---

## 🧮 Dataset Statistics

| Feature | Details |
|---------|---------|
| **Total Samples** | ~150,000 multimodal posts |
| **Modalities** | Text + Images |
| **Class Labels** | Hate / Not Hate |
| **Text Type** | Tweets, captions, comments |
| **Image Type** | Memes, screenshots, photos |

---

## 📖 Training / Validation / Test Split

The dataset is typically partitioned as follows:

| Split | # Samples |
|-------|------------|
| **Training Set** | ~134,823 |
| **Validation Set** | ~5,000 |
| **Testing Set** | ~10,000 |

These splits are designed to support model training, hyperparameter tuning, and unbiased evaluation.

---

## 🏷 Label Distribution

The class distribution in the dataset helps understand the ratio of positive vs. negative instances:

- **Hate / Offensive:** ~44,001  
- **Not Hate / Non-offensive:** ~105,999

The imbalance reflects real-world social media distributions, where harmful content is less prevalent.

---

## 🛠 Typical Features Included

Each sample in the dataset may include:

- **tweet_id**: Unique identifier
- **text**: Original text of the post
- **image_path / image_id**: Reference to associated image
- **label**: Binary indicator (hate vs. not hate)
- **additional metadata**: Tokens, captions, etc.

**Note:** When using models, ensure proper handling of missing modalities (text-only or image-only entries are possible).

---

## 📌 Use Cases

This dataset has been used for:

✔ Multimodal hate speech classification  
✔ Cyberbullying detection  
✔ Attention-based model research  
✔ Cross-modal representation learning  
✔ Benchmarking multimodal architectures

---

## 🧠 Why MMHS150K is Important

- **Multimodal Content:** Allows joint learning from text and images  
- **Realistic Social Media Examples:** Includes memes and sarcastic content  
- **Large Scale:** Suitable for deep learning  
- **Benchmarked:** Widely used in research on hate speech and offensive detection

---

## 📦 Formats Provided

The dataset is usually structured in files such as:

- `.parquet` files
- `.csv` exports
- Folder sets of images
- Metadata files

These are provided to allow efficient loading via pandas, PyTorch `DataLoader`, or TensorFlow data pipelines.

---

## 📥 How to Use the Dataset

1. **Download the dataset folder** from the shared Drive link  
2. Load text and image pairs 
3. Preprocess modalities:
   - Text → Tokenization (e.g., BERT tokenizer)
   - Image → Resize + normalize + caption generation (optional)
4. Construct multimodal dataset loaders
5. Train / Validate / Evaluate models

---

## 📚 Example Code Snippet (PyTorch)

```python
import pandas as pd
from torch.utils.data import DataLoader, Dataset

# Load dataset
df = pd.read_parquet("mmhs150k_train.parquet")

class MMHS150KDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.data = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data.iloc[idx]['text']
        image_path = self.data.iloc[idx]['image']
        label = self.data.iloc[idx]['label']
        # Load image and transform if needed
        return text, image, label

train_dataset = MMHS150KDataset(df)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
```

---

## 📜 References

1. **MMHS150K Dataset Release** – Multimodal Hate Speech dataset for research  
2. **Social Media Hate & Offensive Language Detection Research**  
3. Tools & models such as BERT, CLIP, BLIP, and multimodal fusion architectures

---

## 📌 Disclaimer

The dataset contains text and images that may include **offensive, sensitive, or harmful content**.  
Appropriate care should be taken during research and deployment.

---

## 🚀 Acknowledgements

- Contributors of the MMHS150K dataset  
- Open-source libraries that make multimodal learning feasible (e.g., HuggingFace Transformers, PyTorch)

---

## 📍 Access It Now

👉 **Dataset Reference Link:**  
🔗 **[MMHS150K Public Drive Folder](https://drive.google.com/drive/folders/1oMPF3PPELnzKImf1pWb4PRKsfXSeY1r5?usp=sharing)**

---

