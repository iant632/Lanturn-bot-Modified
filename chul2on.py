fileOut = open("com.bin", "r+b")
fileOut.seek(1)
fileOut.write(bytes([1]))
fileOut.close()