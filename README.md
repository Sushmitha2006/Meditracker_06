# 🩺 MediTracker - Beautiful Health Management System

A modern, beautiful health tracking application with medication reminders and caretaker alerts.

## ✨ Features

### 🎨 Beautiful 4-Page Layout
- **Login Page**: Modern authentication with gradient design
- **Todo Page**: Medication management and reminder testing
- **Medical Page**: Vital signs recording with health guidelines
- **Graph Page**: Beautiful data visualization with summary cards

### 💊 Smart Medication Management
- Add medications with specific timing (e.g., "09:00,21:00")
- Toggle medication active/inactive status
- Delete medications when no longer needed
- Test reminder notifications

### 🔔 Intelligent Reminder System
- **Popup Notifications**: Beautiful modal popups at scheduled times
- **10-Minute Timer**: Countdown timer with visual feedback
- **Confirmation System**: "I've Taken It" button to confirm medication
- **Caretaker Alerts**: Automatic email alerts to caretakers after 10 minutes

### 📊 Beautiful Data Visualization
- **Summary Cards**: Quick overview of average vital signs
- **Interactive Charts**: Heart rate, blood pressure, blood sugar trends
- **Responsive Design**: Optimized for all screen sizes
- **Health Guidelines**: Built-in reference for normal ranges

### 🏥 Comprehensive Health Tracking
- Heart rate monitoring with status indicators
- Blood pressure tracking (systolic/diastolic)
- Blood sugar level monitoring
- Oxygen saturation tracking
- Real-time health status feedback

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🎯 How the Reminder System Works

1. **Schedule**: Add medications with specific times (24-hour format)
2. **Remind**: Beautiful popup appears at scheduled time
3. **Confirm**: Patient clicks "I've Taken It" to confirm
4. **Alert**: If no confirmation within 10 minutes, caretaker gets email alert

## 🎨 Design Features

- **Modern UI**: Glassmorphism design with gradients and shadows
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Animations**: Smooth transitions and hover effects
- **Color Coding**: Health status indicators with appropriate colors
- **Typography**: Clean, readable fonts with proper hierarchy

## 📱 Pages Overview

### Login Page
- Beautiful authentication form
- Toggle between login and registration
- Gradient background with glassmorphism cards

### Todo Page
- Medication management interface
- Reminder testing system
- Active/inactive medication status

### Medical Page
- Vital signs input form
- Real-time health status indicators
- Built-in health guidelines

### Graph Page
- Summary cards with key metrics
- Interactive charts and graphs
- Data visualization with Chart.js

## 🔧 Technical Stack

### Frontend
- React 18
- Chart.js & React-ChartJS-2
- Modern CSS with animations
- Axios for API calls

### Backend
- Flask
- SQLAlchemy
- APScheduler for reminders
- Email notifications

## 📧 Caretaker Alert System

When a patient misses a medication reminder:
1. Popup appears at scheduled time
2. 10-minute countdown timer starts
3. If no confirmation received:
   - Email sent to caretaker
   - Alert includes patient details and medication info
   - Emergency contact information provided

## 🎨 UI/UX Highlights

- **Glassmorphism**: Modern translucent design elements
- **Gradient Backgrounds**: Beautiful color transitions
- **Card-based Layout**: Clean, organized information display
- **Interactive Elements**: Hover effects and smooth transitions
- **Status Indicators**: Color-coded health status feedback
- **Responsive Grid**: Adapts to any screen size

## 📊 Data Visualization

- **Summary Cards**: Quick health overview
- **Line Charts**: Trend analysis over time
- **Bar Charts**: Comparative data display
- **Doughnut Charts**: Status distribution
- **Real-time Updates**: Live data refresh

## 🔐 Security Features

- Patient data protection
- Secure authentication
- Caretaker contact verification
- Data validation and sanitization

## 📈 Future Enhancements

- Push notifications
- SMS alerts
- Mobile app
- Doctor dashboard
- Health reports
- Medication interactions

---

**MediTracker** - Making health management beautiful and intuitive! 🌟