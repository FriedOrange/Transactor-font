@rem build OpenType fonts
@cd source
python %USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\gftools-builder.py config.yaml
@cd ..

@rem generate proof documents
@cd fonts\ttf
set PYTHONUTF8=1
python %USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\gftools-gen-html.py proof -o ..\proof   Transactor-Regular.ttf TransactorInverse-Regular.ttf
@cd ..\..