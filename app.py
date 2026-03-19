# -*- coding: utf-8 -*-
"""
中医辨证 API - 后端服务
用于 Render 部署
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys

# 添加模型路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # 允许跨域

# 加载模型
from tcm_model_v4 import (
    FORMULAS, LUNG_NODULE_FORMULA, diagnose, 
    get_model_info, search_knowledge, 
    人纪教程, 天纪教程, 经典注解
)

@app.route('/')
def home():
    """首页"""
    return jsonify({
        "name": "倪海厦中医辨证 API",
        "version": "4.0",
        "status": "running"
    })

@app.route('/api/info')
def info():
    """模型信息"""
    return jsonify(get_model_info())

@app.route('/api/diagnose', methods=['POST'])
def api_diagnose():
    """辨证接口"""
    data = request.json
    
    symptoms = data.get('symptoms', [])
    tongue = data.get('tongue', '')
    pulse = data.get('pulse', '')
    has_nodule = data.get('has_nodule', False)
    
    results = diagnose(symptoms, tongue, pulse, has_nodule)
    
    return jsonify({
        "symptoms": symptoms,
        "results": results
    })

@app.route('/api/formulas')
def get_formulas():
    """获取所有方剂"""
    return jsonify(FORMULAS)

@app.route('/api/formula/<name>')
def get_formula(name):
    """获取单个方剂"""
    formula = FORMULAS.get(name)
    if formula:
        return jsonify({"name": name, **formula})
    return jsonify({"error": "方剂不存在"}), 404

@app.route('/api/search')
def api_search():
    """搜索知识库"""
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    
    results = search_knowledge(query, category)
    return jsonify({"query": query, "results": results})

@app.route('/api/renji')
def get_renji():
    """获取人纪教程列表"""
    return jsonify({
        "subjects": list(人纪教程.keys()),
        "count": {k: len(v) for k, v in 人纪教程.items()}
    })

@app.route('/api/tianji')
def get_tianji():
    """获取天纪教程列表"""
    return jsonify({
        "subjects": list(天纪教程.keys()),
        "count": {k: len(v) for k, v in 天纪教程.items()}
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
