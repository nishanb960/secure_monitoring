# 🔒 Campus Security Monitor

A powerful, real-time security monitoring system designed specifically for educational campuses to enhance safety, track incidents, and manage access control across multiple locations.

## 🎯 Key Features

### Real-Time Monitoring
- **Live Camera Feeds**: Centralized surveillance feed from all campus cameras
- **Active Cameras Count**: Real-time tracking of operational cameras
- **System Health Status**: Green/Yellow/Red status indicators
- **Multi-Campus Support**: Monitor security across all campuses from one dashboard

### Security Event Management
- **Unauthorized Access Detection**: Real-time alerts for security breaches
- **Event Logging**: Complete history of security incidents
- **Today's Events Counter**: Daily incident tracking
- **Event Filtering**: Categorize by severity, type, and location

### Access Control
- **User Authentication**: Secure login system for security personnel
- **Role-Based Access**: Admin, Security Guard, Manager roles
- **Activity Logging**: Track all user actions

### Dashboard Analytics
- **Security Metrics**: Live statistics and KPIs
- **Incident Reports**: Generate detailed security reports
- **Trend Analysis**: Identify security patterns over time

## 🚀 Technology Stack

- **Backend**: Django 5.2 (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time Features**: Django Channels / WebSockets (optional)
- **Database**: PostgreSQL / SQLite
- **Authentication**: Django Auth System
- **UI Framework**: Custom responsive design

## 📊 Dashboard Components

### Statistics Cards
- **Active Cameras**: Count of operational surveillance cameras
- **Today's Events**: Number of security events today
- **Unauthorized Access**: Count of access violations
- **System Status**: Real-time system health indicator

### Live Monitoring Feed
- Grid view of active camera feeds
- Camera status indicators
- Quick access to full-screen view
- Timestamp overlays

### Recent Security Events
- Real-time event feed
- Event severity indicators (High/Medium/Low)
- Location and time information
- Quick action buttons

## 🔧 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/campus-security-monitor.git

# Navigate to project
cd campus-security-monitor

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure database
python manage.py migrate

# Create security admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver 2000
