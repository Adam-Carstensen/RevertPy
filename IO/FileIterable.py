import os
import fnmatch
from collections import deque

class FileIterable():
  """Breadth first search of the file system starting at the rootPath and optionally navigating subFolders.
  This iterable will return each file matching the file filter."""

  def __init__(self, rootPath, fileFilter = "*.*", includeSubFolders = True) -> None:
    self.rootPath = rootPath
    self.fileFilter = fileFilter
    self.includeSubFolders = includeSubFolders
   
    self.directories = deque()
    self.files = deque()
    self.__poppedFiles = []

    self.populateDirectoryStack(rootPath)


  def populateDirectoryStack(self, path):
    self.populateFileStack(path)

    self.directories.append(path)

    if self.includeSubFolders:
      for item in os.listdir(path):
        itemPath = os.path.join(path, item)
        if os.path.isdir(itemPath):
          self.populateDirectoryStack(itemPath)

  def populateFileStack(self, path):
    directoryFiles = fnmatch.filter(os.listdir(path), self.fileFilter)
    for file in directoryFiles:
      self.files.append(os.path.join(path, file))

  def __iter__(self):
    return self

  def __next__(self):
    try:
      if len(self.files) == 0 or self.files[0] == None:
        self.reset()
        raise StopIteration
      
      currentFile = self.files.popleft()
      self.__poppedFiles.append(currentFile)
      return currentFile

    except BaseException as ex:
      print(ex)
      raise StopIteration
      
  def reset(self):
    if any(self.__poppedFiles):
      for poppedFile in self.__poppedFiles:
        self.files.appendleft(poppedFile)
      self.__poppedFiles.clear()
    else:
      self.populateDirectoryStack(self.rootPath)





