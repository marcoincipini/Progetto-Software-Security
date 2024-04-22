valore_esadecimale = 0x516d617345637a7134336a4538515743637633647a714d6a757476566d38634b5656625a77776551414841613470

# Converti il valore esadecimale in una stringa di byte
byte_string = bytes.fromhex(hex(valore_esadecimale)[2:])

# Decodifica la stringa di byte in una stringa Unicode
stringa = byte_string.decode('utf-8')

print(stringa)
