# 🌊 BlueAlert - Smart Health Surveillance System

A comprehensive multi-page Streamlit dashboard for monitoring water-borne diseases in rural areas, developed for Smart India Hackathon 2024.

## 🚀 Features

### Multi-Page Architecture
- **🏠 Home**: Overview dashboard with key metrics and trends
- **📍 Disease Map**: Interactive map showing disease hotspots across Northeast India
- **📊 Analytics**: Comprehensive data analysis with charts and forecasting
- **💧 Water Quality**: Real-time sensor monitoring with alerts
- **🚨 Alerts**: Safety notifications and emergency response
- **📚 Education**: Health awareness and interactive learning

### Key Capabilities
- ✅ Real-time water quality monitoring (TDS, pH, Turbidity, Temperature)
- ✅ Interactive disease hotspot mapping with Folium
- ✅ Trend analysis and AI forecasting with Plotly
- ✅ Multi-level alert system with notification preferences
- ✅ Comprehensive health education with interactive quizzes
- ✅ Modern matte blue-cyan theme with card-based UI
- ✅ Mobile-responsive design with hover effects
- ✅ Persistent filters and session state management

## 📁 Project Structure

```
bluealert/
├── app.py                 # Main entry point with navigation
├── pages/
│   ├── home.py           # Overview dashboard
│   ├── map.py            # Interactive disease map
│   ├── charts.py         # Analytics and trends
│   ├── water_quality.py  # Water quality monitoring
│   ├── alerts.py         # Alert management
│   └── education.py      # Health education
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ 
- pip package manager

### Quick Start

1. **Clone or download the project files**
   ```bash
   # Create project directory
   mkdir bluealert-dashboard
   cd bluealert-dashboard
   
   # Copy all provided files to this directory
   # Ensure the pages/ folder contains all Python files
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv bluealert-env
   
   # Activate virtual environment
   # On Windows:
   bluealert-env\Scripts\activate
   
   # On Mac/Linux:
   source bluealert-env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 🔧 Configuration

### Mock Data
The application uses hardcoded mock data for demonstration:
- **Disease Cases**: Cholera, Typhoid, Diarrhea, Hepatitis A cases across Northeast India
- **Location Data**: 10 mock locations with coordinates for Assam, Mizoram, Meghalaya, etc.
- **Sensor Data**: Simulated IoT readings for TDS, pH, turbidity, temperature
- **Historical Trends**: Generated time series data with seasonal patterns

### Sensor Integration
To integrate real sensors, replace mock data in `pages/water_quality.py`:

```python
# Replace this mock code:
ss.sensor_data = {
    'TDS': 450,
    'Turbidity': 5.2,
    'Temperature': 28.5,
    'pH': 7.1
}

# With real API calls:
import requests

def fetch_sensor_data():
    try:
        # Arduino/ESP32 endpoint
        response = requests.get('http://192.168.1.100/api/sensors', timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"Sensor API error: {e}")
        return None

# Usage:
sensor_data = fetch_sensor_data()
if sensor_data:
    ss.sensor_data = sensor_data
```

### Arduino/ESP32 Integration Example

```cpp
// Arduino code example for water quality sensors
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// Sensor pins
#define TDS_PIN A0
#define TEMP_PIN 2     // DS18B20
#define TURBIDITY_PIN A1
#define PH_PIN A2

WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin("YOUR_WIFI", "PASSWORD");
  
  server.on("/api/sensors", HTTP_GET, handleSensors);
  server.begin();
}

void handleSensors() {
  StaticJsonDocument<200> doc;
  
  doc["tds"] = readTDS();
  doc["temperature"] = readTemperature();
  doc["turbidity"] = readTurbidity(); 
  doc["ph"] = readPH();
  doc["timestamp"] = millis();
  
  String response;
  serializeJson(doc, response);
  
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", response);
}

float readTDS() {
  // TDS sensor reading logic
  int rawValue = analogRead(TDS_PIN);
  return rawValue * 0.5; // Convert to ppm
}

// Implement other sensor reading functions...
```

## 🚀 Deployment Options

### 1. Streamlit Community Cloud
1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub and deploy
4. App will be available at `https://your-app.streamlit.app`

### 2. Heroku Deployment
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create bluealert-dashboard
git push heroku main
```

### 3. Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t bluealert .
docker run -p 8501:8501 bluealert
```

### 4. Vercel Deployment
Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

## 🧪 Testing

### Functionality Tests
- ✅ All pages load without errors
- ✅ Navigation works between pages  
- ✅ Filters persist across sessions
- ✅ Charts and maps render properly
- ✅ Mock data displays correctly
- ✅ Responsive design on mobile/desktop

### Performance Tests
- ✅ Page load time < 3 seconds
-