# SecurePass Pro – Advanced Password Security Suite

**SecurePass Pro** is a high-fidelity, Python-based desktop security application designed to elevate digital credential management from simple random strings to an enterprise-grade security experience. By integrating advanced heuristics with a modern, high-DPI graphical interface, this tool empowers users to generate, analyze, and manage passwords with scientific precision.

---

## **Project Objective**

This project bridges the gap between basic utility scripts and professional security tools. It showcases a **Security-First Architecture** that performs real-time pattern matching, crack-time estimation, and mathematical entropy calculation, all wrapped in a sleek "Dark Mode" interface.

## **Advanced Features**

* **Intelligent Analysis Engine**: Uses the `zxcvbn` library to provide realistic crack-time estimations based on pattern matching against thousands of common credentials.
* **Scientific Security Metrics**: Dynamically calculates Shannon Entropy to quantify password complexity in real-time.
* **Modern GUI Architecture**: Built on `CustomTkinter` for a professional, high-DPI scaled, tabbed interface.
* **Visual Analytics**: Leverages `Matplotlib` to render live bar charts, allowing users to audit the security variance of their session data.
* **Zero-Touch Mobile Handoff**: Securely generates Base64-encoded QR codes using `pyqrcode` and `Pillow`, allowing for "scan-to-mobile" credential transfer without writing sensitive data to the disk.
* **Cryptographic Strength**: Employs the Python `secrets` module (CSPRNG) to ensure all generated passwords are cryptographically strong.

---

## **Requirements**

* Python 3.8+
* `customtkinter`
* `zxcvbn`
* `matplotlib`
* `pyqrcode`
* `pypng`
* `pillow`

## **Installation**

1. Clone this repository to your local machine.
2. Install the required dependencies:
```bash
pip install -r requirements.txt

```



## **How to Run**

```bash
python main.py

```

---

## **Application Manual**

1. **Generation Suite**: Select your security policy (e.g., Banking, Social Media) from the dropdown, then click "Generate."
2. **Security Dashboard**: Monitor the real-time strength meter. If a password fails the policy threshold, the system automatically regenerates it.
3. **Analytics**: Click the "Analytics" tab to view a visual comparison of your passwords' security scores.
4. **Secure Handoff**: Click the "QR Code" icon to render a secure handoff image for your mobile device.

## **Code Structure**

* **`main.py`**: The application bootloader; handles dependency validation and environment initialization.
* **`gui.py`**: The Controller layer; manages tabbed navigation and real-time UI updates.
* **`analyzer.py`**: The Security Engine; handles `zxcvbn` pattern matching and Shannon Entropy math.
* **`generator.py`**: The logic layer; handles platform-specific policy enforcement.
* **`dashboard.py`**: The Model layer; maintains session history and data persistence.
* **`analytics.py`**: The View layer; renders data-driven insights using Matplotlib.

---

## **Educational Goal**

This project demonstrates advanced **Object-Oriented Programming (OOP)**, **Event-Driven GUI design**, and **Data Visualization** in Python. It is designed to serve as a high-level template for students looking to move beyond simple scripts into building polished, enterprise-ready software.
