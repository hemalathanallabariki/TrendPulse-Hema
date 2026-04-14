# 📊 TrendPulse — What’s Actually Trending Right Now

TrendPulse is a data pipeline project that collects trending stories from Hacker News, cleans the data, performs analysis, and visualizes insights using Python.

---

## 🚀 Project Overview

This project is divided into 4 tasks:

* **Task 1 — Data Collection**
  Fetch top stories from Hacker News API, classify them into categories, and store them in a JSON file.

* **Task 2 — Data Cleaning**
  Load the raw JSON data, remove duplicates, handle missing values, and save a clean dataset as CSV.

* **Task 3 — Data Analysis**
  Perform statistical analysis using Pandas and NumPy and generate new insights.

* **Task 4 — Data Visualization**
  Create charts and a dashboard to visualize trends using Matplotlib.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Requests

---

## 📁 Project Structure

```
trendpulse/
│
├── task1_data_collection.py
├── task2_data_processing.py
├── task3_analysis.py
├── task4_visualization.py
│
├── data/
│   ├── trends_YYYYMMDD.json
│   ├── trends_clean.csv
│   └── trends_analysed.csv
│
├── outputs/
│   ├── chart1_top_stories.png
│   ├── chart2_categories.png
│   ├── chart3_scatter.png
│   └── dashboard.png
│
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the repository

```
git clone https://github.com/hemalathanallabariki/TrendPulse-Hema.git
cd TrendPulse-Hema
```

### 2. Install required libraries

```
pip install pandas numpy matplotlib requests
```

### 3. Run tasks in order

```
python task1_data_collection.py
python task2_data_processing.py
python task3_analysis.py
python task4_visualization.py
```

---

## 📊 Output

After running all tasks, you will get:

* Cleaned dataset (`trends_clean.csv`)
* Analysed dataset (`trends_analysed.csv`)
* Visual charts:

  * Top 10 stories
  * Category distribution
  * Score vs comments
* Final dashboard (`dashboard.png`)

---

## 📌 Key Features

* Categorizes real-world trending data using keyword matching
* Handles missing and inconsistent data
* Performs statistical analysis using NumPy
* Generates visual insights using charts
* End-to-end pipeline from raw data → insights

---

## 🧠 Learnings

* Working with APIs (Hacker News API)
* Data cleaning and preprocessing
* Data analysis using Pandas & NumPy
* Data visualization with Matplotlib
* Structuring a complete data pipeline project

---

## 📎 Note

Some categories may include dummy data if sufficient real stories are not available. This ensures consistent dataset size for analysis.

---

## 👩‍💻 Author

**Hema Latha Nallabariki**
Data Science Student

---

## ⭐ Final Thoughts

This project demonstrates a complete workflow of data collection, processing, analysis, and visualization — similar to real-world data science pipelines.
