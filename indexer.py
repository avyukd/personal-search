from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh import index
import os, os.path
import textract

TEST_PATH = r"C:\Users\avyuk\OneDrive\Desktop\LD"

schema = Schema(filename=ID(stored=True),
                filepath=ID(stored=True),
                content=TEXT(analyzer=StemmingAnalyzer()),
                tags=KEYWORD(commas=True, scorable=True))

sample_files = os.listdir(TEST_PATH)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    ix = index.create_in("indexdir", schema)

ix = index.open_dir("indexdir")

writer = ix.writer()

for path, directories, files in os.walk(TEST_PATH):
    for file in files:
        if ".pdf" in file or ".docx" in file or ".doc" in file:
            try:
                filepath = os.path.join(TEST_PATH, file)

                text = textract.process(filepath).decode("utf-8")
                writer.add_document(filename=file,
                                    filepath=filepath,
                                    content=text)
            except UnicodeDecodeError:
                print("UnicodeDecodeError. Moving to next file.")
            except Exception as e:
                print("Unknown error"+str(e))
writer.commit()


