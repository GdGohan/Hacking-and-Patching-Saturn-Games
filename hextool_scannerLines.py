import os
import subprocess
import re

# --- CONFIGURAÇÕES FIXAS ---
pasta_atual = os.path.dirname(os.path.abspath(__file__))

executable = os.path.join(pasta_atual, "Extracted", "byte_search.exe") # O executável do ByteSearch
ficheiro_saida = os.path.join(pasta_atual, "output.txt") # Onde os resultados vão ser guardados

# Tamanho da linha em bytes: Largura (96) / 2 (porque é 4 BPP) = 48 bytes por linha
BYTES_POR_LINHA = 16

# --- VALIDAÇÃO DO EXECUTÁVEL ---
if not os.path.exists(executable):
    print(f"ERRO: O executável '{executable}' não foi encontrado!")
    print("Certifica-se de que a pasta 'Extracted' com o 'byte_search.exe' está no mesmo local deste script.")
    exit()

# --- AJUDA VISUAL: LISTAR BINS DISPONÍVEIS NA PASTA REAL ---
print("Ficheiros .bin encontrados na pasta do script:")
ficheiros_na_pasta = [f for f in os.listdir(pasta_atual) if f.endswith('.bin')]
for f in ficheiros_na_pasta:
    print(f"  -> {f}")
print("-" * 50)

# --- PEDIR O NOME DO FICHEIRO AO UTILIZADOR ---
ficheiro_input = input("Digite o nome ou caminho do seu ficheiro de dump (ex: SaveMemoryButton): ").strip()

if not ficheiro_input.endswith('.bin'):
    ficheiro_input += '.bin'

ficheiro_binario = os.path.join(pasta_atual, ficheiro_input)

if not os.path.exists(ficheiro_binario):
    print(f"ERRO: O ficheiro '{ficheiro_input}' não foi encontrado!")
    exit()

print(f"\nA abrir '{ficheiro_input}' de forma absoluta...")
print("A executar o ByteSearch com filtro de precisão...\n")

# Listas temporárias para organizar o relatório final
resultados_ideais = []
relatorio_completo = []
num_linha = 0

# --- PROCESSAMENTO EM MEMÓRIA ---
with open(ficheiro_binario, "rb") as f_bin:
    while True:
        bytes_lidos = f_bin.read(BYTES_POR_LINHA)
        if not bytes_lidos:
            break
            
        num_linha += 1
        linha_hex = bytes_lidos.hex().upper()
        
        print(f"A testar Linha {num_linha:02d}...")
        
        comando = [executable, "--quick", linha_hex]
        
        try:
            resultado = subprocess.run(
                comando, 
                capture_output=True, 
                text=True, 
                check=True, 
                cwd=os.path.dirname(executable)
            )
            output_cmd = resultado.stdout
            
            # Guardamos o log desta linha para o relatório geral
            bloco_texto = f"--- Linha {num_linha:02d} ---\nString Hexadecimal: {linha_hex}\n{output_cmd}"
            relatorio_completo.append(bloco_texto)
            
            # --- FILTRO INTELIGENTE (1 MATCH TOTAL) ---
            if "Found 1 match total." in output_cmd:
                # O novo regex ignora o ".\" opcional e pega direto o nome do arquivo .bin
                match_file = re.search(r'>\s*(?:\.\\)?(.+\.bin)', output_cmd)
                match_offset = re.search(r'Offset\s+(0x[0-9A-Fa-f]+)', output_cmd)
                
                if match_file and match_offset:
                    nome_arquivo = match_file.group(1)
                    offset_encontrado = match_offset.group(1)
                    resultados_ideais.append(
                        f"  [ALVO ENCONTRADO] Linha {num_linha:02d} -> Ficheiro: {nome_arquivo} | No Offset: {offset_encontrado}"
                    )
                    
        except subprocess.CalledProcessError as e:
            relatorio_completo.append(f"--- Linha {num_linha:02d} ---\nErro ao executar o comando.\n")

# --- ESCRITA FINAL DO RELATÓRIO ESTRUTURADO ---
with open(ficheiro_saida, "w", encoding="utf-8") as f_out:
    f_out.write("==================================================\n")
    f_out.write(f"RELATÓRIO DE VARREDURA AUTOMÁTICA: {ficheiro_input}\n")
    f_out.write("==================================================\n\n")
    
    # 1. EXIBIR ALVOS PERFEITOS NO TOPO
    f_out.write("🎯 ===============================================\n")
    f_out.write("🎯    RESULTADOS IDEAIS ENCONTRADOS (1x1 MATCH)   \n")
    f_out.write("🎯 ===============================================\n")
    if resultados_ideais:
        for ideal in resultados_ideais:
            f_out.write(ideal + "\n")
    else:
        f_out.write("  Nenhuma linha única isolada foi encontrada. Todas as sequências possuem múltiplos matches.\n")
    f_out.write("\n" + "="*50 + "\n\n")
    
    # 2. SEGUIDO PELO DUMP COMPLETO (Para consulta detalhada se necessário)
    f_out.write("🔍 ===============================================\n")
    f_out.write("🔍          LOG DETALHADO LINHA POR LINHA          \n")
    f_out.write("🔍 ===============================================\n\n")
    for bloco in relatorio_completo:
        f_out.write(bloco)
        f_out.write("\n" + "-"*40 + "\n\n")

print(f"\nConcluído com sucesso! Foram processadas {num_linha} linhas.")
print(f"Abre o ficheiro '{ficheiro_saida}' para ver os alvos perfeitos logo no início!")