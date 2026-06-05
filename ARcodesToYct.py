import os
import struct

def converter_para_yaba_binario_pasta():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    ficheiro_entrada = os.path.join(pasta_atual, "action_replay_codes.txt")

    if not os.path.exists(ficheiro_entrada):
        print("[❌] Erro: O ficheiro 'action_replay_codes.txt' não foi encontrado.")
        return

    entrada_usuario = input("Digite o prefixo para os ficheiros (ex: meu_sprite): ").strip()
    
    # Remove extensões caso o usuário tenha digitado por hábito
    prefixo_nome = entrada_usuario.replace(".yct", "").replace(".bin", "").replace(".cht", "")

    # Cria a pasta de destino para os cheats se não existir
    pasta_saida_cheats = os.path.join(pasta_atual, "Yaba_Cheats")
    if not os.path.exists(pasta_saida_cheats):
        os.makedirs(pasta_saida_cheats)

    with open(ficheiro_entrada, "r") as f:
        linhas = [l.strip() for l in f if l.strip()]

    total_linhas = len(linhas)
    print(f"📖 Processando {total_linhas} códigos individualmente para a pasta 'Yaba_Cheats'...")

    contador_sucesso = 0

    # Itera por cada linha gerando um ficheiro YCHT único por pixel
    for idx, linha in enumerate(linhas):
        partes = linha.split()
        if len(partes) != 2:
            continue
            
        codigo_ar, valor_hex = partes[0], partes[1]

        # Mapeamento do tipo binário
        tipo_yaba = 3 if codigo_ar.startswith('1') else 2

        # Conversão de valores hex para inteiros purificados
        endereco_int = int(codigo_ar[1:], 16)
        valor_int = int(valor_hex, 16)

        # BUFFER BINÁRIO EXCLUSIVO DO CHEAT ATUAL
        buffer_binario = bytearray()

        # Cabeçalho estrutural YCHT
        buffer_binario.extend(b"YCHT")
        buffer_binario.extend(struct.pack(">I", 1))       # Versão

        # Dados da estrutura revelada
        buffer_binario.extend(struct.pack(">I", tipo_yaba))
        buffer_binario.extend(struct.pack(">I", endereco_int))
        buffer_binario.extend(struct.pack(">I", valor_int))
        buffer_binario.extend(struct.pack(">I", 0x01000000)) # Status ativo
        buffer_binario.extend(struct.pack(">H", 0x0001))     # Alinhamento final

        # Nome individualizado (ex: meu_sprite_0.yct)
        nome_ficheiro_individual = f"{prefixo_nome}_{idx}.yct"
        caminho_arquivo_final = os.path.join(pasta_saida_cheats, nome_ficheiro_individual)

        # Escreve o bytearray no arquivo correspondente
        with open(caminho_arquivo_final, "wb") as f:
            f.write(buffer_binario)
        
        contador_sucesso += 1

    print(f"\n[🎯] PROCESSO CONCLUÍDO COM SUCESSO!")
    print(f"💾 {contador_sucesso} arquivos individuais gerados dentro da pasta:")
    print(f"📁 {os.path.abspath(pasta_saida_cheats)}")

if __name__ == "__main__":
    converter_para_yaba_binario_pasta()