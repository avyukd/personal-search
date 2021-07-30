import textract
import os
from datetime import datetime
import time


TEXT_EXTENSIONS = ['.txt', '.doc', '.docx', '.pdf', ".rtf"]
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
CODE_EXTENSIONS = ['.py', '.c', '.cpp', '.java', '.js', '.html', '.css', '.go', '.rb', 
                        '.sh', '.sql', '.xml', '.yaml', '.yml']

def extract_info_local(filepath):
    try:
        origin = "local"
        extension = os.path.splitext(filepath)[1].lower()
        type = extension.replace(".", "")
        size = os.path.getsize(filepath)
        date = os.path.getmtime(filepath)
        #turn date into YYYY/MM/DD
        date = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        filename = os.path.basename(filepath)

        if extension in TEXT_EXTENSIONS:
            content = textract.process(filepath).decode('utf-8')
            content = " ".join(content.split())
        else:
            content = ""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        return {
            "origin": origin,
            "type": type,
            "size": size,
            "date": date,
            "content": content,
            "filename": filename,
            "timestamp": timestamp
        }
    except Exception as e:
        print("Error: " + str(e))
        return None

