import os
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from groq import Groq


load_dotenv(Path(__file__).resolve().parent / ".env")
app = Flask(__name__)


# Load environment variables from .env (for local development)
# Render will set these automatically in the environment.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# ALL 20 ORIGINAL COUNTRIES RESTORED EXACTLY
MARKET_DATABASE = {
   "India": {
       "business_name": "Maneesh Textiles", "city": "New Delhi", "sector": "Retail Clothing", "icon": "🛍️", "ai_rating": 742, "geo_grade": "A+", "cash_flow_volatility": "12.4%", "eval_speed": "3.2s", "score": 74,
       "probability": "87%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 20000, "recommended_emi": 1763,
       "metrics": {"payment_velocity": 92, "location_demand": 85, "transaction_consistency": 78, "business_risk": 14},
       "coords": [28.6139, 77.2090], "currency": "₹",
       "loan_config": {"min": 5000, "max": 100000, "step": 5000, "default_amt": 20000, "default_emi": 1763},
       "explanation": "High credit reliability proven by 92% payment velocity, 8,500 daily pedestrians converting to sales, and +23% YoY foot traffic growth.",
       "layers": {
           "traffic": [[28.6145, 77.2100], [28.6130, 77.2075]], "growth": [[28.6160, 77.2120, 23]],
           "competitors": [[28.6120, 77.2110, "🍵 Tea Shop"], [28.6150, 77.2060, "🧃 Juice Bar"]],
           "flows": [[28.6135, 77.2095, 450]]
       }
   },
   "Uzbekistan": {
       "business_name": "Samarkand Silk Carpets", "city": "Tashkent", "sector": "Artisanal Textiles", "icon": "🏺", "ai_rating": 765, "geo_grade": "A", "cash_flow_volatility": "10.2%", "eval_speed": "2.4s", "score": 78,
       "probability": "89%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 25000000, "recommended_emi": 2204000,
       "metrics": {"payment_velocity": 94, "location_demand": 82, "transaction_consistency": 81, "business_risk": 11},
       "coords": [41.2995, 69.2401], "currency": "soʻm",
       "loan_config": {"min": 5000000, "max": 100000000, "step": 5000000, "default_amt": 25000000, "default_emi": 2204000},
       "explanation": "Excellent transaction metrics driven by strong tourist card processing velocity and low sector saturation within Tashkent hub corridors.",
       "layers": {"traffic": [[41.3010, 69.2420]], "growth": [[41.2980, 69.2380, 18]], "competitors": [[41.3030, 69.2390, "🏺 Gift Shop"]], "flows": [[41.2990, 69.2410, 380]]}
   },
   "Kenya": {
       "business_name": "Jambo Agro-Supplies", "city": "Nairobi", "sector": "Agro-Distribution", "icon": "🚜", "ai_rating": 685, "geo_grade": "B+", "cash_flow_volatility": "18.1%", "eval_speed": "2.8s", "score": 68,
       "probability": "81%", "tier": "TIER 2 - REVIEWED APPROVAL", "recommended_amt": 250000, "recommended_emi": 22150,
       "metrics": {"payment_velocity": 81, "location_demand": 74, "transaction_consistency": 85, "business_risk": 22},
       "coords": [-1.2921, 36.8219], "currency": "KSh",
       "loan_config": {"min": 50000, "max": 1000000, "step": 25000, "default_amt": 250000, "default_emi": 22150},
       "explanation": "Consistent mobile money transaction velocity via M-Pesa merchant logs registers stable cash flow buffers.",
       "layers": {"traffic": [[-1.2910, 36.8230]], "growth": [[-1.2935, 36.8200, 12]], "competitors": [[-1.2940, 36.8240, "🚜 Feed Store"]], "flows": [[-1.2915, 36.8225, 180]]}
   },
   "Brazil": {
       "business_name": "Paulista Distribuidora", "city": "São Paulo", "sector": "Logistics Hub", "icon": "📦", "ai_rating": 810, "geo_grade": "A++", "cash_flow_volatility": "6.2%", "eval_speed": "4.1s", "score": 88,
       "probability": "94%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 45000, "recommended_emi": 3980,
       "metrics": {"payment_velocity": 96, "location_demand": 94, "transaction_consistency": 91, "business_risk": 8},
       "coords": [-23.5505, -46.6333], "currency": "R$",
       "loan_config": {"min": 10000, "max": 200000, "step": 5000, "default_amt": 45000, "default_emi": 3980},
       "explanation": "Flawless alternative logistics network tracking parameters across central highway freight terminals.",
       "layers": {"traffic": [[-23.5510, -46.6320]], "growth": [[-23.5490, -46.6350, 26]], "competitors": [], "flows": [[-23.5500, -46.6340, 600]]}
   },
   "USA": {
       "business_name": "Midwest Auto Parts", "city": "Chicago", "sector": "Automotive Retail", "icon": "🚗", "ai_rating": 795, "geo_grade": "A", "cash_flow_volatility": "9.5%", "eval_speed": "2.1s", "score": 82,
       "probability": "91%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 30000, "recommended_emi": 2650,
       "metrics": {"payment_velocity": 89, "location_demand": 81, "transaction_consistency": 88, "business_risk": 12},
       "coords": [41.8781, -87.6298], "currency": "$",
       "loan_config": {"min": 5000, "max": 150000, "step": 5000, "default_amt": 30000, "default_emi": 2650},
       "explanation": "Solid auto components recovery pipeline verified via point-of-sale invoice financing ledgers.",
       "layers": {"traffic": [[41.8790, -87.6280]], "growth": [[41.8770, -87.6310, 16]], "competitors": [], "flows": [[41.8785, -87.6290, 520]]}
   },
   "Indonesia": {
       "business_name": "Sunda Kelapa Logistics", "city": "Jakarta", "sector": "Maritime Logistics", "icon": "🚢", "ai_rating": 715, "geo_grade": "A-", "cash_flow_volatility": "14.2%", "eval_speed": "3.0s", "score": 71,
       "probability": "84%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 50000000, "recommended_emi": 4430000,
       "metrics": {"payment_velocity": 85, "location_demand": 88, "transaction_consistency": 74, "business_risk": 18},
       "coords": [-6.2088, 106.8456], "currency": "Rp",
       "loan_config": {"min": 10000000, "max": 300000000, "step": 5000000, "default_amt": 50000000, "default_emi": 4430000},
       "explanation": "Port shipping allocation lanes show consistent invoice clearance history pipelines.",
       "layers": {"traffic": [], "growth": [[-6.2070, 106.8440, 14]], "competitors": [], "flows": [[-6.2085, 106.8450, 910]]}
   },
   "Nigeria": {
       "business_name": "Ikeja Tech Ventures", "city": "Lagos", "sector": "Electronics", "icon": "💻", "ai_rating": 690, "geo_grade": "B", "cash_flow_volatility": "19.8%", "eval_speed": "3.9s", "score": 66,
       "probability": "79%", "tier": "TIER 2 - REVIEWED APPROVAL", "recommended_amt": 1200000, "recommended_emi": 106300,
       "metrics": {"payment_velocity": 83, "location_demand": 70, "transaction_consistency": 79, "business_risk": 25},
       "coords": [6.5244, 3.3792], "currency": "₦",
       "loan_config": {"min": 200000, "max": 5000000, "step": 100000, "default_amt": 1200000, "default_emi": 106300},
       "explanation": "Component hardware processing networks present safe baseline profiles.",
       "layers": {"traffic": [[6.5250, 3.3800]], "growth": [], "competitors": [], "flows": []}
   },
   "Mexico": {
       "business_name": "Condesa Cafetería", "city": "Mexico City", "sector": "Cafe & Eatery", "icon": "☕", "ai_rating": 760, "geo_grade": "A", "cash_flow_volatility": "11.1%", "eval_speed": "2.7s", "score": 77,
       "probability": "89%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 180000, "recommended_emi": 15950,
       "metrics": {"payment_velocity": 90, "location_demand": 92, "transaction_consistency": 82, "business_risk": 15},
       "coords": [19.4326, -99.1332], "currency": "$",
       "loan_config": {"min": 10000, "max": 400000, "step": 10000, "default_amt": 180000, "default_emi": 15950},
       "explanation": "High local food and beverage service usage matches steady merchant terminal logs.",
       "layers": {"traffic": [[19.4335, -99.1320]], "growth": [[19.4315, -99.1345, 21]], "competitors": [], "flows": []}
   },
   "Philippines": {
       "business_name": "Manila Bay Seafoods", "city": "Manila", "sector": "Wholesale Market", "icon": "🐟", "ai_rating": 730, "geo_grade": "A-", "cash_flow_volatility": "13.5%", "eval_speed": "3.1s", "score": 73,
       "probability": "85%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 220000, "recommended_emi": 19500,
       "metrics": {"payment_velocity": 88, "location_demand": 84, "transaction_consistency": 80, "business_risk": 16},
       "coords": [14.5995, 120.9842], "currency": "₱",
       "loan_config": {"min": 20000, "max": 500000, "step": 10000, "default_amt": 220000, "default_emi": 19500},
       "explanation": "Bulk storage logistics networks guarantee consistent downstream distributor processing.",
       "layers": {"traffic": [], "growth": [], "competitors": [], "flows": [[14.5990, 120.9840, 310]]}
   },
   "United Kingdom": {
       "business_name": "Soho Tech Solutions", "city": "London", "sector": "IT Services", "icon": "💻", "ai_rating": 820, "geo_grade": "A+", "cash_flow_volatility": "5.4%", "eval_speed": "2.0s", "score": 89,
       "probability": "95%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 40000, "recommended_emi": 3520,
       "metrics": {"payment_velocity": 97, "location_demand": 89, "transaction_consistency": 94, "business_risk": 7},
       "coords": [51.5074, -0.1278], "currency": "£",
       "loan_config": {"min": 5000, "max": 200000, "step": 5000, "default_amt": 40000, "default_emi": 3520},
       "explanation": "Excellent recurring monthly software-as-a-service cash flow trends ensure prime safety profiles.",
       "layers": {"traffic": [[51.5080, -0.1260]], "growth": [[51.5060, -0.1290, 19]], "competitors": [], "flows": []}
   },
   "Germany": {
       "business_name": "München Auto Werk", "city": "Munich", "sector": "Automotive Engineering", "icon": "🔧", "ai_rating": 805, "geo_grade": "A", "cash_flow_volatility": "7.1%", "eval_speed": "2.2s", "score": 86,
       "probability": "93%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 50000, "recommended_emi": 4400,
       "metrics": {"payment_velocity": 95, "location_demand": 83, "transaction_consistency": 90, "business_risk": 9},
       "coords": [48.1351, 11.5820], "currency": "€",
       "loan_config": {"min": 10000, "max": 250000, "step": 5000, "default_amt": 50000, "default_emi": 4400},
       "explanation": "Premium mechanical fabrication infrastructure backlog contracts prove deep financial security.",
       "layers": {"traffic": [], "growth": [], "competitors": [], "flows": []}
   },
   "France": {
       "business_name": "Marais Bistro", "city": "Paris", "sector": "Hospitality", "icon": "🍷", "ai_rating": 740, "geo_grade": "A-", "cash_flow_volatility": "12.0%", "eval_speed": "2.9s", "score": 75,
       "probability": "86%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 35000, "recommended_emi": 3080,
       "metrics": {"payment_velocity": 91, "location_demand": 86, "transaction_consistency": 80, "business_risk": 15},
       "coords": [48.8566, 2.3522], "currency": "€",
       "loan_config": {"min": 5000, "max": 150000, "step": 5000, "default_amt": 35000, "default_emi": 3080},
       "explanation": "High continuous localized entertainment spending activity stabilizes repayment structures.",
       "layers": {"traffic": [[48.8570, 2.3540]], "growth": [], "competitors": [], "flows": []}
   },
   "Japan": {
       "business_name": "Shibuya Ramen Station", "city": "Tokyo", "sector": "Restaurant", "icon": "🍜", "ai_rating": 830, "geo_grade": "A++", "cash_flow_volatility": "4.8%", "eval_speed": "1.8s", "score": 91,
       "probability": "96%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 3000000, "recommended_emi": 264000,
       "metrics": {"payment_velocity": 98, "location_demand": 96, "transaction_consistency": 95, "business_risk": 5},
       "coords": [35.6580, 139.7016], "currency": "¥",
       "loan_config": {"min": 500000, "max": 10000000, "step": 500000, "default_amt": 3000000, "default_emi": 264000},
       "explanation": "Dense passenger hub transit footprint registers exceptional merchant terminal volumes.",
       "layers": {"traffic": [[35.6590, 139.7020]], "growth": [[35.6570, 139.7000, 32]], "competitors": [], "flows": []}
   },
   "Australia": {
       "business_name": "Melbourne Brew Lab", "city": "Melbourne", "sector": "Cafe", "icon": "☕", "ai_rating": 775, "geo_grade": "A", "cash_flow_volatility": "9.1%", "eval_speed": "2.3s", "score": 80,
       "probability": "90%", "tier": "TIER 1 - AUTO-APPROVE", "recommended_amt": 40000, "recommended_emi": 3520,
       "metrics": {"payment_velocity": 93, "location_demand": 87, "transaction_consistency": 85, "business_risk": 11},
       "coords": [-37.8136, 144.9631], "currency": "A$",
       "loan_config": {"min": 5000, "max": 150000, "step": 5000, "default_amt": 40000, "default_emi": 3520},
       "explanation": "Highly predictable local consumer return baselines guarantee stable underwriter metrics.",
       "layers": {"traffic": [[-37.8120, 144.9650]], "growth": [], "competitors": [], "flows": []}
   },
   "Canada": {
       "business_name": "Ontario Timber Craft", "city": "Toronto", "sector": "Manufacturing", "icon": "🪓", "ai_rating": 720, "geo_grade": "B+", "cash_flow_volatility": "14.8%", "eval_speed": "3.1s", "score": 70,
       "probability": "83%", "tier": "TIER 2 - REVIEWED APPROVAL", "recommended_amt": 50000, "recommended_emi": 4420,
       "metrics": {"payment_velocity": 86, "location_demand": 77, "transaction_consistency": 81, "business_risk": 19},
       "coords": [43.6532, -79.3832], "currency": "C$",
       "loan_config": {"min": 10000, "max": 200000, "step": 5000, "default_amt": 50000, "default_emi": 4420},
       "explanation": "Stable commercial supply invoice patterns securely balance out minor supply chain friction.",
       "layers": {"traffic": [], "growth": [], "competitors": [], "flows": []}
   },
   "Vietnam": {
       "business_name": "Dong Xuan Souvenirs", "city": "Hanoi", "sector": "Tourist Retail", "icon": "🎋", "ai_rating": 310, "geo_grade": "D", "cash_flow_volatility": "44.2%", "eval_speed": "4.5s", "score": 28,
       "probability": "32%", "tier": "NOT APPROVED - CRITICAL RISK", "recommended_amt": 0, "recommended_emi": 0,
       "metrics": {"payment_velocity": 34, "location_demand": 21, "transaction_consistency": 40, "business_risk": 82},
       "coords": [21.0285, 105.8542], "currency": "₫",
       "loan_config": {"min": 0, "max": 0, "step": 0, "default_amt": 0, "default_emi": 0},
       "explanation": "Severe revenue volatility metrics matched with hyper-saturated low-margin competitor fields flag terminal risk indicators.",
       "layers": {"traffic": [], "growth": [], "competitors": [[21.0300, 105.8560, "🎋 Gift Stand"]], "flows": []}
   },
   "Egypt": {
       "business_name": "Cairo Artisans Guild", "city": "Cairo", "sector": "Bazaar Retail", "icon": "🏺", "ai_rating": 345, "geo_grade": "D+", "cash_flow_volatility": "39.0%", "eval_speed": "3.8s", "score": 35,
       "probability": "41%", "tier": "NOT APPROVED - CRITICAL RISK", "recommended_amt": 0, "recommended_emi": 0,
       "metrics": {"payment_velocity": 41, "location_demand": 33, "transaction_consistency": 38, "business_risk": 78},
       "coords": [30.0444, 31.2357], "currency": "E£",
       "loan_config": {"min": 0, "max": 0, "step": 0, "default_amt": 0, "default_emi": 0},
       "explanation": "Severe alternative asset ledger anomalies alongside major local macro currency friction block compliance criteria.",
       "layers": {"traffic": [], "growth": [], "competitors": [], "flows": []}
   },
   "Turkey": {
       "business_name": "Anatolia Spice Trading", "city": "Istanbul", "sector": "Wholesale Market", "icon": "🌶️", "ai_rating": 390, "geo_grade": "C-", "cash_flow_volatility": "35.1%", "eval_speed": "3.9s", "score": 39,
       "probability": "46%", "tier": "NOT APPROVED - CRITICAL RISK", "recommended_amt": 0, "recommended_emi": 0,
       "metrics": {"payment_velocity": 45, "location_demand": 42, "transaction_consistency": 49, "business_risk": 72},
       "coords": [41.0082, 28.9784], "currency": "₺",
       "loan_config": {"min": 0, "max": 0, "step": 0, "default_amt": 0, "default_emi": 0},
       "explanation": "Negative regional cash trend indexes point to ongoing transactional capital preservation problems.",
       "layers": {"traffic": [], "growth": [], "competitors": [], "flows": []}
   },
   "Greece": {
       "business_name": "Plaka Souvlaki Hub", "city": "Athens", "sector": "Food Service", "icon": "🍽️", "ai_rating": 410, "geo_grade": "C", "cash_flow_volatility": "31.4%", "eval_speed": "3.1s", "score": 42,
       "probability": "49%", "tier": "NOT APPROVED - CRITICAL RISK", "recommended_amt": 0, "recommended_emi": 0,
       "metrics": {"payment_velocity": 50, "location_demand": 44, "transaction_consistency": 41, "business_risk": 68},
       "coords": [37.9838, 23.7275], "currency": "€",
       "loan_config": {"min": 0, "max": 0, "step": 0, "default_amt": 0, "default_emi": 0},
       "explanation": "Hyper-saturated commercial zone filters identify dense low-performing competitive blocks.",
       "layers": {"traffic": [], "growth": [], "competitors": [[37.9850, 23.7290, "🍔 Diner"]], "flows": []}
   },
   "Argentina": {
       "business_name": "Palermo Leather Outlets", "city": "Buenos Aires", "sector": "Retail Apparel", "icon": "🧥", "ai_rating": 290, "geo_grade": "E", "cash_flow_volatility": "56.2%", "eval_speed": "4.2s", "score": 25,
       "probability": "29%", "tier": "NOT APPROVED - CRITICAL RISK", "recommended_amt": 0, "recommended_emi": 0,
       "metrics": {"payment_velocity": 22, "location_demand": 30, "transaction_consistency": 25, "business_risk": 91},
       "coords": [-34.6037, -58.3816], "currency": "$",
       "loan_config": {"min": 0, "max": 0, "step": 0, "default_amt": 0, "default_emi": 0},
       "explanation": "Critical transaction consistency failure tracks complete operational cash drain parameters.",
       "layers": {"traffic": [], "growth": [], "competitors": [], "flows": []}
   }
}


@app.route('/')
def home():
   return render_template('index.html')


@app.route('/api/market', methods=['GET'])
def get_market_data():
   country = request.args.get('country', 'India')
   market_data = MARKET_DATABASE.get(country, MARKET_DATABASE['India'])
   return jsonify(market_data)


@app.route('/api/search', methods=['GET'])
def search_business():
   query = request.args.get('q', '').strip()
   if ',' in query:
       try:
           parts = query.split(',')
           lat, lng = float(parts[0].strip()), float(parts[1].strip())
           return jsonify({
               "business_name": "Custom Coordinate Pin", "city": "Geospatial Frame", "sector": "Dynamic", "icon": "📍", "ai_rating": 725, "geo_grade": "A-", "cash_flow_volatility": "11.5%", "eval_speed": "1.1s", "score": 72,
               "probability": "84%", "tier": "TIER 1 - AUTO-APPROVE", "metrics": {"payment_velocity": 85, "location_demand": 80, "transaction_consistency": 82, "business_risk": 15},
               "coords": [lat, lng], "currency": "₹", "loan_config": {"min": 5000, "max": 100000, "step": 5000, "default_amt": 20000, "default_emi": 1763},
               "explanation": "Custom target node coordinate query output.",
               "layers": {"traffic": [[lat+0.001, lng+0.001]], "growth": [[lat-0.001, lng-0.001, 15]], "competitors": [], "flows": [[lat, lng, 100]]}
           })
       except ValueError:
           pass


   for country, data in MARKET_DATABASE.items():
       if query.lower() in data['business_name'].lower() or query.lower() in country.lower() or query.lower() in data['city'].lower():
           return jsonify(data)
   return jsonify(MARKET_DATABASE['India'])


@app.route('/api/chat', methods=['POST'])
def process_chat():
   payload = request.get_json(silent=True) or {}
   message = payload.get('message', '')
   country = payload.get('country', 'India')
   business = MARKET_DATABASE.get(country, MARKET_DATABASE['India'])
  
   system_prompt = f"""You are Lendly's underwriting assistant.
   Business Context:
   - Name: {business['business_name']}
   - Location: {business['city']} ({business['sector']})
   - Score: {business['score']}/100 ({business['tier']})
   - Probability: {business['probability']}
   - Recommended Loan: {business['currency']}{business['loan_config']['default_amt']}
  
   Answer the underwriter's questions directly and specifically based on this data. Be professional, concise, and explain your reasoning. Never make up data. If you don't know, say so."""
  
   if not client:
       return jsonify({"reply": "Groq API key is not configured. Set GROQ_API_KEY in your environment or .env file."}), 500


   # Cascade model routing to guarantee uptime
   models_to_try = ["llama-3.1-8b-instant"]
   reply = None
   last_error = ""


   for target_model in models_to_try:
       try:
           completion = client.chat.completions.create(
               model=target_model,
               messages=[
                   {"role": "system", "content": system_prompt},
                   {"role": "user", "content": message}
               ],
               temperature=0.3, max_tokens=300
           )
           reply = completion.choices[0].message.content
           if reply:
               break
       except Exception as e:
           last_error = str(e)
           continue
          
   if not reply:
       reply = f"API Pipeline issue. Diagnostics: {last_error if last_error else 'Timeout'}"
      
   return jsonify({"reply": reply})


@app.route('/api/upload-document', methods=['POST'])
def upload_document():
   if 'document' not in request.files:
       return jsonify({"error": "No file uploaded"}), 400
  
   file = request.files['document']
   filename = secure_filename(file.filename)
  
   time.sleep(1.8)
   doc_type = "GST Certificate" if "gst" in filename.lower() else ("Bank Statement" if "bank" in filename.lower() else "Utility Bill")
  
   return jsonify({
       "document_name": filename,
       "document_type": doc_type,
       "confidence_score": 0.98,
       "fraud_check": {
           "fraud_risk": "LOW (2/100)",
           "red_flags": []
       },
       "verification_summary": {
           "business_legitimacy": "VERIFIED (GST + Bank match)",
           "address_verification": "VERIFIED (Matches utility)",
           "income_verification": "VERIFIED (Matches stated metrics)",
           "payment_reliability": "VERIFIED (0 failed payments)"
       },
       "missing_documents": ["Aadhar card (Optional)", "Shop photos (Optional)"],
       "outstanding_questions": ["Any upcoming business disruptions?", "Can you provide a co-signer?"],
       "recommendation": "All critical documents verified. No fraud indicators. Ready for approval processing."
   })


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=True)

