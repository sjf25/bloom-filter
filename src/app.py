from flask import Flask, request, jsonify
from flask_cors import CORS
from bloom_filter import BloomFilter
from hashlib import sha1
import os

app = Flask(__name__)
CORS(app)

def get_bf():
    file_dir = os.path.abspath(os.path.dirname(__file__))
    in_file_path = os.path.join(file_dir, 'password_data')
    in_file = open(in_file_path, 'rb')
    return BloomFilter.open(in_file)

bf = get_bf()

@app.route('/query-passwords', methods=['GET'])
def query_passwords():
    global bf
    if not bf is None:
        query = request.args.get('query')
        query_sha = sha1(query.encode('utf-8')).digest()
        in_filter = bf.maybe_element(query_sha)
        return jsonify({'query': query, 'in_filter': in_filter})
    else:
        return jsonify({'error': 'bloom filter not initalized'})

if __name__ == '__main__':
    app.run()

