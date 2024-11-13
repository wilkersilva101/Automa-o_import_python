from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd

# Escopos para a API do Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheet_ids(service, spreadsheet_id):
    # Obter as propriedades das abas da planilha
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheet_ids = {}
    for sheet in sheets:
        title = sheet['properties']['title']
        sheet_id = sheet['properties']['sheetId']
        sheet_ids[title] = sheet_id
    return sheet_ids

def get_filtered_cpfs():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # ID da planilha
    spreadsheet_id = '16hzIW5ImASPiEIwvzgoQfFo1y-b2nYrK9rDyK4qTWUQ'

    # Obter os IDs das abas
    sheet_ids = get_sheet_ids(service, spreadsheet_id)

    cpfs_servidores = []
    cpfs_estagiarios = []

    try:
        # Processando planilha "SERVIDORES"
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range='SERVIDORES!A1:G1794').execute()
        values = result.get('values', [])

        if values:
            columns = values[0]
            data = values[1:]
            df = pd.DataFrame(data, columns=columns)

            # Filtragem
            mask = (df['Pendência'].str.lower().eq('deferido')) & (df['Resolvido?'].isna())

            df_filtered = df.loc[mask].copy()

            # Atualizando 'Resolvido?'
            df.loc[mask, 'Resolvido?'] = 'sim'

            print("Registros filtrados (SERVIDORES):")
            print(df_filtered)

            # Atualizando planilha com as mudanças
            update_range = f'SERVIDORES!G2:G{len(df) + 1}'
            body = {
                'values': df['Resolvido?'].values.reshape(-1, 1).tolist()
            }
            sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW',
                                  body=body).execute()

            # Aplicando formatação condicional
            requests = []
            for index, row in df_filtered.iterrows():
                start_row = index + 2
                end_row = start_row
                requests.append({
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_ids['SERVIDORES'],
                            'startRowIndex': start_row - 1,
                            'endRowIndex': end_row,
                            'startColumnIndex': 0,
                            'endColumnIndex': len(columns)
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {
                                    'red': 0.0,
                                    'green': 0.5,
                                    'blue': 0.0
                                }
                            }
                        },
                        'fields': 'userEnteredFormat.backgroundColor'
                    }
                })

            if requests:
                body = {
                    'requests': requests
                }
                sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

            # Processando CPFs
            if 'CPF' in df_filtered.columns:
                df_filtered['CPF'] = df_filtered['CPF'].str.replace('.', '').str.replace('-', '').str.replace('\r\n', '')
            cpfs_servidores = df_filtered['CPF'].tolist()
            print("CPFs processados (SERVIDORES):", cpfs_servidores)

    except Exception as e:
        print(f"Erro ao processar a planilha 'SERVIDORES': {e}")

    try:
        # Processando planilha "ESTAGIÁRIOS NOVOS"
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range='ESTAGIÁRIOS NOVOS!A1:D900').execute()
        values = result.get('values', [])

        if values:
            columns = values[0]
            data = values[1:]
            df = pd.DataFrame(data, columns=columns)

            # Filtragem
            mask = (df['Pendência'].str.lower().eq('deferido')) & (df['Resolvido?'].isna())

            df_filtered = df.loc[mask].copy()

            # Atualizando 'Resolvido?'
            df.loc[mask, 'Resolvido?'] = 'sim'

            print("Registros filtrados (ESTAGIÁRIOS NOVOS):")
            print(df_filtered)

            # Atualizando planilha com as mudanças
            update_range = f'ESTAGIÁRIOS NOVOS!D2:D{len(df) + 1}'
            body = {
                'values': df['Resolvido?'].values.reshape(-1, 1).tolist()
            }
            sheet.values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW',
                                  body=body).execute()

            # Aplicando formatação condicional
            requests = []
            for index, row in df_filtered.iterrows():
                start_row = index + 2
                end_row = start_row
                requests.append({
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_ids['ESTAGIÁRIOS NOVOS'],
                            'startRowIndex': start_row - 1,
                            'endRowIndex': end_row,
                            'startColumnIndex': 0,
                            'endColumnIndex': len(columns)
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': {
                                    'red': 0.0,
                                    'green': 0.5,
                                    'blue': 0.0
                                }
                            }
                        },
                        'fields': 'userEnteredFormat.backgroundColor'
                    }
                })

            if requests:
                body = {
                    'requests': requests
                }
                sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

            # Processando CPFs
            if 'CPF' in df_filtered.columns:
                df_filtered['CPF'] = df_filtered['CPF'].str.replace('.', '').str.replace('-', '').str.replace('\r\n', '')
            cpfs_estagiarios = df_filtered['CPF'].tolist()
            print("CPFs processados (ESTAGIÁRIOS NOVOS):", cpfs_estagiarios)

    except Exception as e:
        print(f"Erro ao processar a planilha 'ESTAGIÁRIOS NOVOS': {e}")

    # Verificação final dos CPFs
    all_cpfs = cpfs_servidores + cpfs_estagiarios
    if all_cpfs:
        print("CPFs filtrados:")
        print("Servidores:", cpfs_servidores)
        print("Estagiários Novos:", cpfs_estagiarios)
        print("Todos os CPFs:", all_cpfs)
    else:
        print("Não há CPFs para importação.")

    return all_cpfs