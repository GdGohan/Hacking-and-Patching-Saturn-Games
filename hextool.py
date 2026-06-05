import os
import subprocess
import sys

def sum_hexadecimal():
    print("\n--- SUM HEXADECIMAL VALUES ---")
    hex1 = input("Enter the first Hex value (e.g., 30): ").strip()
    hex2 = input("Enter the second Hex value (e.g., 1B0): ").strip()
    
    try:
        num1 = int(hex1, 16)
        num2 = int(hex2, 16)
        result_decimal = num1 + num2
        result_hex = hex(result_decimal).split('x')[1].upper()
        
        print(f"\nResult in Decimal: {result_decimal}")
        print(f"Result in Hexadecimal: 0x{result_hex}")
    except ValueError:
        print("\n[ERROR] Invalid hexadecimal values (use 0-9, A-F).")

def decimal_to_hexadecimal():
    print("\n--- CONVERT DECIMAL TO HEX ---")
    decimal_str = input("Enter the decimal number (e.g., 1871): ").strip()
    
    try:
        num_decimal = int(decimal_str)
        result_hex = hex(num_decimal).split('x')[1].upper()
        print(f"\nThe number {num_decimal} in Hexadecimal is: 0x{result_hex}")
    except ValueError:
        print("\n[ERROR] Invalid decimal number.")

def calculate_byte_size():
    print("\n--- CALCULATE SIZE IN BYTES ---")
    try:
        width = int(input("Enter the graphic WIDTH (in pixels): ").strip())
        height = int(input("Enter the graphic HEIGHT (in pixels): ").strip())
        
        print("\nChoose color format (BPP):")
        print("1. 4 BPP (16 colors - Common in Sprites/Buttons)")
        print("2. 15 BPP (High Color - Common in Backgrounds/Screens)")
        bpp_option = input("Choose option (1-2): ").strip()
        
        total_pixels = width * height
        
        if bpp_option == "1":
            size_bytes = total_pixels // 2
            bpp_name = "4 BPP"
        elif bpp_option == "2":
            size_bytes = total_pixels * 2
            bpp_name = "15 BPP"
        else:
            print("\n[ERROR] Invalid BPP option!")
            return

        size_hex = hex(size_bytes).split('x')[1].upper()
        
        print(f"\n=" + "-"*35)
        print(f" RESULT FOR: {width}x{height} ({bpp_name})")
        print(f"=" + "-"*35)
        print(f"Total Pixels: {total_pixels} px")
        print(f"Size in Decimal: {size_bytes} bytes")
        print(f"Size in Hexadecimal: 0x{size_hex}")
        print("-" * 37)

    except ValueError:
        print("\n[ERROR] Please enter only integers for width and height.")

def call_individual_script():
    external_script = "hextool_scannerLines.py"
    
    if not os.path.exists(external_script):
        print(f"\n[ERROR]: The file '{external_script}' was not found in this folder!")
        return
        
    print(f"\n[INFO]: Starting the external script '{external_script}' directly...")
    print("-" * 40)
    
    try:
        # Uses the current Python interpreter to run the script cleanly
        subprocess.run([sys.executable, external_script])
    except Exception as e:
        print(f"\n[ERROR] Failed to execute the external script: {e}")

def menu():
    while True:
        print("\n" + "="*40)
        print("     CALCULATOR & ROMHACKING SCANNER    ")
        print("="*40)
        print("1. Sum two Hexadecimal values")
        print("2. Convert Decimal to Hexadecimal")
        print("3. Calculate Size in Bytes (4 BPP / 15 BPP)")
        print("4. Run Quick Scan (Call external script)")
        print("5. Exit")
        print("-" * 40)
        
        option = input("Choose an option (1-5): ").strip()
        
        if option == "1":
            sum_hexadecimal()
        elif option == "2":
            decimal_to_hexadecimal()
        elif option == "3":
            calculate_byte_size()
        elif option == "4":
            call_individual_script()
        elif option == "5":
            print("\nClosing the program. Good luck with the translation!")
            break
        else:
            print("\nInvalid option! Try again.")

if __name__ == "__main__":
    menu()
