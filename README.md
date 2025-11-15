# 🏥 Real-Time Patient Flow Streaming System - Author: Franco Amigo
### *Apache Kafka · PostgreSQL · Streamlit · Python*

This project implements a real-time data streaming pipeline simulating **patient flow in a hospital**, using Kafka for event streaming, PostgreSQL for storage, and Streamlit for interactive visualization.  
It is based on the original real-time e-commerce pipeline from the Demo, but adapted to the **healthcare domain**.

---

## 📌 1. Overview

This system simulates patient visits to a hospital , streams the events in real time through **Apache Kafka**, stores them in **PostgreSQL**, and displays a live, auto-updating **dashboard** in Streamlit.

Each event represents a patient's interaction with the emergency department workflow, including:

- Patient status (Waiting, In Treatment, Discharged, etc.)
- Hospital specialty (Cardiology, Trauma, emergency)
- Waiting time (minutes)
- Triage level (1–5)
- Insurance type
- Timestamp of arrival

The **dashboard updates every few seconds** to visualize current hospital load and operational metrics.

![ezgif-73782fc49bb9e8ad](https://github.com/user-attachments/assets/5302d709-2e0a-46c4-a303-e85d65762682)


---

## 📐 2. System Architecture

```
┌──────────────────┐        ┌──────────────────┐        ┌─────────────────────────┐
│  Patient Event    │        │      Kafka       │        │      PostgreSQL         │
│    Producer       │──────▶ │   (Topic:        │ ─────▶ │    patient_events       │
│ (Python + Faker)  │        │  patient_events) │        │   structured storage     │
└──────────────────┘        └──────────────────┘        └─────────────────────────┘
                                                                │
                                                                ▼
                                                     ┌──────────────────────┐
                                                     │    Streamlit         │
                                                     │  Real-Time Dashboard │
                                                     └──────────────────────┘
```

---

## 🛠️ 3. Tech Stack

- **Kafka** – real-time event streaming  
- **Python** – producer, consumer, and dashboard logic  
- **Faker** – synthetic patient event generation  
- **PostgreSQL** – persistence layer  
- **SQLAlchemy** – database connection for Streamlit  
- **Streamlit** – real-time visualization UI  
- **Plotly** – interactive charts  

---

## 🧬 4. Data Model (patient_events table)

| Column          | Type             | Description |
|-----------------|------------------|-------------|
| `event_id`      | VARCHAR(50)      | Unique patient event identifier |
| `status`        | VARCHAR(50)      | Patient status (Waiting, Discharged, etc.) |
| `specialty`     | VARCHAR(50)      | Medical specialty (Emergency, Cardiology…) |
| `waiting_time`  | NUMERIC(10,2)    | Minutes from arrival to being seen |
| `timestamp`     | TIMESTAMP        | Event timestamp |
| `hospital_name` | VARCHAR(100)     | Fixed: “General Hospital” |
| `insurance`     | VARCHAR(50)      | Insurance type (Medicare, Medicaid…) |
| `triage_level`  | INTEGER          | Triage severity level (1–5) |

---

## 🧪 5. Components

### ✔️ **1. patient_event_producer.py**
Generates synthetic hospital events and streams them into Kafka (`patient_events` topic).

### ✔️ **2. patient_event_consumer.py**
Subscribes to the Kafka topic and inserts events into PostgreSQL.  
Automatically creates the `patient_events` table if it does not exist.

### ✔️ **3. dashboard.py**
Displays real-time KPIs and charts:
- Total patient events
- Average waiting time
- Average triage level
- Number of patients in treatment
- Number of discharges
- Events by specialty
- Triage level distribution  
- Table of most recent events

---

## 🚀 6. How to Run the System

### **Start Kafka & Zookeeper**
```bash
docker compose up -d
```

### **Start PostgreSQL**
Ensure PostgreSQL is running on:
```
host=localhost
port=5433
user=kafka_user
password=kafka_password
database=kafka_db
```

### **Start the Consumer**
```bash
python patient_event_consumer.py
```

### **Start the Producer**
```bash
python patient_event_producer.py
```

### **Start the Dashboard**
```bash
streamlit run dashboard.py
```
Open:
```
http://localhost:8501
```

---

## 📊 7. Screenshot Docker

<img width="1642" height="427" alt="image" src="https://github.com/user-attachments/assets/373d3c08-eda3-44a2-9fbb-2cc32cf25b3c" />




