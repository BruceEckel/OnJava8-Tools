copy %~dp0output_duet.py C:\Users\Bruce\Documents\Git\on-java\ExtractedExamples /y
copy %~dp0verify_output.py C:\Users\Bruce\Documents\Git\on-java\ExtractedExamples /y
del update_output.bat
del validate_failures.txt
del strategies.txt
py -3 C:\Users\Bruce\Documents\Git\on-java\ExtractedExamples\verify_output.py
