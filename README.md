# automated-pc

### image flow
User uploads image
↓
FastAPI service removes background (RAM or temp file)
↓
AI generates beautiful background + merges with object (RAM or temp file)
↓
Final product image saved to S3 (or CDN / database reference)

