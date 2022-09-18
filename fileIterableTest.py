from RevertPy.IO.FileIterable import FileIterable



path = "C:\Dev\MacroQuest"

fileIterable = FileIterable(path)

for file in fileIterable:
  print(file)




