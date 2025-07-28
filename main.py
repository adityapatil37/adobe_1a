import pymupdf
import pandas as pd
import json
import os
from pathlib import Path

def get_title(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        if not doc.page_count:
            doc.close()
            return "", 0

        page = doc[0]
        text_blocks = page.get_text("dict")["blocks"]
        
        max_font_size = 0
        title_text = ""

        # Find maximum font size
        for block in text_blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span['text'].strip()
                        font_size = round(span['size'], 1)
                        if text and font_size > max_font_size:
                            max_font_size = font_size

        # Collect title text
        for block in text_blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span['text'].strip()
                        font_size = span['size']
                        if text and font_size == max_font_size:
                            title_text = text
                            doc.close()
                            return title_text, max_font_size

        doc.close()
        return "", 0
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return "", 0

def process_pdf(pdf_path):
    try:
        if not os.path.exists(pdf_path):
            print(f"Error: File not found: {pdf_path}")
            return None

        title, title_font_size = get_title(pdf_path)
        if not title:
            print(f"Warning: Could not determine title for {pdf_path}")

        doc = pymupdf.open(pdf_path)
        
        if not doc.page_count:
            doc.close()
            return {"title": title, "outline": []}

        text_data = []
        for page_num in range(1, len(doc)):
            page = doc[page_num]
            text_blocks = page.get_text("dict")["blocks"]
            current_text = ""
            current_font_size = None

            for block in text_blocks:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span['text'].strip()
                        if not text:
                            continue
                        font_size = round(span['size'], 1)
                        if font_size >= title_font_size:
                            continue
                        if current_text and current_font_size == font_size:
                            current_text += " " + text
                        else:
                            if current_text:
                                text_data.append({
                                    "text": current_text,
                                    "f_size": current_font_size,
                                    "page_no": page_num
                                })
                            current_text = text
                            current_font_size = font_size
            if current_text:
                text_data.append({
                    "text": current_text,
                    "f_size": current_font_size,
                    "page_no": page_num
                })

        doc.close()

        if not text_data:
            return {"title": title, "outline": []}

        # Create DataFrame and filter noise
        df = pd.DataFrame(text_data)
        regex_pattern = r'^[0-9\s\.,><%+-]*$'
        df = df[~df['text'].str.match(regex_pattern, na=False)]

        if df.empty:
            return {"title": title, "outline": []}

        # Determine heading hierarchy
        unique_font_sizes = sorted(df['f_size'].unique(), reverse=True)
        heading_sizes = [size for size in unique_font_sizes if size < title_font_size][:2]
        
        if not heading_sizes:
            heading_sizes = unique_font_sizes[:min(2, len(unique_font_sizes))]

        level_mapping = {size: f"H{i+1}" for i, size in enumerate(heading_sizes)}
        df['level'] = df['f_size'].map(level_mapping).fillna("")

        # Create outline
        outline = [
            {"level": row['level'], "text": row['text'], "page": row['page_no']}
            for _, row in df[df['level'] != ''].iterrows()
        ]

        # Remove title if it appears in outline
        if title:
            outline = [item for item in outline if item['text'] != title]

        return {"title": title, "outline": outline}
    
    except Exception as e:
        print(f"Processing error: {e}")
        return {"title": "", "outline": []}

def main():
    # Define input/output paths
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Starting PDF processing...")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Process all PDFs in input directory
    processed = 0
    for pdf_file in input_dir.glob("*.pdf"):
        print(f"\nProcessing: {pdf_file.name}")
        result = process_pdf(str(pdf_file))
        
        if result:
            output_path = output_dir / f"{pdf_file.stem}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"  → Saved outline to: {output_path.name}")
            processed += 1
    
    print(f"\nProcessing complete! Processed {processed} PDF files.")

if __name__ == "__main__":
    main()