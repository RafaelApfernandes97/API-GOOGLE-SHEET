from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'contadeservico.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)

SAMPLE_SPREADSHEET_ID = '16MYWTifM3_29RtB2UIYnfGnvA3ilbjjW3_qsY-3Utjg'
SAMPLE_RANGE_NAME = 'sheet!A1:B10'

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
else:
    for row in values:
        print(', '.join(row))

    # Adicione aqui a funcionalidade de pesquisa
    nome_procurado = "João"
    valor_encontrado = None

    for row in values:
        if len(row) >= 2 and row[0].strip().upper() == nome_procurado.upper():
            valor_encontrado = row[1]
            break

    if valor_encontrado:
        print(f"Valor encontrado para {nome_procurado}: {valor_encontrado}")
    else:
        print(f"Nome {nome_procurado} não encontrado.")
