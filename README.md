# SvenskaScraper
A script to quickly scrap translations from Lexin and SAOL dictionaries

### Description
This script searches for the translation of a list of words in the Lexin and SAOL dictionaries through [Språkbankens API](https://spraakbanken.gu.se/).
Given a list of words in an excel spreadsheet, the script will search for their translation, 
as well as gather information regarding the word type, inflections, grammatical construction and an exemplifying sentence for each of the words.
From the excel sheet is easier to export the data to other services like [Quizlet](https://quizlet.com) to learn it properly, just by copy-pasting.
The script optionally generates a set of exercises with the exemplifying sentences, with empty slots to be filled in with the appropiate word (see pictures below).
These can be exported to Quizlet aswell to test yourself and practice.

**Required dependencies**: [openpyxl](http://openpyxl.readthedocs.io/en/stable/) package for python 2.7   
**Available languages**: english `lang = eng`, spanish `lang = spa`, russian `lang = rus`, albanian `lang = sqi`, bosnian `lang = bos`, finnish `lang = fin`, 
greek `lang = ell`, croatian `lang = hrv`, kurdish (north)  `lang = kur_north`, kurdish (south) `lang = kur_south`, persian `lang = fas`, 
serbian `lang = srp`, serbian (cyrillic) `lang = srp_cyrillic`, somali `lang = som`, turkish `lang = tur`.

### Optional configuration
**create_exercises**: `True/False` parameter used to determine if exercises are going to be created. The set of sentences are written in a new worksheet inside the current excel workbook

**Strict**: parameter used to tune the results retrieved from Lexin API
* `strict = True`  => only finds translations where the base form is exactly equal to the searched word.
* `strict = False` => includes also in the results inflections of the word.
   
*Example*: when searching for word "låg". 

  If `strict = False` => the translations "lie" (ligga, låg, legat) and low (låg, lågt, låga) are returned.   
  If `strict = True`  => only "low" is returned since it is the only one that matches the base form (låg) of the query.   

### Images
#### Data scraping
![Example](https://github.com/juanluisrto/SvenskaScraper/blob/master/img/example.PNG)

#### Exercises
![Example](https://github.com/juanluisrto/SvenskaScraper/blob/master/img/exercise.PNG)
