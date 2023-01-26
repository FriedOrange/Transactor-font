@echo off

fontforge -script source\generate.py

rem Generate intermediate UFO sources
for %%f in (source\temp\Quantum*.sfd) do (
	sfd2ufo %%f source\%%~nf.ufo
	rem copy features.fea %%~nf.ufo\features.fea
)