import os

def converter_para_retroarch_cht_real():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    ficheiro_entrada = os.path.join(pasta_atual, "action_replay_codes.txt")
    ficheiro_saida = input("Final File Name or Path: ").strip()
    nome_limpo = os.path.splitext(os.path.basename(ficheiro_saida))[0]

    if not os.path.exists(ficheiro_entrada):
        print("[❌] Erro: O ficheiro 'action_replay_codes.txt' não foi encontrado.")
        return

    print("📖 Lendo os códigos Action Replay originais...")
    with open(ficheiro_entrada, "r") as f:
        # Filtra linhas em branco e remove espaços extras
        codigos_brutos = [linha.strip() for list_item in f if (linha := list_item.strip())]

    total_codigos = len(codigos_brutos)
    print(f"⚡ Foram detectados {total_codigos} códigos para conversão.")

    print("✍️ Estruturando arquivo .cht na sintaxe nativa do RetroArch...")
    
    conteudo_cht = []
    # O cabeçalho 'cheats' DEVE conter o número exato de comandos independentes
    conteudo_cht.append(f"cheats = {total_codigos}\n")

    # Mapeia cada linha do TXT original em um bloco estruturado sequencial
    for idx, comando in enumerate(codigos_brutos):
        # Cada comando precisa de descrição, código e ativação individuais
        conteudo_cht.append(f'cheat{idx}_desc = "{nome_limpo}_{idx}"')
        conteudo_cht.append(f'cheat{idx}_code = "{comando}"')
        conteudo_cht.append(f'cheat{idx}_enable = true') # Já inicia injetando na VRAM

    with open(ficheiro_saida, "w", encoding="utf-8") as f:
        # Grava os blocos separados corretamente por quebras de linha reais
        f.write("\n".join(conteudo_cht))

    print(f"\n[🎯] CONVERSÃO CONCLUÍDA COM SUCESSO!")
    print(f"💾 Ficheiro formatado pronto: saturn_sprite_mod.cht")
    print(f"Nota: Geradas {total_codigos} entradas estruturadas sequencialmente de cheat0 a cheat{total_codigos-1}.")

if __name__ == "__main__":
    converter_para_retroarch_cht_real()