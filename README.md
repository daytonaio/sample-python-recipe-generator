# Sample Recipe Generator

This repository contains a sample project for a recipe generator application built using Python, FastAPI, Streamlit, Supabase, and Gemini. The application allows users to upload images of items in their refrigerator, analyzes the images, and provides recipe suggestions.

---

## 🚀 Getting Started

### Open Using Daytona

1. **Install Daytona**: Follow the [Daytona installation guide](https://www.daytona.io/docs/installation/installation/).
2. **Create the Workspace**:

   ```bash
   daytona create https://github.com/daytonaio/sample-python-recipe-generator
   ```

3. **Start the Application**:
   ```bash
   uvicorn main:app --reload
   streamlit run streamlit_app.py
   ```

---

### Prerequisites

1. **Install Dependencies**:  
   Ensure you have Python installed and run the following command to install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:  
   Create a `.env` file in the project root directory and add the following configurations:

   ```env
   # Configure Gemini API and Supabase
   SUPABASE_URL = "https://example.supabase.co"
   SUPABASE_KEY = "your_supabase_key"
   GEMINI_API_KEY = "your_gemini_key"
   ```

   Replace `https://example.supabase.co`, `your_supabase_key` and `your_gemini_key` with your actual Supabase and Gemini API url and keys.

3. **Set up Supabase**:  
   Create a table in your Supabase database using the following SQL query:
   ```sql
   CREATE TABLE recipes (
       id SERIAL PRIMARY KEY,
       file_id UUID NOT NULL,
       file_name TEXT NOT NULL,
       recipe_title TEXT NOT NULL,
       recipe_description TEXT NOT NULL,
       recipe_ingredients TEXT[] NOT NULL,
       recipe_making_time TEXT NOT NULL,
       recipe_instructions_to_make TEXT[] NOT NULL,
       recipe_number_of_people_servings TEXT NOT NULL
   );
   ```

---

### Backend Setup

To start the FastAPI backend, run:

```bash
uvicorn main:app --reload
```

---

### Frontend Setup

To start the Streamlit frontend, run:

```bash
streamlit run streamlit_app.py
```

---

### 📷 Screen Shots

![Screenshot 1](https://github.com/daytonaio/sample-python-recipe-generator/blob/main/images/Screenshot-1.png)

![Screenshot 2](https://github.com/daytonaio/sample-python-recipe-generator/blob/main/images/Screenshot-2.png)

![Screenshot 3](https://github.com/daytonaio/sample-python-recipe-generator/blob/main/images/Screenshot-3.png)

---

## ✨ Features

- **AI-Powered Recipe Suggestions**: Analyze uploaded images using Gemini to generate recipes.
- **Interactive UI**: Built with Streamlit for an intuitive user experience.
- **Database Integration**: Store recipe data in Supabase.
- **Modular Architecture**: Clean separation between backend and frontend.

---

This project demonstrates how to combine FastAPI, Streamlit, and Supabase with AI capabilities to build a practical application. Feel free to explore, modify, and enhance!
