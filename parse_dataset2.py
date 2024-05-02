import json
import re


def parse_options(options_string):
    # Regex to find patterns like (A) Option Description
    pattern = r"\(([A-Z])\)\s+([^)(]+)"
    matches = re.findall(pattern, options_string)
    
    # Convert list of tuples into a dictionary
    options_dict = {match[0]: match[1].strip() for match in matches}
    return options_dict


for dataset in ['medqa', 'medmcqa', 'pubmedqa', 'ddxplus', 'pmc-vqa', 'path-vqa']:

    if dataset == 'medqa':
        color = 'yellow'
        title = "MedQA"
        category = 'text-only'
    elif dataset == 'medmcqa':
        color = 'yellow'
        title = 'MedMCQA'
        category = 'text-only'
    elif dataset == 'pubmedqa':
        color = 'yellow'
        title = 'PubMedQA'
        category = 'text-only'
    elif dataset == 'ddxplus':
        color = 'yellow'
        title = 'DDXPlus'
        category = 'text-only'
    elif dataset == 'pmc-vqa':
        color = 'red'
        title = 'PMC-VQA'
        category = 'image+text'
    elif dataset == 'path-vqa':
        color = 'red'
        title = 'Path-VQA'
        category = 'image+text'
    elif dataset == 'medvidqa':
        color = 'blue'
        title = 'MedVidQA'
        category = 'video+text'


    def read_jsonl_file(file_path):
        with open(file_path, 'r') as file:
            return file.readlines() 

    def generate_markdown_form(jsonl_lines, form_endpoint):
        markdown_header = f"""---
layout: blog
book: true
background: {color}
background-image: http://ot1cc1u9t.bkt.clouddn.com/17-7-15/48174506.jpg
title:  "{title}"
category: {category}
---
"""

        
        markdown_content = [markdown_header]
        markdown_content.append("## Medical Quiz\n")
        markdown_content.append("Please enter your unique ID and answer all questions below:\n")
        markdown_content.append(f'<form id="quizForm" action="{form_endpoint}" method="POST">\n')
        markdown_content.append(f'  Unique ID:<br>')
        markdown_content.append(f'  <input type="text" name="unique_id" value="{dataset}_" style="background-color: #D3D3D3;" required><br><br>')
        markdown_content.append("<p><b>Instructions:</b> Given the medical questions below, you need to first provide your answer among the options. Next, for the difficulty/complexity of each question, please select among the following options:</p>")
        markdown_content.append("<ol><li><b>Low:</b> a PCP or general physician can answer this question without consulting a specialist.</li>")
        markdown_content.append("<li><b>Moderate:</b> a PCP or general physician can answer this question in consultation with a specialist, and a single specialist can answer this question.</li>")
        markdown_content.append("<li><b>High:</b> A team of multi-departmental specialists can answer this question, which requires specialists consulting to another department (Requires team effort to treat the case).</li></ol>")
        
        question_number = 1
        for line in jsonl_lines:
            data = json.loads(line)
            if dataset == 'pmc-vqa':
                img_path = data.get('img_path', '')
            if dataset == 'path-vqa':
                img_path = data.get('img', '')

            if dataset == 'medqa':
                question = data["question"]
                options = data["options"]
            elif dataset == 'medmcqa':
                question = data["question"]
                options = {'A': data['opa'], 'B': data['opb'], 'C': data['opc'], 'D': data['opd']}
            elif dataset == 'pubmedqa':
                question = data["question"]
                options = {'A': 'yes', 'B': 'no'}
                question += ' ' + data['context']
            elif dataset == 'ddxplus':
                initial_evidence = data['initial_evidence']
                clinical_evidence = data['evidences']
                age = data['age']
                sex = data['sex']
                question = f"""Patient Information:\n-Age: {age}\n-Sex: {sex}\n-Initial Evidence: {initial_evidence}\n\nClinical Evidence:\n{clinical_evidence}\n\nBased on the above information, please choose the most likely diagnosis."""

                options = parse_options(data['options'])

            elif dataset == 'pmc-vqa':
                question = data["question"]
                options = {'A': data['opa'], 'B': data['opb'], 'C': data['opc'], 'D': data['opd']}
            elif dataset == 'path-vqa':
                question = data["question"]
                options = {'A': 'yes', 'B': 'no'}

            markdown_content.append(f"<p><b>Question {question_number}</b>: {question}</p>\n")
            
            if dataset == 'pmc-vqa':
                markdown_content.append(f'<img src="/dataset/{dataset}/images/{img_path}" alt="Image">\n\n')
            if dataset == 'path-vqa':
                markdown_content.append(f'<img src="/dataset/{dataset}/images/{img_path}.jpg" alt="Image">\n\n')


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
    jsonl_file_path = '/Users/ybkim95/dxagents.github.io/dataset/{}/test.jsonl'.format(dataset)
    form_endpoint = "https://getform.io/f/1569b998-160a-45dd-a9e1-a2babfbdecb5"
    if dataset == 'medqa':
        output_path = "/Users/ybkim95/dxagents.github.io/_posts/text/2024-05-01-medqa.md"
    if dataset == 'medmcqa':
        output_path = "/Users/ybkim95/dxagents.github.io/_posts/text/2024-04-30-medmcqa.md"
    if dataset == 'pubmedqa':
        output_path = "/Users/ybkim95/dxagents.github.io/_posts/text/2024-04-29-pubmedqa.md"
    if dataset == 'ddxplus':
        output_path = "/Users/ybkim95/dxagents.github.io/_posts/text/2024-04-28-ddxplus.md"
    if dataset == 'pmc-vqa':
        output_path = "/Users/ybkim95/dxagents.github.io/_posts/image/2024-04-27-pmc-vqa.md"
    if dataset == 'path-vqa':
        output_path = "/Users/ybkim95/dxagents.github.io/_posts/image/2024-04-26-path-vqa.md"

    # Read the .jsonl file
    jsonl_lines = read_jsonl_file(jsonl_file_path)

    # Generate the markdown form
    markdown_form = generate_markdown_form(jsonl_lines, form_endpoint)

    # Write the content to a file
    write_to_file(output_path, markdown_form)
