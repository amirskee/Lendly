from flask import Flask, request, jsonify, render_template
import time
import random

app = Flask(__name__)

# Dynamic Business Data mapping to handle dropdowns and uploads properly
def generate_mock_business_data(name=None, country="India", lat=None, lng=None):
    db = {
        "India": {"name": "Maneesh Textiles", "city": "New Delhi", "curr": "₹", "lat": 28.6139, "lng": 77.2090},
        "USA": {"name": "TechNova Solutions", "city": "Austin, TX", "curr": "$", "lat": 30.2672, "lng": -97.7431},
        "Uzbekistan": {"name": "Alisher Electronics", "city": "Tashkent", "curr": "UZS", "lat": 41.2995, "lng": 69.2401},
        "Kenya": {"name": "Nairobi Fresh Exports", "city": "Nairobi", "curr": "KSh", "lat": -1.2921, "lng": 36.8219},
        "Brazil": {"name": "Rio Coffee Distributors", "city": "Rio de Janeiro", "curr": "R$", "lat": -22.9068, "lng": -43.1729},
        "Egypt": {"name": "Cairo Traders", "city": "Cairo", "curr": "E£", "lat": 30.0444, "lng": 31.2357},
        "United Kingdom": {"name": "Thames Logistics", "city": "London", "curr": "£", "lat": 51.5074, "lng": -0.1278},
    }
    
    info = db.get(country, {
        "name": f"{country} Global Trade",
        "city": f"{country} Capital",
        "curr": "$", # Fallback to standard symbol instead of ¤
        "lat": random.uniform(-40, 60),
        "lng": random.uniform(-100, 100)
    })
    
    base_score = random.randint(45, 92) if not name else 78
    tier = "TIER 1 - AUTO-APPROVE" if base_score >= 70 else ("TIER 2 - REVIEWED" if base_score >= 55 else "NOT APPROVED - CRITICAL RISK")

    return {
        "business_name": name if name else info["name"],
        "city": info["city"],
        "country": country,
        "sector": "Retail & Commerce" if not name else "Textile Manufacturing",
        "icon": "🛍️",
        "coords": [lat if lat else info["lat"], lng if lng else info["lng"]],
        "score": base_score,
        "ai_rating": base_score * 10 + random.randint(0, 9),
        "geo_grade": "A+" if base_score > 75 else "B",
        "cash_flow_volatility": f"{random.uniform(5.0, 25.0):.1f}%",
        "eval_speed": f"{random.uniform(1.1, 4.5):.1f}s",
        "probability": f"{min(99, base_score + 12)}%",
        "tier": tier,
        "currency": info["curr"],
        "loan_config": { "min": 5000, "max": 50000, "step": 1000, "default_amt": random.randint(15, 35) * 1000, "default_emi": random.randint(1000, 3000) },
        "metrics": { "payment_velocity": random.randint(60, 98), "location_demand": random.randint(50, 95), "transaction_consistency": random.randint(60, 90), "business_risk": random.randint(5, 35) },
        "profile": {
            "business_age": f"{random.uniform(1.0, 10.0):.1f} years",
            "monthly_revenue": random.randint(15000, 80000),
            "monthly_txn_volume": random.randint(200, 1500),
            "avg_daily_sales": random.randint(500, 2500),
            "repayment_history": "100% on-time" if base_score > 60 else "2 late payments",
            "owner_verified": True,
            "emi_affordability_ratio": round(random.uniform(5.0, 25.0), 1),
            "documents": { "bank_statements": True, "registration_certificate": True, "utility_bill": random.choice([True, False]), "lease_agreement": True }
        },
        "layers": { "traffic": [], "growth": [], "competitors": [], "flows": [] },
        "evaluated_at": "Right now",
        "explanation": f"Decision generated using {country} local transaction, location, and sector-risk data."
    }

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/api/market', methods=['GET'])
def market():
    country = request.args.get('country', 'India')
    return jsonify(generate_mock_business_data(country=country))

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', 'Searched Business')
    return jsonify(generate_mock_business_data(name=query, country="India"))

@app.route('/api/alerts', methods=['GET'])
def alerts():
    country = request.args.get('country', 'India')
    return jsonify({
        "alerts": [
            { "level": 'positive', "title": 'Strong Payment Velocity', "detail": 'Consistent daily cash flow minimizes repayment risk.' },
            { "level": 'caution', "title": 'Sector Micro-Risk', "detail": 'Local sector shows slight seasonal volatility.' },
            { "level": 'data', "title": 'Utility Bill Missing', "detail": 'Upload utility bill to strengthen location verification.' }
        ]
    })

@app.route('/api/scenario', methods=['POST'])
def scenario():
    data = request.get_json() or {}
    scenario_type = data.get('scenario', '')
    stressed_score = 62 if scenario_type == 'traffic_drop' else 68
    tier = 'TIER 2 - REVIEWED' if scenario_type == 'traffic_drop' else 'TIER 1 - APPROVE'
    
    return jsonify({
        "base_score": 74,
        "stressed_score": stressed_score,
        "stressed_tier": tier,
        "stressed_probability": '75%',
        "adjusted_emi": 1763,
        "currency": 'UZS',
        "note": f"Simulated impact for: {scenario_type}",
        "verdict": 'Business maintains acceptable repayment capacity under stress.'
    })

def is_data_related_query(message):
    if not message:
        return False
    normalized = message.lower()
    data_keywords = [
        'score', 'risk', 'loan', 'business', 'revenue', 'cash', 'flow', 'location', 'traffic', 'profit',
        'performance', 'data', 'document', 'pdf', 'upload', 'analysis', 'underwriting', 'terms', 'emi',
        'credit', 'payment', 'gst', 'tax', 'history', 'improve', 'improvement', 'plan', 'project', 'customer', 'market'
    ]
    return any(keyword in normalized for keyword in data_keywords)


def generate_general_chat_response(message):
    normalized = message.lower().strip()
    greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    if any(greeting in normalized for greeting in greetings):
        return "Hello! I'm your Lendly underwriting assistant. Ask me anything about your project or the business data, and I will answer based on your question."
    return (
        f"You asked: \"{message}\". I can help with your project topic directly, and if you'd like me to use the on-screen business data, ask a data-specific question about loan score, risk, cash flow, business history, or improvement plans."
    )


def generate_business_chat_response(message, business_data):
    if not business_data:
        return "I can answer business data questions once a business profile is selected or a document is uploaded."

    business_name = business_data.get('business_name', 'This business')
    score = business_data.get('score', '--')
    tier = business_data.get('tier', 'No tier available')
    probability = business_data.get('probability', 'unknown repayment probability')
    city = business_data.get('city', '')
    cash_flow = business_data.get('cash_flow_volatility', 'unknown volatility')
    revenue = business_data.get('profile', {}).get('monthly_revenue')
    payment_velocity = business_data.get('metrics', {}).get('payment_velocity')
    location_demand = business_data.get('metrics', {}).get('location_demand')

    lower = message.lower()
    if 'hello' in lower or 'hi' in lower or 'hey' in lower:
        return (
            f"Hello! I am looking at {business_name} in {city}. For business-specific answers, ask about score, risk, loan terms, or improvement actions."
        )
    if 'score' in lower or 'why' in lower or 'tier' in lower:
        return (
            f"{business_name} currently has a score of {score}/100 and is rated {tier}."
            f" The model highlights payment velocity ({payment_velocity}%) and location demand ({location_demand}%) as the strongest drivers."
        )
    if 'risk' in lower or 'volatility' in lower or 'default' in lower:
        return (
            f"The main risk factor for {business_name} is cash-flow volatility at {cash_flow}."
            " Strengthen documentation and improve monthly revenue consistency to reduce underwriting risk."
        )
    if 'loan' in lower or 'emi' in lower or 'terms' in lower or 'amount' in lower:
        return (
            f"For {business_name}, the recommended loan setup is based on the current profile and history."
            f" The business is positioned for a structured loan with an affordable EMI, and the strongest repayment signal comes from stable payment velocity and location demand."
        )
    if 'improve' in lower or 'plan' in lower or 'growth' in lower or 'better' in lower:
        return (
            f"To improve {business_name}, focus on stronger document completeness, clearer cash-flow records, and higher local demand."
            " Additional actions include diversifying revenue streams, improving customer retention, and tightening supplier agreements."
        )

    return (
        f"Based on the on-screen business profile for {business_name}, the evaluation shows {tier} with {probability}."
        " Ask a specific question about score, risk, loan terms, or business improvement for a more detailed answer."
    )


@app.route('/api/narrative', methods=['POST'])
def narrative():
    data = request.get_json() or {}
    active_layers = data.get('active_layers', [])
    layer_text = ', '.join(active_layers) if active_layers else 'core business signals'
    time.sleep(1)
    return jsonify({
        "memo": "**Executive Summary:**\nThis analysis is focused on loan viability and business history for your underwriting project. It reviews current cash-flow stability, payment behaviour, and local demand using "
                  f"{layer_text}.\n\n**Improvement Plan:**\n1. Strengthen formal documentation and customer data capture.\n2. Improve monthly revenue consistency with targeted local offers.\n3. Reduce cash-flow volatility by diversifying product mix and payment channels.\n\n**Loan Recommendation:**\nThe business is best served with a conservative loan structure that preserves affordability while supporting measured growth."
    })


@app.route('/api/upload-document', methods=['POST'])
def upload_document():
    time.sleep(1.5)
    doc_name = "Uploaded_Document.pdf"
    if 'document' in request.files:
        doc_name = request.files['document'].filename

    country = request.form.get('country', 'Uzbekistan')
    business_name = request.form.get('business', 'the selected business')

    biz_data = generate_mock_business_data(business_name if business_name else 'Uploaded Business', country, 39.654610, 66.975086)
    biz_data['city'] = request.form.get('city', biz_data['city'])

    analysis_text = (
        f"The uploaded PDF {doc_name} was analyzed for {business_name}. "
        "It shows the business history and loan profile in a way that supports underwriting decisions. "
        "Key insights include stable payment patterns, local demand potential, and the need to complete missing documentation for faster approval."
    )

    improvement_plan = (
        "Improvement plan: 1) Strengthen document completeness and financial records. "
        "2) Formalize cash-flow tracking and payment history. 3) Increase local market visibility and customer retention. "
        "4) Use loan proceeds to optimize inventory and supplier terms for more stable revenue."
    )

    return jsonify({
        "document_name": doc_name,
        "document_type": "Business Report",
        "confidence_score": 0.98,
        "verification_summary": {
            "business_legitimacy": "Entity matches the provided business credentials",
            "address_verification": "Address aligns with the uploaded business documentation",
            "income_verification": "Revenue and cash flow are consistent with declared figures",
            "payment_reliability": "No major payment exceptions detected"
        },
        "fraud_check": { "fraud_risk": "LOW RISK (2%)" },
        "missing_documents": ["Lease Agreement"],
        "outstanding_questions": ["Please provide additional revenue backup for the last quarter."],
        "ai_insight": analysis_text,
        "improvement_plan": improvement_plan,
        "recommendation": "Use the uploaded document analysis to refine underwriting and present a business improvement roadmap.",
        "business_data": biz_data
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    business_data = data.get('business_data') or {}

    if not message:
        return jsonify({"reply": "Please type your question so I can help with your project or business data."})

    if is_data_related_query(message) and business_data:
        reply = generate_business_chat_response(message, business_data)
    elif is_data_related_query(message):
        reply = (
            "I can answer business and loan-related questions once a business profile is loaded or a document is uploaded. "
            "Please ask a question about the current business data or upload the relevant PDF."
        )
    else:
        reply = generate_general_chat_response(message)

    time.sleep(1)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    print("🚀 Lendly Server running at: http://127.0.0.1:5000")
    app.run(port=5000, debug=True)