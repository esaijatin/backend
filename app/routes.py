# app/routes.py
from fastapi import APIRouter, UploadFile, HTTPException
import pandas as pd
import qrcode
import os
from bson import ObjectId
from .database import certificates
from .models import Certificate

router = APIRouter()

# Ensure the QR codes directory exists
os.makedirs('qr_codes', exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile):
    try:
        df = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading the Excel file: {str(e)}")
    
    # List to store created certificate details
    created_certificates = []
    
    for _, row in df.iterrows():
        cert = Certificate(name=row["Name"], course=row["Course"], date=row["Date"])
        
        # Generate QR code
        qr_data = f"Certificate for {row['Name']} in {row['Course']} on {row['Date']}"
        qr = qrcode.make(qr_data)
        
        # Define path to save QR code
        qr_code_path = f"qr_codes/{cert.name}_{cert.date}.png"  # Ensure the naming is unique
        qr.save(qr_code_path)  # Save QR code image

        # Save certificate with the path to the QR code
        cert.qr_code = qr_code_path
        certificates.insert_one(cert.dict())
        
        created_certificates.append(cert.dict())

    return {"message": "Certificates generated!", "certificates": created_certificates}

@router.get("/verify/{id}")
async def verify_certificate(id: str):
    try:
        # Convert string ID to ObjectId
        cert = certificates.find_one({"_id": ObjectId(id)})
        
        if cert:
            return {"valid": True, "certificate": cert}
        else:
            return {"valid": False, "message": "Certificate not found."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid certificate ID: {str(e)}")
