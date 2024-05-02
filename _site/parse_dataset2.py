import json

def read_jsonl_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()  # Returns lines directly for better processing in the next function.

def generate_markdown_form(jsonl_lines, form_endpoint):
    markdown_header = """---
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
    markdown_content = [markdown_header]
    markdown_content.append("## Medical Quiz\n")
    markdown_content.append("Please enter your unique ID and answer all questions below:\n")
    markdown_content.append(f'<form id="quizForm" action="{form_endpoint}" method="POST">\n')
    markdown_content.append('  Unique ID:<br>')
    markdown_content.append('  <input type="text" name="unique_id" style="background-color: #D3D3D3;" required><br><br>')
    markdown_content.append("<p><b>Instructions:</b> Given the medical questions below, you need to first provide your answer among the options. Next, for the difficulty/complexity of each question, please select among the following options:</p>")
    markdown_content.append("<ol><li><b>Low:</b> a PCP or general physician can answer this question without consulting a specialist.</li>")
    markdown_content.append("<li><b>Moderate:</b> a PCP or general physician can answer this question in consultation with a specialist, and a single specialist can answer this question.</li>")
    markdown_content.append("<li><b>High:</b> A team of multi-departmental specialists can answer this question, which requires specialists consulting to another department (Requires team effort to treat the case).</li></ol>")
    
    question_number = 1
    for line in jsonl_lines:
        data = json.loads(line)
        question = data["question"]
        options = data["options"]
        
        markdown_content.append(f"<p><b>Question {question_number}</b>: {question}</p>\n")
        for option_key, option_value in options.items():
            markdown_content.append(f'  <input type="radio" id="q{question_number}{option_key}" name="Q{question_number}_answer" value="{option_key}" required>')
            markdown_content.append(f'  <label for="q{question_number}{option_key}">({option_key}) {option_value}</label><br>\n')
        
        # Complexity options for each question
        markdown_content.append('<p>Please rate the complexity of this question:</p>')
        markdown_content.append(f'  <input type="radio" id="low{question_number}" name="Q{question_number}_complexity" value="Low" required>')
        markdown_content.append(f'  <label for="low{question_number}">Low</label><br>')
        markdown_content.append(f'  <input type="radio" id="moderate{question_number}" name="Q{question_number}_complexity" value="Moderate" required>')
        markdown_content.append(f'  <label for="moderate{question_number}">Moderate</label><br>')
        markdown_content.append(f'  <input type="radio" id="high{question_number}" name="Q{question_number}_complexity" value="High" required>')
        markdown_content.append(f'  <label for="high{question_number}">High</label><br><br>')
        
        question_number += 1

    markdown_content.append('<button type="submit" id="submitButton" abled>Submit</button>\n')
    markdown_content.append('</form>\n')
    return '\n'.join(markdown_content)

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Variables
jsonl_file_path = '/Users/ybkim95/dxagents.github.io/dataset/medqa/test.jsonl'
form_endpoint = "https://getform.io/f/1569b998-160a-45dd-a9e1-a2babfbdecb5"
output_path = "/Users/ybkim95/dxagents.github.io/_posts/text/2024-05-01-medqa.md"

# Read the .jsonl file
jsonl_lines = read_jsonl_file(jsonl_file_path)

# Generate the markdown form
markdown_form = generate_markdown_form(jsonl_lines, form_endpoint)

# Write the content to a file
write_to_file(output_path, markdown_form)
