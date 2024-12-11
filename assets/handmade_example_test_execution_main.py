import os
import pandas as pd
from datetime import datetime

# Definir caminho de saída
output_folder = os.path.join('./assets/docs_output/', f'Teste Execução - {datetime.now().strftime("%d_%m_%Y")} - Test_Execution_data Template.xlsx')

# Ler o ficheiro Excel
try:
    df = pd.read_excel('./assets/docs_input/Test_Execution_data Template.xlsx', header=None)
except Exception as e:
    print(f'Erro ao ler o ficheiro: {e}')
    exit()

# Validar estrutura do ficheiro Teste Execução
if df.iloc[0, 0] == 'Test execution' and df.iloc[1, 0] == 'Total run time':
    print('Estrutura de Teste Execução identificada corretamente')
else:
    print('Estrutura inválida. O ficheiro será marcado como INVÁLIDO')

# Ação 4.1: Localizar a linha de cabeçalho da tabela
try:
    expected_columns = ['ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds']
    table_header_rows = df[df.apply(lambda row: all(col in row.values for col in expected_columns), axis=1)].index
    if table_header_rows.empty:
        print(f'Erro na ação 4.1 - Linha correspondente às colunas {expected_columns} não encontrada.')
    else:
        table_header_row = table_header_rows[0]
        print(f'Ação 4.1 executada com sucesso - O cabeçalho corresponde à linha {table_header_row}')
except Exception as e:
    print(f'Erro na ação 4.1 - {str(e)}')

# Ação 4.2: Remover a linha 3 (index 2) se estiver vazia
if df.iloc[2].isnull().all():
    df = df.drop(2)
    print('Ação 4.2 executada com sucesso - Linha 3 removida')
    table_header_row -= 1
    print(f'Ação 4.1 - Nova linha de cabeçalho = {table_header_row}')
    df.to_excel(output_folder, index=False, header=False)
else:
    print('Ação 4.2 ignorada - Linha 3 não estava vazia')

# Ação 4.3: Adicionar uma nova linha branca por cima da linha 1
new_row = pd.DataFrame([[''] * len(df.columns)], columns=df.columns)
df = pd.concat([new_row, df]).reset_index(drop=True)
print('Ação 4.3 executada com sucesso - Linha branca adicionada')
table_header_row += 1
print(f'Ação 4.1 - Nova linha de cabeçalho = {table_header_row}')
df.to_excel(output_folder, index=False, header=False)

# Ação 4.4: Reordenar as colunas da tabela
try:
    table_last_row = df.last_valid_index()
    
    # Selecionar a parte do DataFrame que contém os dados, incluindo o cabeçalho
    data_to_sort = df.iloc[table_header_row:table_last_row + 1]  # +1 para incluir a última linha
    
    # Definindo os cabeçalhos para a parte selecionada
    data_to_sort.columns = df.iloc[table_header_row]  # Definindo a linha do cabeçalho como colunas

    # Reordenar as colunas conforme a lista definida
    data_to_sort = data_to_sort[expected_columns]  # Reordenando as colunas
    
    # Substituir os dados no DataFrame original
    df.iloc[table_header_row:table_last_row + 1] = data_to_sort.values  # Atualiza a parte relevante

    print('Ação 4.4 executada com sucesso - Colunas reordenadas')
    df.to_excel(output_folder, index=False, header=False)
except KeyError as e:
    print(f'Erro na ação 4.4 - Falta de colunas esperadas: {e}')


# Ação 4.5: Substituir pontos por vírgulas na coluna TaskWorkload da tabela
try:
    # Verifique se a linha de cabeçalho foi definida e se a coluna 'TaskWorkload' está presente
    if table_header_row is not None and table_header_row < len(df):
        # Acessa a coluna 'TaskWorkload' usando o cabeçalho definido
        task_workload_col_index = df.iloc[table_header_row].tolist().index('TaskWorkload')
        
        # Aplicar a substituição de pontos por vírgulas
        df.iloc[table_header_row + 1:, task_workload_col_index] = df.iloc[table_header_row + 1:, task_workload_col_index].apply(lambda x: str(x).replace('.', ','))
        
        print('Ação 4.5 executada com sucesso - Valores de TaskWorkload ajustados')
        df.to_excel(output_folder, index=False, header=False)
    else:
        print('Erro na ação 4.5 - Linha de cabeçalho não encontrada ou inválida')
except Exception as e:
    print(f'Erro na ação 4.5 - {str(e)}')

# Ação 4.6: Adicionar o somatório de RunTimeSeconds e TaskWorkload
try:
    # Verificar se as linhas de cabeçalho e última linha são válidas
    if table_header_row is not None and table_last_row is not None and table_last_row >= table_header_row:
        # Criar uma nova linha para os totais
        df.loc[len(df)] = [None] * df.shape[1]  # Adiciona uma nova linha vazia

        # Acessa a coluna 'RunTimeSeconds' usando o cabeçalho definido
        task_runtimeseconds_col_index = df.iloc[table_header_row].tolist().index('RunTimeSeconds')
        # Calcular o somatório de RunTimeSeconds
        total_runtime = df.iloc[table_header_row + 1:table_last_row + 1, task_runtimeseconds_col_index].sum()
        df.iloc[len(df) - 1, task_runtimeseconds_col_index] = total_runtime  # Atribui o total a RunTimeSeconds
        # Adicionar a linha de totais ao DataFrame
        df.to_excel(output_folder, index=False, header=False)
        print('Ação 4.6 executada com sucesso - Somatório de RunTimeSeconds adicionado')
        
        # Acessa a coluna 'TaskWorkload' usando o cabeçalho definido
        task_taskworkload_col_index = df.iloc[table_header_row].tolist().index('TaskWorkload')
        # Calcular o somatório de TaskWorkload, convertendo para float
        total_taskworkload = df.iloc[table_header_row + 1:table_last_row + 1, task_taskworkload_col_index].apply(lambda x: float(str(x).replace(',', '.'))).sum()
        df.iloc[len(df) - 1, task_taskworkload_col_index] = f'{total_taskworkload:.5f}'.replace('.', ',')  # Atribui o total a TaskWorkload
        # Adicionar a linha de totais ao DataFrame
        df.to_excel(output_folder, index=False, header=False)
        print('Ação 4.6 executada com sucesso - Somatório de TaskWorkload adicionado')
    else:
        print('Erro na ação 4.6 - Linhas de cabeçalho ou última linha inválidas')
except KeyError as e:
    print(f'Erro na ação 4.6 - Coluna em falta: {e}')
except Exception as e:
    print(f'Erro na ação 4.6 - {str(e)}')

# Guardar o ficheiro processado
try:
    df.to_excel(output_folder, index=False, header=False)
    print('Ficheiro guardado com sucesso')
except Exception as e:
    print(f'Erro ao guardar o ficheiro: {e}')
