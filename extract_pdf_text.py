#!/usr/bin/env python3
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import sys
import os

def extract_text_from_pdf(pdf_path, output_path):
    """Extract text from PDF using OCR and save to text file"""
    try:
        # Convert PDF to images
        print(f"Converting PDF to images...")
        images = convert_from_path(pdf_path, dpi=300)
        
        all_text = []
        
        # Process each page
        for i, image in enumerate(images):
            print(f"Processing page {i+1}/{len(images)}...")
            
            # Try different language configurations for Chinese text
            try:
                # Try with local chi_sim file
                text = pytesseract.image_to_string(image, lang='chi_sim', config='--tessdata-dir .')
            except:
                try:
                    # Fallback to English
                    text = pytesseract.image_to_string(image, lang='eng')
                except:
                    # Last resort - try without language specification
                    text = pytesseract.image_to_string(image)
            
            if text.strip():
                all_text.append(f"=== Page {i+1} ===\n{text}\n")
        
        # Save to text file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        
        print(f"Text extracted and saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    pdf_file = "梦醒极乐寺--举报学诚尼自白.pdf"
    output_file = "梦醒极乐寺--举报学诚尼自白_extracted_text.txt"
    
    if os.path.exists(pdf_file):
        extract_text_from_pdf(pdf_file, output_file)
    else:
        print(f"PDF file not found: {pdf_file}")