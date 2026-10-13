"""Generates the demo payment QR codes as SVG (needs: pip install segno). Each encodes a demo page on this site, never a real payment account."""
import segno
BASE="https://ben-sampson.github.io/sampson-family-law/payment-demo.html?method="
for m in ("cashapp","venmo","strike"):
    segno.make(BASE+m,error="m").save(f"img/qr/{m}.svg",scale=8,border=4,dark="#0a2540",light="#ffffff",xmldecl=False,svgns=True,title=f"Demo QR code for {m}: opens a demonstration page")
    print(m,BASE+m)
