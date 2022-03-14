import json
import os
import glob
keywordList = []

path = 'build/contracts/'
outputDir = 'abi/'
for filename in glob.glob(os.path.join(path, '*.json')):
  print(f'Read from      {filename}')
  with open(filename) as currentFile:
    abi = json.load(currentFile)["abi"]
    save_path = os.path.join(outputDir, filename.split('/')[-1])
    with open(save_path, 'w') as outfile:
      json.dump(abi, outfile)
      print(f'Save ABI into: {save_path}\n')
