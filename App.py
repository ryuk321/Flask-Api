from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


import os
import json

app = Flask(__name__)
CORS(app)


"""Do not submit this apis  directly to this code. USe Heroku Variables
"""

# 🔧 Set up credentials and gspread client
GOOGLE_SHEET_ID = "1UP4h4JdctiWvpWftCQ7I3NI5RJy7I9dU6zLZUDR2ejk"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# json_filename = "service_account.json"
# with open(json_filename, "r") as f:
#     credentials_dict = json.load(f)
#     print(credentials_dict)
#
#
# gc = gspread.service_account_from_dict(credentials_dict)

GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
credentials_dict = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
gc = gspread.service_account_from_dict(credentials_dict)


sh = gc.open_by_key(GOOGLE_SHEET_ID)

worksheet = sh.worksheet("Applications")





@app.route('/write-to-sheet', methods=['POST'])
def write_to_sheet():
    try:
        data = request.get_json()
        values = data.get('values')
        print(values)
        row = ParseTheData(values)
        print("New Vlaeus",values)


        if not values:
            return jsonify({'error': 'Missing "values" in request'}), 400

        sh = gc.open_by_key(GOOGLE_SHEET_ID)
        worksheet =  sh.worksheet('Applications')



        worksheet.append_row(row)

        return jsonify({'status': 'success', 'rows_added': len(values)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route("/apply", methods=["POST"])
def apply():
    data = request.get_json()
    print("📨 New Application Received:")
    for key, value in data.items():
        print(f"{key}: {value}")

    return jsonify({"message": "Application submitted successfully!"})


def ParseTheData(Data):
    try:
        print("Got the data", Data)
        print("Got the length data", len(Data))
        if len(Data)==2:
            print(Data)# [[heading],[column]]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [timestamp]+Data[1]
            print(data)
            return data
    except Exception as e:
        print("Exception : ", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)