import torch
from torchvision.models import resnet50, ResNet50_Weights
from torchvision import transforms
from PIL import Image
import io
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from random import sample

app = FastAPI()

origins = [
    "http://localhost:3000"
    "https://detect-brain-cancer.nbaron.com",
    "https://detect-.nbaron.com",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

melanoma_model = None
melanoma_transform = None

# todo: process .webp images
def load_melanoma_model():
    global melanoma_model, melanoma_transform
    
    # Load model architecture
    weights = ResNet50_Weights.DEFAULT
    melanoma_model = resnet50(weights=weights)
    
    # Freeze parameters
    for param in melanoma_model.parameters():
        param.requires_grad = False
        
    # Replace final layer
    melanoma_model.fc = torch.nn.Linear(2048, 4)
    
    melanoma_model.load_state_dict(torch.load('./models/100k-images.pth', map_location=torch.device('cpu'), weights_only=True))
    melanoma_model.to(device)
    melanoma_model.eval()
    
    melanoma_transform = weights.transforms()


brain_tumor_model = None
brain_tumor_transform = None

def load_braintumor_model():
    global brain_tumor_model, brain_tumor_transform

    weights = ResNet50_Weights.DEFAULT
    brain_tumor_model = resnet50(weights=weights).to(device)

    for param in brain_tumor_model.parameters():
        param.requires_grad = False

    # Unfreeze the last residual block
    for param in brain_tumor_model.layer4.parameters():
        param.requires_grad = True

    # Replace classifier with a more robust head
    brain_tumor_model.fc = torch.nn.Sequential(
        torch.nn.Linear(2048, 512),
        torch.nn.ReLU(),
        torch.nn.Dropout(0.4),
        torch.nn.Linear(512, 4)
    ).to(device)
    
    brain_tumor_transform = transforms.Compose([
        transforms.Resize(256),  # Resize to slightly larger dimension
        transforms.CenterCrop(224),  # Crop center to match training size
        transforms.ToTensor(),
        weights.transforms()
    ])


load_melanoma_model()
load_braintumor_model()

@app.get('/health')
def health():
    return "OK"

class PredictionResponse(BaseModel):
    success: bool
    classification: int
    confidence: float
    error_message: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    success: bool = False
 
@app.post('/melanoma/predict')
async def predict(image: UploadFile = File(...)):
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File uploaded is not an image"
        )
    
    try:
        image_bytes = await image.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        image_tensor = melanoma_transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = melanoma_model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        pred_label_idx = torch.argmax(probabilities, dim=1).item()    
        
        return PredictionResponse(
            classification=pred_label_idx,
            confidence=float(probabilities[0][pred_label_idx].item()),
            success=True
        )
        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

class ImageURL(BaseModel):
    url: str       

@app.post('/melanoma/predict-url')
async def predict_url(image_data: ImageURL):
    try:
        # Download image from URL
        response = requests.get(image_data.url, timeout=10)
        response.raise_for_status()

        # Open and convert image
        image = Image.open(io.BytesIO(response.content)).convert('RGB')
        
        # Preprocess
        image_tensor = melanoma_transform(image).unsqueeze(0).to(device)
        
        # Get prediction
        with torch.no_grad():
            outputs = melanoma_model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        pred_label_idx = torch.argmax(probabilities, dim=1).item()
        
        return PredictionResponse(
            classification=pred_label_idx,
            confidence=probabilities[0][pred_label_idx].item(),
            success=True
        )

    except requests.RequestException:
        raise HTTPException(
            status_code=400,
            detail="Could not download image from URL"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )



class Image(BaseModel):
    src: str
    label: str

class ImagesResponse(BaseModel):
    images: list[Image]


@app.get('/brain-tumor/images')
async def getImages():
    random_images = sample(images, 12)

    return ImagesResponse(images=random_images)

@app.post('/brain-tumor/predict')
async def predict(image: UploadFile = File(...)):
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File uploaded is not an image"
        )
    
    try:
        image_bytes = await image.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        image_tensor = brain_tumor_transform(image).to(device)

        with torch.no_grad():
            outputs = brain_tumor_model(image_tensor.unsqueeze(0))
            probabilities = torch.nn.functional.softmax(outputs, dim=1)

        pred_label_idx = torch.argmax(probabilities, dim=1).item()    
            
        return PredictionResponse(
            classification=pred_label_idx,
            confidence=float(probabilities[0][pred_label_idx].item()),
            success=True
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
