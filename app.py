from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
history = []

def manual_calculate(expr):
    expr = expr.replace(' ', '')  # remove spaces
    if expr.replace('.', '', 1).isdigit():
        return f"{expr} = {expr}"
    operators = ['+', '-', '*', '/']

    for op in operators:
        if op in expr:
            parts = expr.split(op)
            if len(parts) != 2:
                return "Error"
            a_str, b_str = parts
            try:
                a = float(a_str)
                b = float(b_str)
            except:
                return "Invalid numbers"

            if op == '+':
                result = a + b
                return f"{a} + {b} = {result}"
            elif op == '-':
                result = a - b
                return f"{a} - {b} = {result}"
            elif op == '*':
                result = a * b
                return f"{a} * {b} = {result}"
            elif op == '/':
                if b == 0:
                    return "Division by zero"
                result = a / b
                return f"{a} / {b} = {result}"
    
    return "Unsupported expression"

@app.route("/")
def index():
    return render_template("index.html", history=history)

@app.route("/calculate", methods=["POST"])
def calculate():
    expr = request.form.get("expression", "")
    result = manual_calculate(expr)
    if "Error" not in result and "Invalid" not in result:
        history.append(result)
    return jsonify({"result": result.split('=')[-1].strip() if '=' in result else result})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
