from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import os, json
from uuid import uuid4
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client, Client
import mimetypes


# Load environment variables
load_dotenv()

app = FastAPI()


# Constants
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Function to generate recipe
def generate_recipe(prompt: str, pdf_uri: str):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        result = model.generate_content(
            [prompt, pdf_uri],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "making_time": {"type": "string"},
                        "number_of_people_servings": {"type": "string"},
                        "ingredients": {"type": "array", "items": {"type": "string"}},
                        "instructions_to_make": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "title",
                        "description",
                        "making_time",
                        "number_of_people_servings",
                        "ingredients",
                        "instructions_to_make",
                    ],
                },
            ),
        )
        candidates = result.candidates
        if candidates:
            recipe_json = json.loads(candidates[0].content.parts[0].text)
        return recipe_json
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating recipe: {str(e)}"
        )


# Endpoint to upload image and generate recipe
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file locally
        file_id = str(uuid4())
        file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            raise ValueError("Could not determine the MIME type of the uploaded file.")

        # Upload image to Gemini API
        uploaded_image = genai.upload_file(file_path)

        # Create prompt for recipe generation
        prompt = (
            "Generate a recipe using the identified items in the image. "
            "Consider the ingredients and suggest a recipe with a title, "
            "description, preparation time, serving size, ingredients list, "
            "and detailed instructions."
        )

        # Generate recipe
        recipe = generate_recipe(prompt, uploaded_image.uri)
        os.remove(file_path)

        # Store recipe in Supabase
        data = {
            "file_id": file_id,
            "file_name": file.filename,
            "recipe_title": recipe["title"],
            "recipe_description": recipe["description"],
            "recipe_ingredients": recipe["ingredients"],
            "recipe_making_time": recipe["making_time"],
            "recipe_instructions_to_make": recipe["instructions_to_make"],
            "recipe_number_of_people_servings": recipe["number_of_people_servings"],
        }

        supabase.table("recipes").insert(data).execute()

        return JSONResponse(
            content={"message": "Recipe stored successfully!", "data": data},
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@app.get("/view-recipe/{id}")
async def view_recipe(id: int):
    try:
        # Fetch the recipe with the specified ID from the Supabase `recipes` table
        response = supabase.table("recipes").select("*").eq("id", id).execute()

        # Check if the recipe exists
        if not response.data:
            raise HTTPException(
                status_code=404, detail=f"Recipe with ID {id} not found"
            )

        # Return the fetched recipe
        recipe = response.data[0]  # There should be only one record with the given ID
        return JSONResponse(content={"recipe": recipe}, status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


@app.get("/view-all-recipes")
async def view_all_recipes():
    try:
        # Fetch all recipes from the Supabase `recipes` table
        response = supabase.table("recipes").select("*").execute()

        # Return the fetched recipes
        recipes = response.data
        return JSONResponse(content={"recipes": recipes}, status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


# 02bfde16-26cc-4236-8bb1-65369f2a91be - .sesskey
