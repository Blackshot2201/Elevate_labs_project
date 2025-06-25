# Elevate_labs_project
# 🔐 Encrypted Keylogger with GUI

A GUI-based keylogger with military-grade encryption, designed **for educational purposes** and **authorized penetration testing** only. The application allows real-time control, encrypted data handling, and stealth features, all managed through an intuitive graphical interface.

---

## 📜 Table of Contents

* [Project Description](#project-description)
* [Features](#features)
* [Screenshots](#screenshots)
* [Prerequisites](#prerequisites)
* [Installation Guide](#installation-guide)
* [Usage Instructions](#usage-instructions)
* [Technical Specifications](#technical-specifications)
* [Security Implementation](#security-implementation)
* [Troubleshooting](#troubleshooting)
* [Development Roadmap](#development-roadmap)
* [Ethical Considerations](#ethical-considerations)
* [License](#license)

---

## 📌 Project Description

This project is a **graphical keylogger with encrypted logging** capabilities. Built for educational use and ethical hacking labs, it ensures all recorded keystrokes are safely stored using **AES encryption**. It features a **stealth mode**, kill switch, and secure log management tools.

---

## ✨ Features

* 🔐 **Advanced Encryption**

  * AES-128 CBC using Fernet
* 🖥️ **GUI Controls**

  * Start / Stop / Save / Exfiltrate buttons
* 🕶️ **Stealth Operations**

  * Optional Windows persistence
  * Kill switch (3x ESC) to wipe & halt
* 🗂️ **Data Management**

  * Timestamped logs
  * Encrypted local files
  * Simulated data exfiltration
* 🛡️ **Safety Mechanisms**

  * Emergency key wipe (3x ESC)
  * Secure key storage (`keylogger_key.key`)

---

## 🖼️ Screenshots

> 📌 *Add actual screenshots in your repo's ******************************************`/screenshots/`****************************************** folder and reference below*

* **Main Interface:** Shows logging status, controls
* **Log Example:** Shows sample encrypted data

---

## 📋 Prerequisites

* Python 3.8 or above
* Administrator/root privileges (for persistence)
* \~50MB disk space

---

## 🛠️ Installation Guide

### 📦 Method 1: PIP Installation

pip install encrypted-keylogger&#x20;

### 💻 Method 2: Manual Setup

git clone [https://github.com/yourusername/encrypted-keylogger.git](https://github.com/yourusername/encrypted-keylogger.git)

cd encrypted-keylogger

python setup.py install

### 🔗 Dependencies

`pip install -r requirements.txt`

---

## 🎯 Usage Instructions

### 🚀 Launch

`python keylogger.py`

### 🕹️ Controls

* 🟢 **Start** — Begin keystroke logging
* 🔴 **Stop** — Pause logging
* 💾 **Save** — Encrypt & save logs
* 📤 **Exfiltrate** — Simulate sending encrypted logs

### ⚙️ Advanced Features

#### 🔁 Enable Persistence (Admin Required)

In `keylogger.py`:

`# Uncomment this line: app.add_startup_persistence()`

#### 🆘 Kill Switch (3x ESC)

* Stops keylogger
* Securely wipes logs
* Pauses further execution

---

## ⚙️ Technical Specifications

### 🔄 Data Flow

`[Keyboard Input] → [Timestamp] → [AES Encryption] → [Local Storage] ↳ [Simulated Exfiltration]`

### 🔐 Encryption

* AES-128 CBC mode (via Fernet)
* Key File: `keylogger_key.key` (Base64 encoded)
* Key Permissions: `600`
* Padding: PKCS7
* Key rotation: Manual

---

## 🔒 Security Implementation

* **Key Management:**

  * 256-bit key in base64
  * Enforced file permissions
* **Data Protection:**

  * Logs never stored in plaintext
  * In-memory encryption
  * Emergency memory wipe via kill switch

---

## 🐛 Troubleshooting

| ProblemSolution   |                                    |
| ----------------- | ---------------------------------- |
| Import Errors     | `pip install -r requirements.txt`  |
| Permission Denied | Run as `admin` or with `sudo`      |
| Kill Switch Fails | Press ESC 3 times **fast**         |
| Key File Missing  | Delete old file to auto-regenerate |

---

## 🗺️ Development Roadmap

### ✅ Next Version

* Multi-platform persistence
* Encrypted network exfiltration
* Behavior-based alerts

### 🔮 Planned Features

* 🌍 Geofencing triggers
* ☁️ Cloud backup (optional)
* 🛡️ Anti-debugging layers

---

## ⚠️ Ethical Considerations

> **LEGAL DISCLAIMER**

This project is intended **only for**:

* ✅ Educational use
* ✅ Personal device monitoring
* ✅ Authorized penetration testing

**You are strictly prohibited** from:

* ❌ Unauthorized keylogging
* ❌ Credential harvesting
* ❌ Illegal surveillance

> 🛑 **You are solely responsible for your actions. Use ethically and legally.**

---

---

## 🪪 License

This project is released under the **MIT License**. Refer to `LICENSE` file for details.
