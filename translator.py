# -*- coding: utf-8 -*-
"""
Translator

@author Justin Smith
@version 1.0
"""

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from google_trans_new import google_translator
import re

Tk().withdraw() 
filename = askopenfilename() 
print(filename)

targetLanguage = input("Please enter the language code for the target language (ex. 'en', 'es', 'fr', etc): ")

baseFile = open(filename, 'r')
newFile = open('renameMe.xlf', 'w')

lines = baseFile.readlines()

temp = ''
translator = google_translator()

x = 0

while x < (len(lines)):
    line = lines[x]
    phraseToTranslate = ''
    
    if '<source>' in line:
        phraseToTranslate = line[line.find('<source>') + 8 : line.rfind('</source>')]
        copyPhrase = line
        
        while '</source>' not in copyPhrase:
            x = x + 1
            phraseToTranslate = phraseToTranslate + lines[x]
            copyPhrase = copyPhrase + lines[x]
        
        if '<' in phraseToTranslate:
            phraseToTranslate = re.sub(r'<.+?>', '', phraseToTranslate)
        
        result = ''
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
        
baseFile.close()
newFile.close()
