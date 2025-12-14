# Security Policy for PocketChef

Thank you for using and contributing to **PocketChef**!  
This document outlines how security vulnerabilities should be reported, how we handle them, and what you can expect from the response process.

---

## 📬 Reporting a Security Vulnerability

If you discover a security vulnerability in this project, we ask that you **report it privately and responsibly** to give us a chance to address it before it’s publicly disclosed.

### How to report:
1. **Email us** at:  
   `security@pocketchef.online`  
2. Or use **GitHub Security Advisories**:  
   https://github.com/JoshuaDonnelly/GCA2-IoT-PocketChef/security/advisories

> ⚠ **Do not** open a public GitHub issue or pull request for security vulnerabilities — this could expose sensitive details before a fix is available. :contentReference[oaicite:1]{index=1}

### What to include in your report:
- A clear description of the issue
- Steps to reproduce the problem
- Any logs, screenshots or proof-of-concept code
- The impact and severity (if known)

---

## ⏱ Response & Communication Timeline

We take security reports seriously and aim to respond in a timely manner:

| Stage | Target Timeframe |
|-------|------------------|
| Acknowledge receipt | Within **3 business days** |
| Initial assessment | Within **7 business days** |
| Proposed fix / next steps | Within **14 business days** |

We will coordinate with you, especially if you are the reporter, to ensure the issue is resolved securely and efficiently.

---

## 🛠 Supported Versions

We maintain and support the **latest release** on the `main` branch of this project.  
Please make sure you are running the most recent version before reporting an issue.

---

## 🔐 Security Best Practices for Users & Developers

While using or contributing to this project, please follow these general IoT and repository security guidelines:

### 📌 Development & Repo Security
- Avoid committing **secrets** (API keys, credentials, etc.) — scan the repo before publishing.
- Enable GitHub features like **Dependabot alerts**, **branch protection** and **secret scanning** if possible.
- Review dependency security regularly and update when vulnerabilities are discovered.

### 🔒 IoT-Specific Practices
Since this project involves IoT concepts and potentially connected hardware or network services, consider the following common security practices:
- Use **strong authentication mechanisms** for connected services.
- Encrypt all communication channels (e.g., HTTPS, MQTT over TLS).
- Regularly update firmware and software components to patch security issues. :contentReference[oaicite:3]{index=3}
- Don’t expose administrative interfaces or unnecessary ports externally.
- Apply the **principle of least privilege** in configurations and access controls. :contentReference[oaicite:4]{index=4}

---

## 📣 Responsible Disclosure & Public Communication

Once a security vulnerability is addressed:
- We may publish a **security advisory** detailing the issue and resolution.
- The disclosure will coordinate with the reporter if they are willing.

For critical vulnerabilities, we may use **coordinated disclosure** practices to ensure users have time to update before details are widely posted.

---

Thank you for helping keep **PocketChef** safe and secure! 💪
