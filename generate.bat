@echo off

fontforge -script source\generate.py

rem Generate intermediate UFO sources
for %%f in (source\temp\Quantum*.sfd) do (
	sfd2ufo %%f source\%%~nf.ufo
)

copy source\features.fea source\Quantum-Regular.ufo\features.fea
copy source\features.fea source\Quantum-Bold.ufo\features.fea
copy source\features.fea source\QuantumPrint-Regular.ufo\features.fea
copy source\features.fea source\QuantumPrint-Bold.ufo\features.fea
copy source\features.fea source\QuantumRaster-Regular.ufo\features.fea
copy source\features.fea source\QuantumRaster-Bold.ufo\features.fea
copy source\features.fea source\QuantumScreen-Regular.ufo\features.fea
copy source\features.fea source\QuantumScreen-Bold.ufo\features.fea
copy source\features.fea source\QuantumVideo-Regular.ufo\features.fea