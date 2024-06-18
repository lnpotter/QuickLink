from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient

app = Flask(__name__)