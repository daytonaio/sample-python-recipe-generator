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

## Set Up Supabase

3. Configure Supabase for the application:

- Create a Supabase project and note down the `URL` and `Key`.
- Use the following SQL command to set up the required database table:

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

## Set Environment Variables

4. Create a `.env` file in the root directory of the project and add the following configurations:

```env
SUPABASE_URL="https://example.supabase.co"
SUPABASE_KEY="your_supabase_key"
GEMINI_API_KEY="your_gemini_key"
```

Replace the placeholders with your actual Supabase `URL`, `Key`, and Gemini `API Key`.

---

## Run the App

5. Start the application by running the backend and frontend separately.

### Backend

Run the FastAPI backend:

```bash
uvicorn main:app --reload
```

### Frontend

Run the Streamlit frontend:

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
