from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import os

app = Flask(__name__)
CORS(app)  # Permite CORS desde cualquier origen

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1EyaRCaJdyDXgKxcJ34fBydxcAbBNhmMxXbZxZ4UQg84'  # ID de tu Google Sheet

# Cargar credenciales desde variable de entorno
creds_json = os.environ.get('GOOGLE_CREDS')
if not creds_json:
    raise ValueError("No se encontró la variable de entorno GOOGLE_CREDS")
creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Inicializar servicio de Google Sheets
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

@app.route('/guardar_reporte', methods=['POST'])
def guardar_reporte():
    datos = request.json
    try:
        tareas_realizadas = [k.replace("_", " ").capitalize() for k,v in datos['tareas'].items() if v == 'si']
        accesorios_malos = [k.replace("_", " ").capitalize() for k,v in datos['accesorios'].items() if v == 'no']

        fila = [
            datos.get('nombre', ''),
            datos.get('marca', ''),
            datos.get('modelo', ''),
            datos.get('anio', ''),
            datos.get('chapa', ''),
            datos.get('km', ''),
            datos.get('fecha', ''),
            datos.get('tecnico', ''),
            ", ".join(tareas_realizadas),
            ", ".join(accesorios_malos)
        ]

        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='A1',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': [fila]}
        ).execute()

        return jsonify({'result': 'success', 'details': result}), 200
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
