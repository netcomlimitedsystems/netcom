cybersecurity and software development website
# Netcom Learning Website

A modern **e-learning platform** built with **Django 4**, featuring:
- User authentication (login, registration, profiles, account settings)
- Courses with lessons, enrollments, and difficulty levels
- Blogs with categories and images
- Admin dashboard with charts (using Chart.js)
- Responsive UI styled with **Bootstrap 5**
- Guest vs authenticated views using conditional rendering in `base.html`

---

## 🚀 Features

- **Authentication**
  - User registration, login, and logout
  - Profile with avatar, bio, and account settings
  - Change password & delete account (with confirmation)

- **Courses**
  - Categories: Cybersecurity, Software Development, Cloud, DevOps
  - Lessons with content, video links, and duration
  - User enrollment tracking
  - Search and filter by category & difficulty

- **Blog**
  - Rich blog posts with categories
  - Upload images for posts
  - Author-linked posts with timestamps

- **Admin Dashboard**
  - Manage users, courses, lessons, enrollments, and blogs
  - Visual analytics with **Chart.js**
  - Clean UI styled with Bootstrap

- **Responsive Design**
  - Guest-friendly landing pages
  - Authenticated users see sidebar navigation
  - Dark theme for cybersecurity feel

---

## 🛠️ Tech Stack

- **Backend:** Django 4.2
- **Frontend:** Bootstrap 5 + Chart.js (via CDN)
- **Database:** SQLite (default) / PostgreSQL (production)
- **Image Handling:** Pillow
- **Forms:** django-crispy-forms + crispy-bootstrap5

---

## 📦 Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/netcomlimitedsystems/netcom.git
   cd netcom
