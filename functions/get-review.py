from flask import Flask, request, jsonify
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

app = Flask(__name__)

def db_cloudant_connect():
    try:
        client = Cloudant(
            '3aa297bd-7a6c-4bd8-b39b-ed6410efe4e8-bluemix',
            '_byEPlSJlhupgrRH3elkFh0lbsBiHUHQh67-d6P_fGyF',
            url='https://3aa297bd-7a6c-4bd8-b39b-ed6410efe4e8-bluemix.cloudantnosqldb.appdomain.cloud',
            connect=True
        )
        db = client['reviews']
        print('¡Connection Success! Connected to DB')
        return db
    except CloudantException as ce:
        print('Connection error: ' + ce.message + ' for DB Cloudant')
        raise ce

db = db_cloudant_connect()

@app.route('/api/review', methods=['GET'])
def get_reviews():
    dealer_id = request.args.get('dealerId')

    if not dealer_id:
        return jsonify({'error': 'dealerId param required'}), 400

    try:
        result_collection = Result(db.all_docs, include_docs=True, conflicts=True)
        reviews = [doc['doc'] for doc in result_collection if 'dealer_id' in doc['doc'] and doc['doc']['dealer_id'] == int(dealer_id)]

        if not reviews:
            return jsonify({'error': 'dealerId does not exist'}), 404

        return jsonify(reviews)
    except Exception as e:
        print('reviews error:', str(e))
        return jsonify({'error': 'Something went wrong on the server'}), 500

@app.route('/api/review', methods=['POST'])
def post_review():
    try:
        review_data = request.get_json()

        if 'review' not in review_data:
            return jsonify({'error': '"review" object is required'}), 400

        new_review = review_data['review']
        db.create_document(new_review)

        return jsonify({'message': 'Review created successfully'}), 201
    except Exception as e:
        print('Error in review creation:', str(e))
        return jsonify({'error': 'Something went wrong on the server'}), 500

if __name__ == '__main__':
    app.run(debug=True)
