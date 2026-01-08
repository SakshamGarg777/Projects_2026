# 🧩 SafeHash  
### Privacy-First Image Fingerprinting to Combat Non-Consensual Image Sharing

SafeHash is a **privacy-preserving prototype** that demonstrates how **image hashing** can be used to detect duplicate uploads of sensitive content **without ever storing the images themselves**.

This project is motivated by the growing problem of **non-consensual image sharing, sextortion, and image-based abuse**, and explores how **hash-sharing systems** could help platforms detect and block re-uploads of harmful content at scale.

> ⚠️ **Disclaimer:** SafeHash is a student prototype built for learning and demonstration. It does not share data with any platform and is not a production system.

---

## 🚨 Why This Project Exists

Non-consensual image sharing and sextortion are rapidly increasing worldwide.  
Once an image is leaked, it can be re-uploaded repeatedly across platforms, making takedown efforts slow, emotionally damaging, and often ineffective.

A core challenge faced by platforms is:

- How do you **recognise known harmful images**
- **Without storing or redistributing the actual images**
- While respecting **privacy, consent, and legal constraints**

### 🔑 Core Idea

Instead of sharing images, platforms can share **cryptographic fingerprints (hashes)**.  
If a newly uploaded image matches a known harmful fingerprint, it can be flagged or blocked automatically.

**SafeHash demonstrates the engineering foundation of this idea.**

---

## 🧠 What SafeHash Does

SafeHash allows users to:

1. Upload an image through a web interface  
2. Generate **image fingerprints (hashes)**  
3. Store **only the hashes** in a database (no images)  
4. Detect if the **same image is uploaded again**  
5. Browse and export stored hashes for analysis or sharing  

---

## 🔐 Privacy-First Design

SafeHash is intentionally designed to minimise risk:

- ❌ No raw images are stored long-term  
- ✅ Only fixed-length hash values are persisted  
- ✅ Hashes cannot be reverse-engineered into images  
- ✅ Suitable for conceptual **hash-sharing** across platforms  

This design mirrors real-world trust & safety systems where **privacy is as important as detection**.

---

## ⚙️ How It Works (Technical Overview)

### 1️⃣ Image Upload
A user uploads an image via the Streamlit web interface.

### 2️⃣ Hash Generation
Two different hashes are computed:

#### 🔹 SHA-256 (Exact Match)
- Cryptographic hash of the raw file bytes  
- Detects **exact duplicates only**  
- Any change (resize, compression) produces a new hash  

#### 🔹 Perceptual Hash (pHash)
- Captures the **visual structure** of an image  
- Designed to survive resizing or compression  
- Enables future **near-duplicate detection**

### 3️⃣ Duplicate Detection
- If the SHA-256 hash already exists → **Exact duplicate detected**
- (Future work) If pHash distance is small → **Visually similar image detected**

### 4️⃣ Storage
- Hashes and metadata are stored in **SQLite**
- No image pixels are persisted

---

## 🧪 Current Features

- 📤 Image upload interface  
- 🔐 SHA-256 + perceptual hashing  
- 🚫 Exact duplicate detection  
- 🗄️ Hash database (“Hash Vault”)  
- 🔍 Search and inspect stored hashes  
- 📁 Export hashes as JSON or CSV  
- 🎨 Polished, demo-ready UI  

---

## 🧱 Tech Stack

| Component | Technology |
|--------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| Hashing | SHA-256, pHash |
| Image Processing | Pillow, ImageHash |
| Deployment | Streamlit Community Cloud |

---


---

## 🌍 Real-World Significance

Systems inspired by this approach are already used conceptually in:

- Image-based abuse prevention
- Sextortion and child-safety pipelines
- Copyright enforcement
- Platform trust & safety systems

SafeHash demonstrates how **engineering, ethics, and privacy** intersect in modern software design.

---

## 🚀 Future Work

This prototype can be extended to include:

- 🔁 Near-duplicate detection using pHash distance thresholds  
- 🤝 Secure hash-sharing APIs between platforms  
- 🔒 Encryption-at-rest for stored identifiers  
- 🧠 ML-based image embeddings for robustness testing  
- 📊 Precision / recall evaluation of detection accuracy  
- 🗑️ Auto-expiration and user-controlled deletion  

---

## 📌 Important Notes

- This app is for **educational and demonstration purposes only**
- Do **not** upload sensitive personal images to public deployments
- Any real deployment must follow strict legal and ethical guidelines

---

## 👤 Author

**Saksham Garg**  
Mechatronic Engineering — University of Sydney  
Portfolio Project (2026)

---

## ⭐ Demo

A live demo is available via Streamlit Cloud.  
(Database resets on redeploy — suitable for demonstrations.)



