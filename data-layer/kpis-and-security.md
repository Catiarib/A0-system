# A·0 Data Strategy: KPIs, Measurement & Security Framework

This document defines how **A·0** captures, measures, and protects the intelligence generated within immersive experiences.

---

## I. Key Performance Indicators (KPIs)

To validate the success of an A·0 deployment, we track three categories of metrics:

### 1. Engagement Metrics (Audience Intelligence)
*   **Average Dwell Time (ADT):** Mean time spent by visitors in specific zones.
*   **Zone Conversion Rate:** % of visitors who move from one experience zone to the next (e.g., Threshold → Immersion).
*   **High-Engagement Index:** % of audience remaining in a "Hero Zone" for >30 seconds.
*   **Interaction Velocity:** Frequency of sensor activations per minute during peak times.

### 2. Operational Metrics (System Efficiency)
*   **System Latency:** Time (ms) between sensor detection and visual/light output (Target: <150ms).
*   **Deployment Lead Time:** Hours required from site arrival to full system operation.
*   **Module Reusability Score:** % of software/hardware logic repurposed from previous editions.
*   **Trigger Accuracy:** Precision of LiDAR/PIR detection vs. actual physical movement.

### 3. Business & ROI Metrics (Client Value)
*   **Lead Generation Conversion:** % of visitors interacting with the data exit point (QR/NFC).
*   **Cost per Impression (CPI):** Total project cost divided by total validated visitor count.
*   **Adaptive Optimization Lift:** % increase in dwell time when using adaptive lighting (M02) vs. static lighting.

---

## II. Data Acquisition & Methodology

### 1. The Collection Stack (Hardware to Cloud)
*   **Sensors (M08):** LiDAR (spatial tracking), PIR (occupancy), and Computer Vision (anonymized crowd heatmaps).
*   **A·0 Edge Node:** Raspberry Pi / Industrial PC processing real-time telemetry via MQTT or WebSocket.
*   **REST API Bridge:** Structured data sent from the experience site to the SQL Data Layer.

### 2. Processing & Visualization
*   **ETL Pipeline:** Python scripts cleaning and transforming raw telemetry into time-series data.
*   **SQL Storage:** PostgreSQL database storing historical logs and case-based precedents.
*   **Analytics Dashboard (M09):** Real-time Power BI reporting for stakeholders.

---

## III. Data Security & Protection Measures

A·0 follows a "Privacy by Design" approach to ensure GDPR compliance and protect client intellectual property.

### 1. Data Anonymization & Privacy
*   **PII Hashing:** No Personal Identifiable Information (PII) is stored. Computer vision modules use skeletal tracking or heatmaps rather than facial recognition.
*   **GDPR Compliance:** All visitor data is aggregated. No individual profiles are created unless the visitor explicitly opts-in via the Lead Gen module.

### 2. Data in Transit & at Rest
*   **Transport Layer Security (TLS):** All data sent from the experience site to the cloud is encrypted via TLS 1.3.
*   **Encryption at Rest:** Databases are encrypted using AES-256 standards.
*   **Isolated Infrastructure:** Local experience networks are air-gapped or protected via VPNs to prevent unauthorized external access.

### 3. Access Control (RBAC)
*   **API Authentication:** Every module (M01-M10) communicates via signed API tokens.
*   **Role-Based Access Control:** Stakeholders only have access to aggregated reports, while technical operators have access to system logs.
*   **Audit Logging:** Every system change or data access event is logged and timestamped.

---

**"Converting Art into Data, Protected by System."**
*A·0 / Narrative · Light · Space / Barcelona 2026*
