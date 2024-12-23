import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"  # Update if deployed

st.set_page_config(page_title="Recipe Finder", layout="wide")


def upload_image():
    st.header("Upload an Image to Generate a Recipe")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        if st.button("Scan for Recipe"):
            with st.spinner("Uploading and processing..."):
                try:
                    # Call the /upload-image API
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    }
                    response = requests.post(
                        f"{API_BASE_URL}/upload-image", files=files
                    )

                    if response.status_code == 200:
                        recipe_data = response.json().get("data", {})
                        st.success("Recipe Generated Successfully!")
                        display_recipe(recipe_data)
                    else:
                        st.error(
                            f"Error generating recipe: {response.json().get('detail', 'Unknown error')}"
                        )

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


def view_all_recipes():
    st.header("All Recipes")
    response = requests.get(f"{API_BASE_URL}/view-all-recipes")

    if response.status_code == 200:
        recipes = response.json().get("recipes", [])
        if not recipes:
            st.warning("No recipes found.")
            return

        for recipe in recipes:
            with st.expander(recipe["recipe_title"]):
                st.write(f"**Description:** {recipe['recipe_description']}")
                st.write(f"**Making Time:** {recipe['recipe_making_time']}")
                st.write(f"**Servings:** {recipe['recipe_number_of_people_servings']}")
                if st.button("View Full Recipe", key=f"view_{recipe['id']}"):
                    view_recipe(recipe["id"])
    else:
        st.error("Error fetching recipes!")


def view_recipe(recipe_id):
    response = requests.get(f"{API_BASE_URL}/view-recipe/{recipe_id}")

    if response.status_code == 200:
        recipe = response.json().get("recipe", {})
        display_recipe(recipe)
    else:
        st.error("Error fetching recipe details!")


def display_recipe(recipe):
    st.header(recipe["recipe_title"])
    st.write(f"**Description:** {recipe['recipe_description']}")
    st.write(f"**Making Time:** {recipe['recipe_making_time']}")
    st.write(f"**Servings:** {recipe['recipe_number_of_people_servings']}")

    st.subheader("Ingredients")
    st.write("\n".join(recipe["recipe_ingredients"]))

    st.subheader("Instructions")
    for step in recipe["recipe_instructions_to_make"]:
        st.write(f"- {step}")


# Main UI
st.title("🍴 Recipe Finder")

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Upload Image", "View All Recipes"], index=0)

if page == "Upload Image":
    upload_image()
elif page == "View All Recipes":
    view_all_recipes()
