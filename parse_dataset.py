import json
import os


dataset = 'medqa'

jsonl_file_path = '/Users/ybkim95/dxagents.github.io/dataset/{}/test.jsonl'.format(dataset)

if dataset == 'medqa':
  output_md_path = '/Users/ybkim95/dxagents.github.io/_posts/text/2024-05-01-medqa.md'

elif dataset == 'pmc-vqa':
   output_md_path = '/Users/ybkim95/dxagents.github.io/_posts/image/2024-04-27-pmc-vqa.md'

if dataset in ['medqa', 'pubmedq', 'ddxplus', 'medmcqa']:
  # Prepare the header for the Markdown file
  md_header = """---
layout: blog
book: true
background: yellow
background-image: http://ot1cc1u9t.bkt.clouddn.com/17-7-15/48174506.jpg
category: text-only
title: MedQA
tags:
- text
---

"""

  # Function to convert JSONL to Markdown
  def jsonl_to_md(jsonl_path, md_path):
      with open(jsonl_path, 'r') as jsonl_file, open(md_path, 'w') as md_file:
          # Write the header to the markdown file
          md_file.write(md_header)
          
          # Process each line in the JSONL file
          count = 1
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
              md_file.write(f"## Question {count}\n{question}\n\n(A) {opa} (B) {opb} (C) {opc} (D) {opd} (E) {ope}\n\n")
              md_file.write(f"## Answer\n({answer_idx}) {answer}\n\n")
              
              # if img_path:
              #     md_file.write(f"![Image]({img_path})\n\n")

              count += 1

  jsonl_to_md(jsonl_file_path, output_md_path)

elif dataset in ['pmc-vqa', 'path-vqa']:
  md_header = """---
layout: blog
book: true
title: "PMC-VQA"
background: red
background-image: http://ot1cc1u9t.bkt.clouddn.com/17-7-15/48174506.jpg
category: image+text
---

"""

  def jsonl_to_md(jsonl_path, md_path):
    with open(jsonl_path, 'r') as jsonl_file, open(md_path, 'w') as md_file:
        md_file.write(md_header)

        count = 1
        for line in jsonl_file:
            data = json.loads(line)

            question = data.get('question', 'No question provided')
            answer = data.get('answer', 'No answer provided')
            # answer_idx = data.get('answer_idx', 'No answer provided')
            opa = data.get('opa', {}).split(":")[1].strip()
            opb = data.get('opb', {}).split(":")[1].strip()
            opc = data.get('opc', {}).split(":")[1].strip()
            opd = data.get('opd', {}).split(":")[1].strip()
            img_path = data.get('img_path', '')

            if answer == opa:
               answer_idx = 'A'
            if answer == opb:
               answer_idx = 'B'
            if answer == opc:
               answer_idx = 'C'
            if answer == opd:
               answer_idx = 'D'

            md_file.write(f"## Question {count}\n{question}\n(A) {opa} (B) {opb} (C) {opc} (D) {opd}\n\n")
            # for key, value in options.items():
                # md_file.write(f"({key}) {value} ")
            
            if img_path:
              md_file.write(f"![Image](/dataset/pmc-vqa/images/{img_path})\n\n")
            
            
            md_file.write("\n\n## Answer\n({}) {}\n\n".format(answer_idx, answer))

            


            # if video_url:
            #     md_file.write(f'<video src="{video_url}" controls width="250">\nYour browser does not support the video tag.\n</video>\n\n')

            count += 1

  jsonl_to_md(jsonl_file_path, output_md_path)
    




