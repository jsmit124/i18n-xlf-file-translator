# -*- coding: utf-8 -*-
# Python 3.8.0
"""
Translator

@author Justin Smith
@version 1.0

"""


'''
- - - - - - - - - - - - - Imports - - - - - - - - - - - - -
'''
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from google_trans_new import google_translator
import re


'''
- - - - - - - - - - - - - Global Variables - - - - - - - - - - - - -
'''
openingSourceTag = '<source>'
closingSourceTag = '</source>'

ampersandCode = '&amp;'
apostrapheCode = '&apos;'


'''
- - - - - - - - - - - - - User Input - - - - - - - - - - - - -
'''
Tk().withdraw() 
filename = askopenfilename() 
print("File selected: " + filename + "\n")

print("Please see our Wiki page for the language codes you may enter (https://github.com/jsmit124/i18n-xlf-file-translator)\n")
targetLanguage = input("Please enter the language code for the target language (ex. 'en', 'es', 'fr', etc): ")


'''
- - - - - - - - - - - - - IO - - - - - - - - - - - - -
'''
base = os.path.basename(filename)
splitBase = os.path.splitext(base)[0]
translatedFileName = re.sub(splitBase, splitBase + "." + targetLanguage, filename)

baseFile = open(filename, 'r')
newFile = open(translatedFileName, 'w')

lines = baseFile.readlines()

temp = ''
translator = google_translator()


'''
- - - - - - - - - - - - - Main - - - - - - - - - - - - -
'''
x = 0

while x < (len(lines)):
    line = lines[x]
    phraseToTranslate = ''
    
    if openingSourceTag in line:
        phraseToTranslate = line[line.find(openingSourceTag) + 8 : line.rfind(closingSourceTag)]
        copyPhrase = line
        
        while closingSourceTag not in copyPhrase:
            x = x + 1
            phraseToTranslate = phraseToTranslate + lines[x]
            copyPhrase = copyPhrase + lines[x]
        
        if '<' in phraseToTranslate:
            phraseToTranslate = re.sub(r'<.+?>', '', phraseToTranslate)
        
        result = ''
        
        if ampersandCode in phraseToTranslate:
            re.sub(ampersandCode, 'and', phraseToTranslate)
            
        if apostrapheCode in phraseToTranslate:
            re.sub(apostrapheCode, "'", phraseToTranslate)
        
        if len(phraseToTranslate.strip()) > 0:
            result = translator.translate(phraseToTranslate, lang_src='en', lang_tgt=targetLanguage)
        
        if isinstance(result, list):
            result = result[0]
            
        if '  ' in result:
            result = re.sub('  ', '\n\t', result)
            
        if (len(result.strip()) > 0):
            newFile.write(copyPhrase)
            
            targetPhrase = copyPhrase.replace('source', 'target')
            targetPhrase = targetPhrase.replace(phraseToTranslate.strip(), result.strip())
            
            newFile.write(targetPhrase)
        else:
            newFile.write(copyPhrase)
            newFile.write('\t\t<target></target>// TODO\n')
        x = x + 1
    else:
        newFile.writelines(line)
        x = x + 1
        
        
'''
- - - - - - - - - - - - - Cleanup - - - - - - - - - - - - -
'''
baseFile.close()
newFile.close()
