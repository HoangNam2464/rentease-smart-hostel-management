import os, base64
from PIL import Image, ImageDraw

BRAND_DIR = '../frontend/static/rentease/img/brand'
os.makedirs(BRAND_DIR, exist_ok=True)

with open('icon.png', 'rb') as f:
    icon_b64 = base64.b64encode(f.read()).decode('utf-8')
icon_href = f"data:image/png;base64,{icon_b64}"

def write_svg(filename, width, height, content):
    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&amp;display=swap');
      .font-sans {{ font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif; }}
    </style>
    <filter id="white-tint"><feColorMatrix type="matrix" values="0 0 0 0 1   0 0 0 0 1   0 0 0 0 1   0 0 0 1 0"/></filter>
    <filter id="mono-tint"><feColorMatrix type="matrix" values="0 0 0 0 0.059   0 0 0 0 0.141   0 0 0 0 0.2   0 0 0 1 0"/></filter>
  </defs>
  {content}
</svg>"""
    with open(os.path.join(BRAND_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(svg)

# Notice: I increased width from 80 to 90 because the fixed icon has a slightly wider crop relative to its height.
write_svg('logo-rentease-icon.svg', 100, 100, f'<image href="{icon_href}" x="0" y="0" width="100" height="100" />')

write_svg('logo-rentease-horizontal.svg', 380, 100, f"""
  <image href="{icon_href}" x="0" y="10" width="80" height="80" />
  <text x="92" y="66" class="font-sans" font-size="50" font-weight="800" letter-spacing="-1.5">
    <tspan fill="#0f2433">Rent</tspan><tspan fill="#0f766e">Ease</tspan>
  </text>
""")

write_svg('logo-rentease-primary.svg', 500, 120, f"""
  <image href="{icon_href}" x="0" y="10" width="90" height="90" />
  <text x="104" y="62" class="font-sans" font-size="50" font-weight="800" letter-spacing="-1.5">
    <tspan fill="#0f2433">Rent</tspan><tspan fill="#0f766e">Ease</tspan>
  </text>
  <text x="106" y="88" class="font-sans" font-size="14" font-weight="600" fill="#627386" letter-spacing="0.3">
    Smart Rental Room Management System
  </text>
""")

write_svg('logo-rentease-compact.svg', 200, 200, f"""
  <image href="{icon_href}" x="50" y="10" width="100" height="100" />
  <text x="100" y="150" class="font-sans" font-size="36" font-weight="800" letter-spacing="-1" text-anchor="middle">
    <tspan fill="#0f2433">Rent</tspan><tspan fill="#0f766e">Ease</tspan>
  </text>
""")

write_svg('logo-rentease-white.svg', 380, 100, f"""
  <image href="{icon_href}" x="0" y="10" width="80" height="80" filter="url(#white-tint)" />
  <text x="92" y="66" class="font-sans" font-size="50" font-weight="800" letter-spacing="-1.5" fill="#ffffff">RentEase</text>
""")

write_svg('logo-rentease-mono.svg', 380, 100, f"""
  <image href="{icon_href}" x="0" y="10" width="80" height="80" filter="url(#mono-tint)" />
  <text x="92" y="66" class="font-sans" font-size="50" font-weight="800" letter-spacing="-1.5" fill="#0f2433">RentEase</text>
""")

write_svg('logo-rentease-auth.svg', 360, 140, f"""
  <image href="{icon_href}" x="130" y="0" width="100" height="100" />
  <text x="180" y="130" class="font-sans" font-size="42" font-weight="800" letter-spacing="-1" text-anchor="middle">
    <tspan fill="#0f2433">Rent</tspan><tspan fill="#0f766e">Ease</tspan>
  </text>
""")

print("SVG Logos Regenerated!")
