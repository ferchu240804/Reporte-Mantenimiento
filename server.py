from flask import Flask, request, jsonify
from flask_cors import CORS
import openpyxl
import os

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

RUTA_EXCEL = "reportes_mantenimiento.xlsx"

def guardar_en_excel(datos):
    if os.path.exists(RUTA_EXCEL):
        wb = openpyxl.load_workbook(RUTA_EXCEL)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        # Crear encabezados
        encabezados = [
            "Nombre", "Marca", "Modelo", "Año", "Chapa", "Kilometraje", "Fecha", "Técnico",
            "Tareas realizadas", "Accesorios en mal estado"
        ]
        ws.append(encabezados)

    tareas_realizadas = [k.replace("_", " ").capitalize() for k, v in datos["tareas"].items() if v == "si"]
    accesorios_malos = [k.replace("_", " ").capitalize() for k, v in datos["accesorios"].items() if v == "no"]

    fila = [
        datos.get("nombre", ""),
        datos.get("marca", ""),
        datos.get("modelo", ""),
        datos.get("anio", ""),
        datos.get("chapa", ""),
        datos.get("km", ""),
        datos.get("fecha", ""),
        datos.get("tecnico", ""),
        ", ".join(tareas_realizadas),
        ", ".join(accesorios_malos)
    ]

    ws.append(fila)
    wb.save(RUTA_EXCEL)

@app.route('/guardar_reporte', methods=['POST'])
def guardar_reporte():
    datos = request.json
    try:
        guardar_en_excel(datos)
        return jsonify({"mensaje": "Guardado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
