import os
import subprocess
import sys

def somar_hexadecimal():
    print("\n--- SOMAR HEXADECIMAIS ---")
    hex1 = input("Digite o primeiro valor Hex (ex: 30): ").strip()
    hex2 = input("Digite o segundo valor Hex (ex: 1B0): ").strip()
    
    try:
        num1 = int(hex1, 16)
        num2 = int(hex2, 16)
        resultado_decimal = num1 + num2
        resultado_hex = hex(resultado_decimal).split('x')[1].upper()
        
        print(f"\nResultado em Decimal: {resultado_decimal}")
        print(f"Resultado em Hexadecimal: 0x{resultado_hex}")
    except ValueError:
        print("\n[ERRO] Valores hexadecimais inválidos (use 0-9, A-F).")

def decimal_para_hexadecimal():
    print("\n--- CONVERTER DECIMAL PARA HEX ---")
    decimal_str = input("Digite o número decimal (ex: 1871): ").strip()
    
    try:
        num_decimal = int(decimal_str)
        resultado_hex = hex(num_decimal).split('x')[1].upper()
        print(f"\nO número {num_decimal} em Hexadecimal é: 0x{resultado_hex}")
    except ValueError:
        print("\n[ERRO] Número decimal inválido.")

def calcular_tamanho_bytes():
    print("\n--- CALCULAR TAMANHO EM BYTES ---")
    try:
        largura = int(input("Digite a LARGURA do gráfico (em pixels): ").strip())
        altura = int(input("Digite a ALTURA do gráfico (em pixels): ").strip())
        
        print("\nEscolha o formato de cor (BPP):")
        print("1. 4 BPP (16 cores - Comum em Sprites/Botões)")
        print("2. 15 BPP (High Color - Comum em Fundos/Telas)")
        bpp_opcao = input("Escolha a opção (1-2): ").strip()
        
        pixels_totais = largura * altura
        
        if bpp_opcao == "1":
            tamanho_bytes = pixels_totais // 2
            bpp_nome = "4 BPP"
        elif bpp_opcao == "2":
            tamanho_bytes = pixels_totais * 2
            bpp_nome = "15 BPP"
        else:
            print("\n[ERRO] Opção de BPP inválida!")
            return

        tamanho_hex = hex(tamanho_bytes).split('x')[1].upper()
        
        print(f"\n=" + "-"*35)
        print(f" RESULTADO PARA: {largura}x{altura} ({bpp_nome})")
        print(f"=" + "-"*35)
        print(f"Total de Pixels: {pixels_totais} px")
        print(f"Tamanho em Decimal: {tamanho_bytes} bytes")
        print(f"Tamanho em Hexadecimal: 0x{tamanho_hex}")
        print("-" * 37)

    except ValueError:
        print("\n[ERRO] Por favor, digite apenas números inteiros para largura e altura.")

def chamar_script_individual():
    script_externo = "hextool_scannerLines.py"  # Nome do seu arquivo individual mais rápido
    
    if not os.path.exists(script_externo):
        print(f"\n[ERRO]: O arquivo '{script_externo}' não foi encontrado nesta pasta!")
        return
        
    print(f"\n[INFO]: Iniciando o '{script_externo}' externo de forma direta...")
    print("-" * 40)
    
    try:
        # Usa o mesmo interpretador Python atual (sys.executable) para rodar o script rápido
        # de forma limpa e isolada do menu atual
        subprocess.run([sys.executable, script_externo])
    except Exception as e:
        print(f"\n[ERRO] Falha ao executar o script externo: {e}")

def menu():
    while True:
        print("\n" + "="*40)
        print("       CALCULADORA & SCANNER ROMHACKING     ")
        print("="*40)
        print("1. Somar dois valores Hexadecimais")
        print("2. Converter Decimal para Hexadecimal")
        print("3. Calcular Tamanho em Bytes (4 BPP / 15 BPP)")
        print("4. Executar Varredura Rápida (Chama Script Separado)")
        print("5. Sair")
        print("-" * 40)
        
        opcao = input("Escolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            somar_hexadecimal()
        elif opcao == "2":
            decimal_para_hexadecimal()
        elif opcao == "3":
            calcular_tamanho_bytes()
        elif opcao == "4":
            chamar_script_individual()
        elif opcao == "5":
            print("\nA fechar o programa. Boa sorte com a tradução!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()