import json
import os


dataset = 'medqa'

# Define the path to the JSONL file
jsonl_file_path = '/Users/ybkim95/dxagents.github.io/dataset/{}/test.jsonl'.format(dataset)
# Define the output Markdown file path
output_md_path = '/Users/ybkim95/dxagents.github.io/_posts/text/1970-01-01-medqa.md'

# Prepare the header for the Markdown file
md_header = """---
layout: blog
book: true
background-image: http://ot1cc1u9t.bkt.clouddn.com/17-7-16/91630214.jpg
category: text
title: MedQA
tags:
- text
redirect_from:
  - /1970/01/bookindex/
---

"""

# Function to convert JSONL to Markdown
def jsonl_to_md(jsonl_path, md_path):
    with open(jsonl_path, 'r') as jsonl_file, open(md_path, 'w') as md_file:
        # Write the header to the markdown file
        md_file.write(md_header)
        
        # Process each line in the JSONL file
        for line in jsonl_file:
            # Parse JSON data
            data = json.loads(line)
            
            # Extract question, answer, and img_path
            question = data.get('question', 'No question provided')
            answer = data.get('answer', 'No answer provided')
            answer_idx = data.get('answer_idx', 'No answer provided')
            opa = data.get('options', 'No answer provided')['A']
            opb = data.get('options', 'No answer provided')['B']
            opc = data.get('options', 'No answer provided')['C']
            opd = data.get('options', 'No answer provided')['D']
            ope = data.get('options', 'No answer provided')['E']
            # img_path = data.get('img_path', '')
            
            # Write to the Markdown file
            md_file.write(f"## Question\n{question}\n\n(A) {opa} (B) {opb} (C) {opc} (D) {opd} (E) {ope}\n\n")
            md_file.write(f"## Answer\n({answer_idx}) {answer}\n\n")
            # if img_path:
                # md_file.write(f"![Image]({img_path})\n\n")

# Call the function with paths
jsonl_to_md(jsonl_file_path, output_md_path)
