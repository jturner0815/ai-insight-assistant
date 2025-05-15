# AI Insight Assistant 🧠📊

A secure, branded, client-facing AI insight assistant powered by Groq and built with Flask. This app allows users to upload CSV data, receive AI-generated insights, and download the results in PDF or TXT format — all behind a login system with prompt logging.

 
*https://ai-insight-assistant.onrender.com*

---

## 🚀 Features

- 🔐 **User Authentication** – Register, log in, and logout with password hashing
- 📁 **CSV Upload** – Upload data to preview and analyze
- 🧠 **Groq AI Integration** – Generate 3 smart insights using Llama 3
- 🧾 **PDF & TXT Download** – Export the AI response to share with others
- 📓 **Prompt Logging** – Records user, prompt, and response to CSV
- 🧼 **Clean UI** – Custom logo, background pattern, and soft styling
- 🌐 **Deployed on Render** – Easily accessible to clients and users

---

## 🖼 Screenshots

> Add screenshots of the login page, dashboard, insight output, and PDF

---

## ⚙️ Tech Stack

- **Flask** + **Flask-Login**
- **Groq API** – Llama 3 (8B)
- **Gunicorn** for production
- **Render.com** deployment
- **xhtml2pdf** for PDF export

---

## 🔧 Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-insight-assistant.git
cd ai-insight-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch .env
# Add: GROQ_API_KEY=your_actual_key
python app.py
```

---

## 📁 Folder Structure

```
ai-insight-assistant/
├── app.py
├── logger.py
├── pdf_exporter.py
├── requirements.txt
├── render.yaml
├── templates/
│   ├── login.html
│   ├── register.html
│   └── index.html
├── static/
│   ├── logo1.png
│   ├── pattern.png
│   └── insight.pdf
```

---

## 🛡 Security Notes

- Passwords are hashed with Werkzeug
- `.env` is used for secret API keys
- `.gitignore` excludes sensitive and runtime files

---

## 📜 License

MIT License

---

## 🙌 Built by [@jturner0815](https://github.com/jturner0815)

