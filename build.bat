@rem build OpenType fonts
@cd source
python %USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\gftools-builder.py config.yaml
@cd ..

@rem generate proof documents
@cd fonts\ttf
set PYTHONUTF8=1
python %USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\gftools-gen-html.py proof -o ..\proof   Quantum-Regular.ttf  QuantumPrint-Regular.ttf  QuantumRaster-Regular.ttf  QuantumScreen-Regular.ttf  QuantumVideo-Regular.ttf  QuantumPrint#2-Regular.ttf  Quantum-Bold.ttf  QuantumPrint-Bold.ttf  QuantumRaster-Bold.ttf  QuantumScreen-Bold.ttf  QuantumPrint#2-Bold.ttf
@cd ..\..