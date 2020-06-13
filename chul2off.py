fileOut = open("com.bin", "r+b")
fileOut.seek(1)
fileOut.write(bytes([0]))
fileOut.close()