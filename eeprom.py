########################################################################
# Autor: Ernesto Lomar
# Fecha de creación: 12/12/2022
# Ultima modificación: 12/12/2024
#
# Script para insertar número de serie y número de versión en tablilla
########################################################################

#Importamos librerías externas
import subprocess
import sys
from time import sleep

try:
    ok = subprocess.run("i2cdetect -y 1", stdout=subprocess.PIPE, shell=True)
    state_num_serie = ""
    state_num_version = ""
    print("\x1b[1;32m"+"Conectándonos con memoria EEPROM...")
    sleep(0.010)

    if ok.returncode == 0:
            print("\x1b[1;32m"+"Conectado a memoria EEPROM...")
            sleep(0.010)
            if sys.argv[1] != "":
                
                num_tablilla = sys.argv[1]
                print("\x1b[1;32m"+"Dato ingresado: ", num_tablilla)
                sleep(0.010)
                numero_de_serie_por_defecto = "Ix20241200"
                i = 0
                n = 0
                print("\x1b[1;32m"+"Procedemos a escribir número de serie en memoria EEPROM...")
                sleep(0.010)

                for c in range(14):
                    i_hex = hex(i)
                    if c <= 9:
                        print("\x1b[1;32m"+"Escribiendo " + numero_de_serie_por_defecto[c] + " en celda: ", str(i_hex))
                        sleep(0.010)
                        valor = subprocess.run(f"i2cset -y 1 0x50 {str(i_hex)} {str(hex(ord(numero_de_serie_por_defecto[c])))}", stdout=subprocess.PIPE, shell=True)
                    else:
                        if c == 12:
                            valor = subprocess.run(f"i2cset -y 1 0x50 {str(i_hex)} 0x00", stdout=subprocess.PIPE, shell=True)
                            break
                        print("\x1b[1;32m"+"Escribiendo " + num_tablilla[n] + " en celda: ", str(i_hex))
                        sleep(0.010)
                        valor = subprocess.run(f"i2cset -y 1 0x50 {str(i_hex)} {str(hex(ord(num_tablilla[n])))}", stdout=subprocess.PIPE, shell=True)
                        n+=1
                    i+=1
                
                print("\x1b[1;32m"+"Número de serie escrito en memoria EEPROM...\n")
                num_version = "vE6.14"
                i = 100
                print("\x1b[1;32m"+"Procedemos a escribir número de versión en memoria EEPROM...")
                sleep(0.010)

                for c in range(7):
                    i_hex = hex(i)
                    if c == 6:
                            valor = subprocess.run(f"i2cset -y 1 0x50 {str(i_hex)} 0x00", stdout=subprocess.PIPE, shell=True)
                            break
                    if c == 3:
                        valor = subprocess.run(f"i2cset -y 1 0x50 {str(i_hex)} 0x2e", stdout=subprocess.PIPE, shell=True)
                        print("\x1b[1;32m"+"Escribiendo " + num_version[c] + " en celda: ", str(i_hex))
                        sleep(0.010)
                        i+=1
                        continue
                    print("\x1b[1;32m"+"Escribiendo " + num_version[c] + " en celda: ", str(i_hex))
                    sleep(0.010)
                    valor = subprocess.run(f"i2cset -y 1 0x50 {str(i_hex)} {str(hex(ord(num_version[c])))}", stdout=subprocess.PIPE, shell=True)
                    i+=1
                print("\x1b[1;32m"+"Número de versión escrito en memoria EEPROM...")
            else:
                print("\x1b[1;33m"+"ERROR: No se ha introducido el número de serie")
                
            print("\n")
            print("\x1b[1;32m"+"Procedemos a leer número de serie y número de versión de la memoria EEPROM...")
            num_serie_hex = []
            i = 0

            while True:
                i_hex = hex(i)
                valor = subprocess.run(f"i2cget -y 1 0x50 {i_hex}", stdout=subprocess.PIPE, shell=True)
                if valor.stdout[2:4].decode() == "00":
                    break
                num_serie_hex.append(valor.stdout[2:4].decode())
                i+=1

            num_serie_utf8 = []
            j = 0

            for i in num_serie_hex:
                byte_arr = bytearray.fromhex(num_serie_hex[j])
                num_serie_utf8.append(byte_arr.decode())
                j+=1
            
            num_version_hex = []
            i = 100

            while True:
                i_hex = hex(i)
                valor = subprocess.run(f"i2cget -y 1 0x50 {i_hex}", stdout=subprocess.PIPE, shell=True)
                if valor.stdout[2:4].decode() == "00":
                    break
                num_version_hex.append(valor.stdout[2:4].decode())
                i+=1

            num_version_utf8 = []
            j = 0

            for i in num_version_hex:
                byte_arr = bytearray.fromhex(num_version_hex[j])
                num_version_utf8.append(byte_arr.decode())
                j+=1
            
            state_num_serie = "".join(num_serie_utf8)
            state_num_version = "".join(num_version_utf8)
            print("\x1b[1;32m"+"Número de serie: ", state_num_serie)
            print("\x1b[1;32m"+"Número de versión: ", state_num_version)
    else:
        print("\x1b[1;33m"+"ERROR: No se ha encontrado la EEPROM")
except Exception as e:
    print("\x1b[1;33m"+"ERROR: ", e)
