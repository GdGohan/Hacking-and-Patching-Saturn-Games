import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================

ARQUIVO_ORIGINAL = input("Dumped File Name or Path (ex: SaveMemoryButton.bin): ").strip()
ARQUIVO_EDITADO = input("Edited File Name or Path (ex: EditedSaveMemoryButton.bin): ").strip()

# Endereço da textura encontrado no VDP1
entrada = input("Enter the starting address of the contents found in VDP1's RAM: ").strip()

entrada = entrada.replace("0x", "").replace("0X", "")

BASE_VRAM = int(entrada, 16)

# ============================================================

with open(ARQUIVO_ORIGINAL, "rb") as f:
    original = f.read()

with open(ARQUIVO_EDITADO, "rb") as f:
    editado = f.read()

if len(original) != len(editado):
    raise Exception("Os arquivos possuem tamanhos diferentes!")

codigos = []

i = 0

while i < len(original):

    # Tenta gerar código de 16 bits
    if i + 1 < len(original):

        orig16 = original[i:i+2]
        edit16 = editado[i:i+2]

        if orig16 != edit16:

            endereco = BASE_VRAM + i
            valor = (edit16[0] << 8) | edit16[1]

            codigo = f"1{endereco & 0x0FFFFFF:07X} {valor:04X}"
            codigos.append(codigo)

            i += 2
            continue

    # Caso sobre 1 byte isolado
    if original[i] != editado[i]:

        endereco = BASE_VRAM + i

        codigo = f"3{endereco & 0x0FFFFFF:07X} 00{editado[i]:02X}"
        codigos.append(codigo)

    i += 1

with open("action_replay_codes.txt", "w") as f:
    f.write("\n".join(codigos))

print(f"\nGerados {len(codigos)} códigos.")
print("Arquivo salvo: action_replay_codes.txt")