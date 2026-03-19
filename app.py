# -*- coding: utf-8 -*-
"""
中医辨证 API - 后端服务
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

from tcm_model import (
    FORMULAS, LUNG_NODULE_FORMULA, diagnose, 
    get_model_info, search_knowledge
)

@app.route('/')
def home():
    return jsonify({
        "name": "倪海厦中医辨证 API",
        "version": "4.0",
        "status": "running"
    })

@app.route('/api/info')
def info():
    return jsonify(get_model_info())

@app.route('/api/diagnose', methods=['POST'])
def api_diagnose():
    data = request.json
    symptoms = data.get('symptoms', [])
    tongue = data.get('tongue', '')
    pulse = data.get('pulse', '')
    has_nodule = data.get('has_nodule', False)
    results = diagnose(symptoms, tongue, pulse, has_nodule)
    return jsonify({"symptoms": symptoms, "results": results})

@app.route('/api/formulas')
def get_formulas():
    return jsonify(FORMULAS)

@app.route('/api/formula/<name>')
def get_formula(name):
    formula = FORMULAS.get(name)
    if formula:
        return jsonify({"name": name, **formula})
    return jsonify({"error": "方剂不存在"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
