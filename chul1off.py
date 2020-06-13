fileOut = open("com.bin", "r+b")
fileOut.seek(0)
fileOut.write(bytes([0]))
fileOut.close()