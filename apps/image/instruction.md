# GPT-5 Product Card Microservice

This microservice generates e-commerce product cards using OpenAI's GPT-5 image model (`gpt-image-1`).  
It can:

- Remove product backgrounds
- Enhance/upscale images
- Compose products onto new backgrounds
- Add title and description text
- Return a complete product card image

## Features

- **REST API** built with FastAPI
- Accepts image uploads and product details
- Integrates with OpenAI's GPT-5 image model
- Returns a ready-to-use product card image

## Endpoints

### `GET /health`

Health check endpoint.  
Returns service status and whether the `OPENAI_API_KEY` is set.

### `POST /process`

Generate a product card.

**Form Data:**

- `image` (file, required): Product image
- `title` (string, optional): Product title (default: "Ваза керамическая")
- `bullets` (string, optional): Product details, newline-separated or JSON array (default: example details)
- `background_color` (string, optional): Background color (default: "#FFFFFF")
- `background_prompt` (string, optional): Custom background prompt (default: None)
- `size` (string, optional): Output size (default: "1024x1024")
- `quality` (string, optional): Output quality (default: "high")

**Response:**  
Returns a PNG image of the generated product card.

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Set your OpenAI API key in .env (OPENAI_API_KEY=...)
uvicorn main:app --reload --port 8000
```

## Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your_openai_key_here
```

## Example Request

```bash
curl -X POST "http://localhost:8000/process" \
  -F "image=@your_image.png" \
  -F "title=Sample Product" \
  -F "bullets=Feature 1\nFeature 2"
```

## File Structure

- [`main.py`](main.py): FastAPI app and endpoints
- [`openai_images.py`](openai_images.py): OpenAI image generation logic
- [`requirements.txt`](requirements.txt): Python dependencies
