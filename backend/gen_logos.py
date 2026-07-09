import os

BRAND_DIR = '../frontend/static/rentease/img/brand'
os.makedirs(BRAND_DIR, exist_ok=True)

# Pure SVG representation of the Teal/Green gradient house with an "R"
PURE_ICON_SVG = """
  <linearGradient id="tealGreenGrad" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#0f766e"/>
    <stop offset="1" stop-color="#10b981"/>
  </linearGradient>
  <rect x="5" y="5" width="90" height="90" rx="22" fill="url(#tealGreenGrad)" />
  <path d="M 50 22 L 22 50 L 30 50 L 30 78 L 70 78 L 70 50 L 78 50 Z" fill="white" stroke="white" stroke-width="4" stroke-linejoin="round" />
  <text x="50" y="60" font-family="Inter, sans-serif" font-weight="800" font-size="28" fill="#0f766e" text-anchor="middle" dominant-baseline="middle">R</text>
"""

# Horizontal alignment version
HORIZONTAL_ICON_SVG = """
  <g transform="translate(0, 10) scale(0.8)">
""" + PURE_ICON_SVG + """
  </g>
"""

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

# 1. Icon only (100x100)
write_svg('logo-rentease-icon.svg', 100, 100, PURE_ICON_SVG)

# 2. Horizontal (Primary) (380x100)
write_svg('logo-rentease-horizontal.svg', 380, 100, f"""
  {HORIZONTAL_ICON_SVG}
  <text x="90" y="55" class="font-sans" font-size="48" font-weight="800" fill="#0f766e" dominant-baseline="middle">Rent<tspan fill="#1e293b">Ease</tspan></text>
""")

# 3. Horizontal (White text for dark backgrounds)
write_svg('logo-rentease-white.svg', 380, 100, f"""
  {HORIZONTAL_ICON_SVG}
  <text x="90" y="55" class="font-sans" font-size="48" font-weight="800" fill="#ffffff" dominant-baseline="middle">Rent<tspan fill="#e2e8f0">Ease</tspan></text>
""")

# 4. Horizontal (Compact) (300x80)
write_svg('logo-rentease-compact.svg', 300, 80, f"""
  <g transform="scale(0.8)">
    {HORIZONTAL_ICON_SVG}
    <text x="90" y="55" class="font-sans" font-size="48" font-weight="800" fill="#0f766e" dominant-baseline="middle">Rent<tspan fill="#1e293b">Ease</tspan></text>
  </g>
""")

# 5. Auth / Login Page Logo (Centered stacked layout) (300x240)
write_svg('logo-rentease-auth.svg', 300, 240, f"""
  <g transform="translate(100, 10)">
    {PURE_ICON_SVG}
  </g>
  <text x="150" y="150" class="font-sans" font-size="44" font-weight="800" fill="#0f766e" text-anchor="middle">Rent<tspan fill="#1e293b">Ease</tspan></text>
  <text x="150" y="190" class="font-sans" font-size="16" font-weight="600" fill="#64748b" text-anchor="middle" letter-spacing="1.5">PROPERTY MANAGEMENT</text>
""")

# 6. Primary Monotone (for flat styles / printing)
write_svg('logo-rentease-mono.svg', 380, 100, f"""
""")

print("SVG Logos Regenerated!")
