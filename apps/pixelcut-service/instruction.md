# Pixelcut FastAPI Microservice

This is a simple FastAPI service that removes backgrounds from images using the Pixelcut API. You can also upscale the image or generate a new AI background if you want.

## What it does

- Upload an image (`.jpg`, `.png`, `.webp`, etc.)
- If it's `.webp`, it gets converted to `.jpg` for compatibility
- The image is uploaded to ImgBB to get a public link
- That link is sent to Pixelcut to remove the background
- You can also ask it to upscale or generate a new background
- You get the final image back as a PNG

## How to use

### 1. Install dependencies

```sh
pip install fastapi uvicorn python-dotenv pillow requests
```

### 2. Add your API keys

Create a `.env` file in this folder:

```
PIXELCUT_API_KEY=your_pixelcut_api_key
IMGBB_API_KEY=your_imgbb_api_key
```

### 3. Start the server

```sh
uvicorn main:app --reload --port 4000
```

### 4. Try it out

- Open [http://localhost:4000/docs](http://localhost:4000/docs) in your browser for a nice UI
- Or use curl:

```sh
curl -X POST -F "image=@your_image.webp" "http://localhost:4000/remove-bg?upscale=true&generate_background=true&background_scene=marble" --output result.png
```

## Options

- `upscale=true` — makes the image bigger and sharper
- `generate_background=true` — adds a new AI background (set `background_scene` if you want)
- `background_scene` — like `"marble"`, `"beach"`, etc.
- `prompt` and `negative_prompt` — for more control over the AI background

## Notes

- Your API keys need to be valid and have credits
- Temporary files are cleaned up automatically
- The result is always a PNG
