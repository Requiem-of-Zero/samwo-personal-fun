# 📱 FamilyLedger

FamilyLedger is a sleek, dark-mode mobile app that helps families track and manage expenses collaboratively — from Amazon purchases to manual entries. Built with privacy, simplicity, and Apple-inspired minimalism in mind.

---

## 🚀 Features

- 🔐 Secure user authentication (Email/Password, Google, Apple)
- 👨‍👩‍👧‍👦 Family grouping with shared visibility
- 💳 Add/view manual or synced Amazon expenses
- 📊 Dashboard with smart spending insights
- ✉️ Invite family members by email
- 🔔 Customize notifications or mailing preferences

---

## 🧱 Tech Stack

| Layer       | Tech                            |
| ----------- | ------------------------------- |
| Frontend    | React Native (Expo)             |
| Auth        | JWT, OAuth (Google, Apple)      |
| Backend API | FastAPI (Python)                |
| Database    | PostgreSQL                      |
| ORM         | SQLAlchemy / SQLModel           |
| Scraping    | Playwright (Amazon integration) |
| Deployment  | EAS Build + Render/Railway      |

---

## 📂 Project Structure

backend/
├── app/
│ ├── models/ # ORM models (User, Family, Expense, etc.)
│ ├── routes/ # API endpoints
│ ├── services/ # Business logic (invites, mailers, auth)
│ └── main.py # FastAPI app entry point

mobile/
├── components/ # Reusable UI components
├── screens/ # Login, Dashboard, Transactions, etc.
└── App.tsx # Entry point

---

## 📦 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/nestledger.git
cd nestledger
```

### 2. Backend (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Mobile App (React Native with Expo)

```bash
cd mobile
npm install
npx expo start
```

## 🗂️ Key Models (UML Overview)

- User — credentials, preferences, family link

- Family — group container for multiple users

- Expense — amount, category, source (Amazon/manual)

- Category — user-defined or default

- Invite — tokenized family invites

- TransactionSource — flag for Amazon, receipts, etc.

- NotificationPreference — email/push options

## ✍️ Roadmap

- [x] Wireframes and dark minimalist design

- [x] UML diagram with extended classes

- [ ] FastAPI backend with full auth and models

- [ ] Connect React Native frontend via secure API

- [ ] Amazon transaction integration

- [ ] Push to TestFlight / App Store

---

Let me know if you want a `requirements.txt`, `package.json`, or backend starter scaffolding next.
