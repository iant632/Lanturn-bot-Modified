fileOut = open("com.bin", "r+b")
fileOut.seek(0)
fileOut.write(bytes([1]))
fileOut.close()