from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

credenciais = 'contadeservico.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    credenciais, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    spreadsheet_id = data.get('id')
    range_name = data.get('range')
    chave = data.get('nome')

    if not spreadsheet_id or not range_name or not chave:
        return jsonify({"erro": "ID da planilha, intervalo e nome são necessários"}), 400

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    valor_encontrado = None

    # Procura pela palavra-chave em todas as células da planilha
    for row in values:
        if chave.upper() in (celula.strip().upper() for celula in row):
            # Encontra o índice da célula que contém a palavra-chave
            idx = row.index(chave)
            # Verifica se existe uma célula seguinte na mesma linha
            if idx + 1 < len(row):
                valor_encontrado = row[idx + 1]
                break

    if valor_encontrado is not None:
        return jsonify({"resultado": valor_encontrado})
    else:
        return jsonify({"erro": f"Nome {chave} não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
