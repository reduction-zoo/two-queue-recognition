"""Vector schematics for the construction and the exceptional positions."""
from pathlib import Path
from html import escape

root=Path(__file__).parent

def text(x,y,s,size=19):return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="serif" font-size="{size}">{escape(s)}</text>'

def line(x,y,u,v,dash=False):return f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="#202020" stroke-width="2"'+(' stroke-dasharray="6 4"' if dash else '')+'/>'

svg=['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="250" viewBox="0 0 800 250">']
for i in range(5):
    x=60+i*140
    svg += [line(350,28,x,85,True),line(350,220,x,145,True)]
svg += ['<path d="M 360 27 C 900 25 900 225 360 221" fill="none" stroke="#202020" stroke-width="2"/>']
for i in range(5):
    x=10+i*140
    svg += [f'<rect x="{x}" y="85" width="100" height="60" rx="4" fill="white" stroke="#202020" stroke-width="2"/>',text(x+50,122,'G'+'₁₂₃₄₅'[i])]
for y,label in [(25,'a'),(222,'b')]:
    svg += [f'<circle cx="350" cy="{y}" r="15" fill="white" stroke="#202020" stroke-width="2"/>',text(350,y+6,label)]
svg += ['</svg>']
(root/'construction.svg').write_text(''.join(svg))

svg=['<svg xmlns="http://www.w3.org/2000/svg" width="700" height="130" viewBox="0 0 700 130">',line(25,55,675,55)]
labels=[('ℓ',45,True),('⋯',110,False),('p',180,True),('a',240,False),('⋯',350,False),('b',460,False),('q',520,True),('⋯',585,False),('r',655,True)]
for label,x,special in labels:
    if label=='⋯':svg += [f'<rect x="{x-13}" y="40" width="26" height="25" fill="white"/>',text(x,59,label)]
    else:
        svg += [f'<circle cx="{x}" cy="55" r="7" fill="'+('#202020' if special else 'white')+'" stroke="#202020" stroke-width="2"/>',text(x,30,label)]
svg += [text(350,108,'Delete ℓ, r and the existing boundary vertices p, q.',18),'</svg>']
(root/'exceptions.svg').write_text(''.join(svg))
