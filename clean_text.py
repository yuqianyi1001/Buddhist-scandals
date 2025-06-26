#!/usr/bin/env python3
import re

def clean_chinese_text(input_file, output_file):
    """Remove unnecessary spaces from Chinese text"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Multiple passes to remove spaces between Chinese characters
    # Pass 1: Remove single spaces between Chinese characters
    cleaned_content = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', content)
    
    # Pass 2: Repeat to catch remaining spaces (iterative cleaning)
    for _ in range(3):  # Multiple passes for thorough cleaning
        cleaned_content = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', cleaned_content)
    
    # Remove spaces between Chinese characters and punctuation
    cleaned_content = re.sub(r'([\u4e00-\u9fff])\s+([，。；：！？、])', r'\1\2', cleaned_content)
    cleaned_content = re.sub(r'([，。；：！？、])\s+([\u4e00-\u9fff])', r'\1\2', cleaned_content)
    
    # Keep single space around English words/numbers but remove excessive spaces
    cleaned_content = re.sub(r' {2,}', ' ', cleaned_content)
    
    # Remove trailing spaces at end of lines
    cleaned_content = re.sub(r' +$', '', cleaned_content, flags=re.MULTILINE)
    
    # Remove leading spaces at beginning of lines (except for intentional indentation)
    cleaned_content = re.sub(r'^\s+', '', cleaned_content, flags=re.MULTILINE)
    
    # Remove excessive blank lines (more than 2 consecutive)
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Cleaned text saved to: {output_file}")
    
    # Show file size comparison
    import os
    original_size = os.path.getsize(input_file)
    cleaned_size = os.path.getsize(output_file)
    print(f"Original size: {original_size:,} bytes")
    print(f"Cleaned size: {cleaned_size:,} bytes")
    print(f"Reduced by: {original_size - cleaned_size:,} bytes ({((original_size - cleaned_size) / original_size * 100):.1f}%)")

if __name__ == "__main__":
    input_file = "梦醒极乐寺--举报学诚尼自白_extracted_text.txt"
    output_file = "梦醒极乐寺--举报学诚尼自白_cleaned.txt"
    clean_chinese_text(input_file, output_file)