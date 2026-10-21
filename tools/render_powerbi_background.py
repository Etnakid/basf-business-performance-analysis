"""Render decorative report background (no financial values or chart marks).

Requires Pillow and Inkscape. Uses the original BASF logo SVG unchanged.
Run from any directory: python tools/render_powerbi_background.py
"""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

BASE = Path(__file__).resolve().parents[1] / 'powerbi/BASF'
ASSETS = BASE / 'assets'
OUT = BASE / 'BASF.Report/StaticResources/RegisteredResources'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1600, 900
S = 2
canvas = Image.new('RGB', (W*S, H*S), '#06120C')

# Original BASF photos, touching top/right edges, faded into the canvas.
for filename, x, width, opacity in [('night.jpg', 890, 710, .85), ('day.jpg', 720, 600, .55)]:
    photo = ImageOps.fit(Image.open(ASSETS / filename).convert('RGB'), (width*S, 235*S))
    mask = Image.new('L', photo.size)
    pix = mask.load()
    for yy in range(photo.height):
        fy = min(1, max(0, (235*S-yy)/(130*S)))
        for xx in range(photo.width):
            fx = min(1, xx/(width*S*.6))
            if filename == 'day.jpg': fx *= min(1, (width*S-xx)/(width*S*.4))
            pix[xx, yy] = int(255 * fx * fy * opacity)
    canvas.paste(photo, (x*S, 0), mask)

draw = ImageDraw.Draw(canvas)

def text(x, y, value, size=12, fill='#B8CCB7', strong=False):
    face = 'SpaceGrotesk-Bold.ttf' if strong else 'SpaceGrotesk-Medium.ttf'
    draw.text((x*S, y*S), value, font=ImageFont.truetype(str(ASSETS/face), size*S), fill=fill)

def panel(x, y, w, h, radius=14):
    draw.rounded_rectangle((x*S, y*S, (x+w)*S, (y+h)*S), radius=radius*S, fill='#0B1C13', outline='#29452E', width=S)

with tempfile.TemporaryDirectory() as temp:
    p = Path(temp)/'logo.png'
    subprocess.run(['inkscape', str(ASSETS/'basf-official-logo.svg'),
                    '--export-type=png', '--export-width=242', '--export-filename='+str(p)], check=True, capture_output=True)
    logo = Image.open(p).convert('RGBA')
    canvas.paste(logo, (32*S, 24*S), logo)
draw.line((176*S, 33*S, 176*S, 62*S), fill='#71915A', width=S)
text(198, 39, 'F I N A N C I A L   P E R S P E C T I V E S', 12, '#A0E95C')
text(32, 90, 'Business Performance', 42, '#F1FAE9')
font = ImageFont.truetype(str(ASSETS/'SpaceGrotesk-Medium.ttf'), 42*S)
advance = draw.textlength('Business Performance ', font=font)/S
text(32+advance, 90, 'Analysis', 42, '#A5E96A')
text(33, 151, '2016–2025 · A closer look at the industry shaping my city.', 13)
text(1330, 27, 'L U D W I G S H A F E N', 11, '#EAF5E2')
text(1370, 117, 'REPORT YEAR', 12, '#EAF5E2')
draw.line((32*S, 195*S, 1568*S, 195*S), fill='#34572D', width=S)

labels = [('Sales', ''), ('EBITDA', ''), ('EBIT', ''), ('Net income', ''),
          ('EBITDA margin', 'before special items'), ('Operating', 'cash flow'),
          ('Free cash flow', ''), ('Investments', 'asset additions'), ('ROCE', '')]
for i, (a,b) in enumerate(labels):
    x = 32+i*172
    # Rounded surfaces with subtle light rim and base glow.
    panel(x, 209, 160, 143, 20)
    gradient = Image.new('RGB', (158*S, 141*S))
    gd = ImageDraw.Draw(gradient)
    for j in range(141*S):
        t = (1-j/(141*S))**2
        shade = (int(11+18*t), int(28+29*t), int(18+16*t))
        gd.line((0,j,158*S,j),fill=shade)
    mask = Image.new('L', gradient.size)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,158*S-1,141*S-1),radius=19*S,fill=255)
    canvas.paste(gradient, ((x+1)*S,210*S), mask)
    text(x+12, 219, a, 17, '#EAF5E2', strong=True)
    if b:
        text(x+12, 242, b, 15 if i == 5 else 11, '#B8CCB7', strong=(i == 5))
    text(x+12, 303, '%' if i in (4,8) else 'million EUR', 11, '#A4B9AA')
    draw.line(((x+64)*S,351*S,(x+96)*S,351*S),fill='#78AC52',width=2*S)

for x,y,w,h,title in [(32,370,826,240,'Sales trajectory'),(872,370,696,240,'Profitability'),
                       (32,624,826,222,'Cash generation'),(872,624,696,222,'Investments / CapEx')]:
    panel(x,y,w,h)
    text(x+15,y+12,title,16,'#EAF5E2')
    text(x+w-111,y+16,'million EUR',10,'#A4B9AA')

draw.line((32*S, 859*S, 1568*S, 859*S), fill='#28442D', width=S)
text(32, 864, 'Source: BASF Report 2025 · Published figures include restatements; comparisons are not like-for-like.', 12, '#B8CCB7')
text(32, 882, 'Margin: before special items. CapEx: asset additions, not cash payments. Photos and logo © BASF.', 12, '#B8CCB7')
text(1230, 872, 'INDEPENDENT PORTFOLIO PROJECT', 12, '#A6D18A')
canvas.save(OUT/'background.png', optimize=True)
print(OUT/'background.png')
