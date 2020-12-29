# -*- coding: utf-8 -*-
# Python 3.8.0
"""
XLF Translator for Across Healthcare inc

@author Justin Smith and Michael Jiles
@version 2.0
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
openingTargetTag = '<target>'
closingTargetTag = '</target>'

ampersandCode = '&amp;'
apostrapheCode = '&apos;'
quoteCode = '&quot;'


'''
 Get the language(s) and selected_filename from the user as input
'''
def get_language_and_filename():
    '''
    Gets the language code(s) to be translated to, and the selected_filename for translation
    '''
    Tk().withdraw()
    selected_filename = askopenfilename()
    print("File selected: " + selected_filename + "\n")

    print("Please see our Wiki page for the language code(s) you may enter (https://github.com/jsmit124/i18n-xlf-file-translator)\n")
    targetLanguageString = input("Enter target language code(s) separated by commas (ex. 'it,fr,es'): ")
    targetLanguages = targetLanguageString.split(',')
    return targetLanguages, selected_filename


'''
 Returns a list of translated phrases for the current line

 TODO: Find how to translate text that spans more than one line**
 TODO: Consider how to prevent multiple constructions of the translator object
'''
def getTranslatedPhrases(phrases, targetLanguage):
    translator = google_translator()
    translatedPhrases = []

    for phrase in phrases:
        result = ''
        if ampersandCode in phrase:
            phrase = phrase.replace(ampersandCode, 'and')
            
        if apostrapheCode in phrase:
            phrase = phrase.replace(apostrapheCode, '\'')
            
        if quoteCode in phrase:
            phrase = phrase.replace(quoteCode, '\"')
    
        if len(phrase.strip()) > 0:
            result = translator.translate(phrase, lang_src='en', lang_tgt=targetLanguage)
            result = result[:-1]
    
        if isinstance(result, list):
            result = result[0]

        translatedPhrases.append(result)
    return translatedPhrases


'''
 Writes the translated phrases to the target file(s)
 
 TODO: phrase.strip()::line80 results in an issue with START tag
'''
def writeTranslatedPhrases(targetPhrase, translatedPhrases, phrases, file):
    for index, phrase in enumerate(phrases):
        targetPhrase = targetPhrase.replace(phrase.strip(), translatedPhrases[index])

    file.write(targetPhrase)
    

'''
 Builds a dictionary from an existing translation file(s), if one exists
'''
def buildExistingTranslationFile(oldLines):
    targetDictionary = {}
    sourceSection = ''
    targetSection = ''
    y = 0
    
    while y < (len(oldLines)):
        line = oldLines[y]

        if openingSourceTag in line:
            sourceSection = line

            while closingSourceTag not in sourceSection:
                y = y + 1
                sourceSection = sourceSection + oldLines[y]
        
        elif openingTargetTag in line:
            targetSection = line

            while closingTargetTag not in targetSection:
                y = y + 1
                targetSection = targetSection + oldLines[y]
            targetDictionary.update({ sourceSection : targetSection })

        y = y + 1

    print("Dictionary Made")
    
    return targetDictionary


'''
 Translates the base file into the target language
'''
def translateFile(targetLanguage, translatedFileName, base_file_lines):

    # Read from base file
    targetDictionary = {}
    file_exists = os.path.isfile(translatedFileName)
    if (file_exists):
        translatedFile = open(translatedFileName, 'r', encoding='utf8')
        oldLines = translatedFile.readlines()
        targetDictionary = buildExistingTranslationFile(oldLines)

    newFile = open(translatedFileName, 'w', encoding='utf8')
    print("Translating to " + targetLanguage + "..")

    x = 0

    while x < (len(base_file_lines)):
        line = base_file_lines[x]
        phraseToTranslate = ''

        if openingSourceTag in line:
            phraseToTranslate = line[line.find(openingSourceTag) + 8 : line.rfind(closingSourceTag)]
            copyPhrase = line

            while closingSourceTag not in copyPhrase:
                x = x + 1
                phraseToTranslate = phraseToTranslate + base_file_lines[x]
                copyPhrase = copyPhrase + base_file_lines[x]
            if copyPhrase in targetDictionary:
                newFile.write(copyPhrase)
                newFile.write(targetDictionary.get(copyPhrase))
                x = x + 1
            else:
                phrases = []

                if '<' in phraseToTranslate:
                    phrases = re.split(r'<.*>|\n', phraseToTranslate)
                else:
                    phrases.append(phraseToTranslate)
                
                translatedPhrases = getTranslatedPhrases(phrases, targetLanguage)
                newFile.write(copyPhrase)
                targetPhrase = copyPhrase.replace('source', 'target')
                writeTranslatedPhrases(targetPhrase, translatedPhrases, phrases, newFile)
                
                x = x + 1
        else:
            newFile.writelines(line)
            x = x + 1

    newFile.close()


'''
 Initial entry point for the program
'''
def main():
    # Take user input
    targetLanguages, base_file_path = get_language_and_filename()
    
    '''
    - - - - - - - - - - - - - IO - - - - - - - - - - - - -
    '''
    # Build translated file path
    base_file_name = os.path.basename(base_file_path)
    splitBase = os.path.splitext(base_file_name)[0]
    baseFile = open(base_file_path, 'r', encoding='utf8')
    base_file_lines = baseFile.readlines()

    '''
    - - - - - - - - - - - - - Translation - - - - - - - - - - - - -
    '''
    for targetLanguage in targetLanguages:
        translatedFileName = re.sub(splitBase, splitBase + "." + targetLanguage, base_file_path)
        translateFile(targetLanguage, translatedFileName, base_file_lines)


    baseFile.close()
    print("Done!")


'''
- - - - - - - - - - - - - Startup - - - - - - - - - - - - -
'''
if __name__ == "__main__":
    main()
