# 🛍️ GenieCart ML Recommendation Engine

A sophisticated machine learning-based recommendation system that provides personalized product suggestions based on user preferences, purchase history, and product attributes.

## 🎯 Overview

The GenieCart ML Recommendation Engine analyzes user behavior and product characteristics to generate tailored product recommendations. It employs an advanced scoring algorithm that considers multiple factors to provide the most relevant suggestions.

## ✨ Key Features

🏷️ **Price-Level Based Matching**
- Categorizes products into high-end, middle, and low-end segments.
- Intelligently matches products to user preferences and budget.

⭐ **Rating-Based Scoring**
- Incorporates product ratings with configurable weight factors.
- Prioritizes highly-rated items in recommendations.

🔍 **Tag-Based Similarity**
- Analyzes product tags and attributes.
- Finds items matching user preferences and interests.

📊 **Purchase History Analysis**
- Learns from user's previous purchases.
- Continuously improves recommendation accuracy.

📦 **Availability Checking**
- Ensures recommended products are in stock.
- Maintains real-time inventory tracking.

💱 **Multi-Currency Support**
- Seamless handling of USD and LKR.
- Automatic currency conversion.

## 🏗️ System Architecture

### 1️⃣ Data Processing Layer
**ItemDataConvertor.py**
- Handles CSV to object conversion.
- Processes product attributes.
- Manages price conversions.
- Generates and normalizes product tags.

**MachineCustomerItemDataConvertor.py**
- Creates machine customer profiles.
- Processes user preferences.
- Handles purchase history integration.

### 2️⃣ Core Recommendation Engine
**Model.py**
- Implements the scoring algorithm.
- Manages price level categorization.
- Processes tag matching.
- Calculates final recommendation scores.

### 3️⃣ Database Layer
**Database.py**
- Manages MySQL connections.
- Handles customer authentication.
- Stores and retrieves purchase history.
- Manages search results.

### 4️⃣ Configuration
**consts.py**
- Defines price level thresholds.
- Sets scoring weights.
- Configures availability thresholds.
- Defines currency conversion rates.

## 📚 API Documentation

### Recommendation Endpoint
**URL**: `/recommend`  
**Method**: `POST`  
**Content-Type**: `application/json`

### Request Format
```json
{
    "secret_key": "your_secret_key_here",
    "item_name": "A4 bundle", 
    "custom_domains": ["https://www.amazon.com"],
    "price_level": 3, 
    "tags": ["white","photocopy","a4"]
}
```

### Response Format
- **Success**: Returns a success status.
- **Error**: Returns an error message with status code.

## 🛠️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Project_GenieCart/ML-model
   ```

2. **Install dependencies**:
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install
   ```