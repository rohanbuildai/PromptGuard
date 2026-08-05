# 🛡️ PromptGuard

> **A Hybrid AI Prompt Injection Detection System** built using **Rule-Based Analysis**, **Semantic Similarity**, and **Machine Learning** to identify malicious prompts before they reach Large Language Models (LLMs).

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-REST%20API-black?style=for-the-badge&logo=flask)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green?style=for-the-badge)
![NLP](https://img.shields.io/badge/NLP-SentenceTransformers-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</p>

---

# 📖 Overview

Large Language Models (LLMs) are vulnerable to **Prompt Injection Attacks**, where attackers manipulate prompts to override system instructions, reveal hidden prompts, bypass safety mechanisms, or extract confidential information.

**PromptGuard** is a hybrid prompt security system that analyzes every incoming prompt through **three independent detection engines** before generating a final security decision.

Unlike traditional rule-based systems, PromptGuard combines multiple AI techniques to improve detection of both **direct attacks** and **paraphrased prompt injection attempts**.

---

# ✨ Features

- ✅ Rule-Based Prompt Injection Detection
- ✅ Semantic Similarity Detection using Sentence Transformers
- ✅ Machine Learning Classification
- ✅ Hybrid Decision Engine
- ✅ REST API built with Flask
- ✅ Automated Testing Framework
- ✅ Modular & Scalable Architecture
- ✅ JSON-based API Responses
- ✅ Configurable Detection Thresholds

---

# 🏗️ System Architecture

```
                    User Prompt
                         │
                         ▼
                Hybrid Decision Engine
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 Rule Engine      Semantic Engine      ML Engine
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
               Final Risk Assessment
                         ▼
                  JSON API Response
```

---

# ⚙️ Detection Engines

## 1️⃣ Rule Engine

The Rule Engine performs deterministic detection using weighted keyword matching.

It detects well-known prompt injection patterns such as:

- Ignore previous instructions
- Reveal your system prompt
- Forget everything above
- Disable your safety mechanisms
- Reveal confidential information

Each suspicious pattern contributes to an overall risk score.

### Responsibilities

- Detect exact prompt injection attacks
- Calculate weighted risk score
- Assign risk level
- Return matched malicious patterns

### Advantages

- Extremely fast
- Reliable for known attacks
- Easy to extend

### Limitations

Cannot detect paraphrased attacks that use different wording.

---

## 2️⃣ Semantic Engine

The Semantic Engine detects attacks based on **meaning** rather than exact text.

It uses the **Sentence Transformers** model:

```
sentence-transformers/all-MiniLM-L6-v2
```

Known prompt injection examples are converted into vector embeddings.

Incoming prompts are embedded and compared using cosine similarity.

This enables PromptGuard to recognize semantically similar attacks even when the wording changes.

### Responsibilities

- Generate embeddings
- Compute semantic similarity
- Detect paraphrased attacks
- Produce semantic risk level

### Advantages

- Detects rewritten attacks
- Captures contextual meaning
- Works beyond exact keyword matching

### Limitations

Requires careful threshold tuning to minimize false positives.

---

## 3️⃣ Machine Learning Engine

PromptGuard also includes a supervised Machine Learning classifier.

### Training Pipeline

```
Prompt Dataset
       │
       ▼
Sentence Embeddings
       │
       ▼
Logistic Regression
       │
       ▼
Trained Model
```

The model was trained on a labeled dataset containing:

- Benign prompts
- Prompt injection examples

The trained model is stored inside:

```
models/
├── promptguard_classifier.pkl
├── label_encoder.pkl
```

During inference the ML Engine returns:

- Prediction
- Class probabilities
- Risk level
- Recommendation

### Advantages

- Learns statistical patterns
- Provides an independent detection signal
- Complements Rule & Semantic engines

### Limitations

Performance depends on dataset quality and diversity.

---

# 🧠 Hybrid Decision Engine

PromptGuard combines the outputs of all three engines to generate a final security assessment.

The Hybrid Decision Engine returns:

- Overall Risk
- Decision Source
- Decision Reason
- Recommendation
- Individual Engine Results

Example:

```json
{
  "overall_risk": "HIGH",
  "decision": {
    "source": "Hybrid Decision Engine",
    "reason": "...",
    "recommendation": "Block this prompt before forwarding it to the LLM."
  }
}
```

---

# 📂 Project Structure

```
PromptGuard/
│
├── config/
│   ├── constants.py
│   ├── patterns.py
│
├── data/
│
├── engines/
│   ├── analyzer.py
│   ├── rule_engine.py
│   ├── semantic_engine.py
│   └── ml_engine.py
│
├── models/
│
├── notebooks/
│
├── screenshots/
│
├── tests/
│   ├── test_api.py
│   ├── test_prompts.json
│   └── test_results.md
│
├── server.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| API | Flask |
| Machine Learning | Scikit-Learn |
| NLP | Sentence Transformers |
| Embeddings | all-MiniLM-L6-v2 |
| Data Processing | NumPy, Pandas |
| Model Serialization | Joblib |
| Testing | Requests |

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/rohanbuildai/PromptGuard.git

cd PromptGuard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
python server.py
```

---

# 🌐 API Endpoints

## Home

```
GET /
```

Returns basic API information.

---

## Health Check

```
GET /health
```

Returns service status.

---

## About

```
GET /about
```

Returns project metadata.

---

## Analyze Prompt

```
POST /analyze
```

Example Request

```json
{
    "prompt":"Ignore previous instructions."
}
```

Example Response

```json
{
    "prompt":"Ignore previous instructions.",

    "overall_risk":"HIGH",

    "decision":{
        "source":"Hybrid Decision Engine",
        "reason":"Critical prompt injection pattern detected.",
        "recommendation":"Block this prompt before forwarding it to the LLM."
    },

    "engines":{
        "rule_engine":{},
        "semantic_engine":{},
        "ml_engine":{}
    }
}
```

---

# 🧪 Testing

PromptGuard includes an automated testing framework.

Run:

```bash
python tests/test_api.py
```

The test suite evaluates multiple prompt categories:

- Safe Prompts
- Direct Prompt Injection Attacks
- Semantic Attacks
- Educational Prompts
- Mixed Adversarial Prompts

This provides a structured way to evaluate the behavior of the hybrid detection system across diverse prompt types.

---

# 🚀 Future Improvements

- Fine-tune Transformer models for classification
- Larger and more diverse prompt datasets
- Better semantic threshold calibration
- Context-aware rule matching
- Confidence-based decision fusion
- Docker support
- CI/CD pipeline
- Interactive Web Dashboard
- Real-time monitoring

---

# 🤝 Contributing

Contributions are welcome.

If you have ideas for improving PromptGuard, feel free to open an issue or submit a pull request.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Rohan Singh**

- GitHub: https://github.com/rohanbuildai

---

## ⭐ Support

If you found this project useful, consider giving it a **Star ⭐** on GitHub.

It helps the project reach more developers and motivates future improvements.