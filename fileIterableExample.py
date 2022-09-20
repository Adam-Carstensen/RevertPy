from IO.FileIterable import FileIterable

path = "C:\directory"
fileIterable = FileIterable(path, fileFilter="*.dat")
for file in fileIterable:
  print(file)

