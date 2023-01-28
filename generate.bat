@echo off

fontforge -script source\generate.py

rem Generate intermediate UFO sources
for %%f in (source\temp\Quantum*.sfd) do (
	sfd2ufo %%f source\%%~nf.ufo
)

copy features.fea Quantum-Regular.ufo\features.fea
copy features.fea Quantum-Bold.ufo\features.fea
copy features.fea QuantumPrint-Regular.ufo\features.fea
copy features.fea QuantumPrint-Bold..ufo\features.fea
copy features.fea QuantumRaster-Regular.ufo\features.fea
copy features.fea QuantumRaster-Bold..ufo\features.fea
copy features.fea QuantumScreen-Regular.ufo\features.fea
copy features.fea QuantumScreen-Bold..ufo\features.fea
copy features.fea QuantumVideo-Regular.ufo\features.fea