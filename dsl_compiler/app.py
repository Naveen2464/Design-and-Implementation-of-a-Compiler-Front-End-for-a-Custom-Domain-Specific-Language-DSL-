from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code', '')
    
    # Write code to sample.dsl
    with open('sample.dsl', 'w') as f:
        f.write(code)
    
    try:
        # Run parser.py
        result = subprocess.run(['python', 'parser.py'], capture_output=True, text=True)
        output = result.stdout
        
        # Simple parsing of the output to split it into sections
        sections = {
            'lexical': '',
            'syntax': '',
            'semantic': '',
            'symbol': '',
            'tac': '',
            'output': ''
        }
        
        current_section = None
        lines = output.split('\n')
        
        for i, line in enumerate(lines):
            if "LEXICAL ANALYSIS" in line:
                current_section = 'lexical'
            elif "SYNTAX ANALYSIS" in line:
                current_section = 'syntax'
            elif "SEMANTIC ANALYSIS" in line:
                current_section = 'semantic'
            elif "SYMBOL TABLE" in line:
                current_section = 'symbol'
            elif "THREE ADDRESS CODE" in line:
                current_section = 'tac'
            elif "PROGRAM OUTPUT" in line:
                current_section = 'output'
            elif current_section and "---------------------------------" not in line:
                if line.strip() != "":
                    sections[current_section] += line + '\n'
        
        return jsonify({
            'success': True,
            'raw_output': output,
            'sections': sections
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
