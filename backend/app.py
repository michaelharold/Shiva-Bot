from flask import Flask, jsonify

app = Flask(__name__)

employee_db = {
    "101": {
        "casual": 5,
        "sick": 3,
        "earned": 10,
        "salary": 50000,
        "bonus": 5000
    },
    "102": {
        "casual": 2,
        "sick": 4,
        "earned": 8,
        "salary": 60000,
        "bonus": 6000
    }
}

benefits_data = {
    "health_insurance": "Comprehensive medical insurance",
    "retirement_plan": "Company-sponsored retirement savings plan",
    "paid_leave": "Annual paid leave policy"
}

@app.route("/api/leave/<emp_id>/<leave_type>")
def get_leave(emp_id, leave_type):
    leave_balance = employee_db.get(emp_id, {}).get(leave_type.lower(), 0)
    return jsonify({"balance": leave_balance})

@app.route("/api/payroll/<emp_id>")
def get_payroll(emp_id):
    emp = employee_db.get(emp_id, {})
    return jsonify({
        "salary": emp.get("salary", 0),
        "bonus": emp.get("bonus", 0)
    })

@app.route("/api/benefits")
def get_benefits():
    return jsonify(benefits_data)

if __name__ == "__main__":
    app.run(port=5000)