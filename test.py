import os 
TEST_PATH = r"C:\Users\avyuk\OneDrive\Desktop\LD"
for path, directories, files in os.walk(TEST_PATH):
    for file in files:
        print(os.path.join(path, file))
