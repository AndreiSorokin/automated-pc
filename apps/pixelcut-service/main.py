import os
import requests
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
import tempfile
import base64

# Load environment variables from .env file
load_dotenv()

PIXELCUT_API_KEY = os.getenv("PIXELCUT_API_KEY")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_to_imgbb(image_path: str) -> str:
    with open(image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode("utf-8")
    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY, "image": encoded_image}
    )
    if resp.status_code != 200:
        raise Exception(f"ImgBB upload failed: {resp.text}")
    return resp.json()["data"]["image"]["url"]

@app.post("/remove-bg")
async def remove_bg(
    image: UploadFile = File(...),
    upscale: bool = Query(False),
    generate_background: bool = Query(False),
    background_scene: str = Query("marble"),
    prompt: str = Query(""),
    negative_prompt: str = Query("")
):
    # Save uploaded file to a temp file
    suffix = os.path.splitext(image.filename)[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await image.read())
        tmp_path = tmp.name

    # Convert webp to jpg if needed
    if suffix == ".webp":
        jpg_path = tmp_path.replace(".webp", ".jpg")
        with Image.open(tmp_path) as im:
            im = im.convert("RGB")
            im.save(jpg_path, format="JPEG")
        os.remove(tmp_path)
        tmp_path = jpg_path

    try:
        # Upload to ImgBB
        image_url = upload_to_imgbb(tmp_path)

        # Remove background with Pixelcut
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-KEY": PIXELCUT_API_KEY
        }
        payload = {
            "image_url": image_url,
            "format": "png"
        }
        pixelcut_resp = requests.post(
            "https://api.developer.pixelcut.ai/v1/remove-background",
            headers=headers,
            json=payload
        )
        if pixelcut_resp.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"error": f"Pixelcut API failed: {pixelcut_resp.text}"}
            )
        result = pixelcut_resp.json()
        output_url = result.get("result_url")
        if not output_url:
            return JSONResponse(
                status_code=500,
                content={"error": "No result_url from Pixelcut"}
            )

        # Optionally upscale
        if upscale:
            upscale_payload = {
                "image_url": output_url,
                "scale": 2
            }
            upscale_resp = requests.post(
                "https://api.developer.pixelcut.ai/v1/upscale",
                headers=headers,
                json=upscale_payload
            )
            if upscale_resp.status_code == 200:
                upscaled_url = upscale_resp.json().get("result_url")
                if upscaled_url:
                    output_url = upscaled_url

        # Optionally generate background
        if generate_background:
            gen_payload = {
                "image_url": output_url,
                "image_transform": {
                    "scale": 1.0,
                    "x_center": 0.5,
                    "y_center": 0.5
                },
                "scene": background_scene,
                "prompt": prompt,
                "negative_prompt": negative_prompt
            }
            gen_resp = requests.post(
                "https://api.developer.pixelcut.ai/v1/generate-background",
                headers=headers,
                json=gen_payload
            )
            if gen_resp.status_code == 200:
                gen_url = gen_resp.json().get("result_url")
                if gen_url:
                    output_url = gen_url

        # Download and return the final image
        img_data = requests.get(output_url).content
        return Response(content=img_data, media_type="image/png")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
