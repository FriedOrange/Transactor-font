fontforge -script source\step1.py normal "source\\glyphs.pbm" "source\\glyphs.csv" "source\\temp\\step1 main.sfd"
fontforge -script source\step1.py halfstep "source\\glyphs halfstep.pbm" "source\\glyphs halfstep.csv" "source\\temp\\step1 halfstep.sfd"
fontforge -script source\step1.py normal "source\\glyphs bold aux.pbm" "source\\glyphs bold aux.csv" "source\\temp\\step1 bold.sfd"
fontforge -script source\step1.py video "source\\glyphs hires aux.pbm" "source\\glyphs hires aux.csv" "source\\temp\\step1 video.sfd"