# -*- coding: utf-8 -*-
import re, urllib2, json, sys, openpyxl as px

reload(sys)
sys.setdefaultencoding('utf8')

# Configuration variables
path = ""
file_name = "scraper.xlsx"
sheet_name = "scraper"  # sheet where you have your words
lang = "spa"  # Language code used to search translations
create_exercises = True
strict = False

wb = px.load_workbook(path + file_name)
ws = wb.get_sheet_by_name(sheet_name)
terms = []
sentences = []


# Simple class used as a data structure
class Term:
    def __init__(self, swedish, row):
        self.swedish = swedish
        self.translation = []
        self.construction = []
        self.inflection = []
        self.word_type = []
        self.example = None
        self.row = row

    def write_data(self):
        global wb, ws
        i = self.row
        ws["B" + str(i)] = "; ".join(self.translation)
        ws["C" + str(i)] = "; ".join(self.word_type)
        ws["D" + str(i)] = "; ".join(self.construction)
        ws["E" + str(i)] = "; ".join(self.inflection)
        ws["F" + str(i)] = self.example

        try:
            wb.save(path + file_name)
        except IOError:
            print "Close your excel file " + file_name + "!!!"

    # calls språkbanken's api for the exact term in the lexin dictionary to retrieve translation, construction, word type and inflection.
    def lexin(self):
        if strict:
            operator = "baseformC"
        else:
            operator = "wfC"
        url = "https://ws.spraakbanken.gu.se/ws/karp/v4/query?q=extended||and|" + operator + "|equals|" \
              + self.swedish.replace(" ", "%20") + "|&resource=lexin"
        # baseformC = exactly baseform (ex ställa); wfC = any wordform (ex ställer, ställt)
        # for more operators => https://ws.spraakbanken.gu.se/ws/karp/v4/modeinfo/karp
        raw_json = urllib2.urlopen(url)
        parsed_json = json.load(raw_json)
        results = parsed_json["hits"]["hits"]
        if not results:  # if no results are found skip
            return
        for result in results:
            # retrieves inflections of the searched word
            try:
                self.inflection.insert(0, result["_source"]["FormRepresentations"][0]["baseform"])
                for inflection in results[0]["_source"]["WordForms"]:
                    if not inflection["writtenForm"] in self.inflection:
                        self.inflection.append(inflection["writtenForm"])
            except:
                print "Inflections weren't found"
            # retrieves translations of the searched word
            translations = result["_source"]["FormRepresentations"]
            if (strict and translations[0]["baseform"] != self.swedish) or \
            (strict == False and self.swedish not in self.inflection):
                self.inflection = []
                continue
            for t in translations:
                if t["lang"] == "swe" and not t["nativeOfSpeech"] in self.word_type:
                    self.word_type.append(t["nativeOfSpeech"])
                if t["lang"] == lang and not t["baseform"] in self.translation:
                    self.translation.append(t["baseform"])
            try:
                grammar = result["_source"]["Sense"][0]["gram"]
                if isinstance(grammar, list):
                    self.construction.append("; ".join(grammar))
                else:
                    self.construction.append(grammar)
            except:
                print "No grammar found for term " + self.swedish


    # retrieves an example sentence from Svenska Akademins Ordlista for the given word.
    def saol(self):
        word = self.swedish.replace(" ", "%20")
        url = "https://svenska.se/so/?sok=" + word
        html = urllib2.urlopen(url).read()
        examples = re.findall(r'<span class="syntex">(.*?)</span>', html)
        # splits the sentences to calculate the one with most words.
        broken = []
        for s in examples:
            if create_exercises:
                sentences.append([self.inflection, s.replace('-', '')])
            broken.append(s.split())
        if broken:
            pos = broken.index(max(broken, key=len))
            self.example = examples[pos].replace('-', '')


def generate_questions():
    global wb
    questions, solutions, words = [], [], []
    for tuple in sentences:  # tuple = [[inflections], sentence]
        inflections = tuple[0]
        sentence = tuple[1]
        if sentence.count(" ") < 2:  # if the sentence has less than 3 words => skip
            continue
        for inf in inflections:
            if inf.find(" ") != -1:  # if inflection is compound (ex äta upp) search within the string
                pos = sentence.find(inf)
                if pos != -1:
                    words.append(inf)
                    solutions.append(sentence)
                    questions.append(sentence.replace(inf, "_____").encode('utf-8'))
                    break
            else:  # if inflection is simple (ex ätit) split and search within elements
                split_sentence = tuple[1].split()
                if inf in split_sentence:
                    index = split_sentence.index(inf)
                    split_sentence.insert(index, "_____")
                    split_sentence.remove(inf)
                    words.append(inf)
                    questions.append(" ".join(split_sentence))
                    solutions.append(tuple[1])
                    break

    # remove possible duplicates
    for sentence in questions:
        n = questions.count(sentence)
        for i in range(0, n - 1):
            index = questions.index(sentence)
            solutions.pop(index)
            questions.pop(index)
            words.pop(index)

    exercise_sheet = wb.create_sheet("exercises", 2)
    exercise_sheet.column_dimensions['B'].width = 70
    exercise_sheet.column_dimensions['C'].width = 70
    for i in range(len(questions)):
        exercise_sheet['A' + str(i + 1)] = words[i]
        exercise_sheet['B' + str(i + 1)] = questions[i]
        exercise_sheet['C' + str(i + 1)] = solutions[i]
    try:
        wb.save(path + file_name)
    except IOError:
        print "Close your excel file " + file_name + "!!! Otherwise I can't write stuff on it"


def main():
    global ws
    global terms
    # import words in excel document.
    for i in range(ws.min_row + 1, ws.max_row + 1):
        word = Term(ws["A" + str(i)].value.lower(), i)
        if word.swedish == None:
            break
        terms.append(word)

    # perform queries
    for term in terms:
        print term.swedish
        term.lexin()
        term.saol()
        term.write_data()

    if (create_exercises):
        generate_questions()


if __name__ == "__main__":
    main()
