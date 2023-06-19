import csv
import eng_to_ipa as ipa

def read_template(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def substitute_body(template, body_text):
    return template.replace('$body', body_text)

def save_result(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def generate_html_row(row_data, row_counter):
    html = "<tr>"
    for word in row_data:
        if (row_counter - 1) % 3 == 0:
            word = word + " [" + ipa.convert(word) + "]"
        html += f"<td>{word}</td>"
    html += "</tr>"
    return html

def process_csv_file(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        html_output = ""
        row_counter = 0

        for row in csvreader:
            if row:
                row_counter += 1
                html_output += generate_html_row(row, row_counter)
                if row_counter % 3 == 0:
                    html_output += '<tr class="blank-row"></tr>'

    return html_output

filename = "words.csv"
html_table_rows = process_csv_file(filename)

template_content = read_template("template.html")
substituted_content = substitute_body(template_content, html_table_rows)
save_result("words.html", substituted_content)



