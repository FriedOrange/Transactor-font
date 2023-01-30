fontforge -script source\step1.py normal "source\\glyphs.pbm" "source\\glyphs.csv" "source\\temp\\step1 main.sfd"
fontforge -script source\step1.py halfstep "source\\glyphs halfstep.pbm" "source\\glyphs halfstep.csv" "source\\temp\\step1 halfstep.sfd"
fontforge -script source\step1.py normal "source\\glyphs bold special.pbm" "source\\glyphs bold special.csv" "source\\temp\\step1 bold.sfd"