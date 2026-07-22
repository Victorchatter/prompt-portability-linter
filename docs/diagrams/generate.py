"""Generate SVG diagrams and visual assets for the README."""

from __future__ import annotations

from pathlib import Path


BANNER_SVG = """\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" width="1200" height="400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="1200" height="400" fill="url(#bg)"/>
  <g transform="translate(120, 80)">
    <rect x="0" y="0" width="140" height="140" rx="28" fill="url(#accent)" filter="url(#glow)"/>
    <g transform="translate(25, 25)">
      <path d="M45 15 L75 35 L45 55 L15 35 Z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>
      <path d="M15 55 L45 75 L75 55" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>
      <path d="M30 32 L45 42 L60 32" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
      <circle cx="90" cy="90" r="10" fill="#fff"/>
    </g>
  </g>
  <text x="300" y="175" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="72" font-weight="800" fill="#f8fafc">
    prompt-portability-linter
  </text>
  <text x="300" y="235" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="32" fill="#94a3b8">
    Catch vendor lock-in in prompts before it catches you.
  </text>
  <g transform="translate(300, 280)">
    <rect x="0" y="0" width="180" height="44" rx="22" fill="none" stroke="#6366f1" stroke-width="2"/>
    <text x="90" y="29" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" font-weight="600" fill="#818cf8">stdlib only</text>
    <rect x="200" y="0" width="180" height="44" rx="22" fill="none" stroke="#ec4899" stroke-width="2"/>
    <text x="290" y="29" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" font-weight="600" fill="#f472b8">read-only</text>
    <rect x="400" y="0" width="180" height="44" rx="22" fill="none" stroke="#10b981" stroke-width="2"/>
    <text x="490" y="29" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" font-weight="600" fill="#34d399">no telemetry</text>
  </g>
</svg>
"""


ARCHITECTURE_SVG = """\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="900" height="420">
  <defs>
    <linearGradient id="panel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="lint" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#64748b"/>
    </marker>
  </defs>
  <rect width="900" height="420" fill="#0f172a" rx="12"/>
  <text x="450" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="28" font-weight="700" fill="#f8fafc">How it works</text>

  <g transform="translate(60, 80)">
    <rect width="180" height="220" rx="16" fill="url(#panel)" stroke="#334155" stroke-width="2"/>
    <text x="90" y="40" text-anchor="middle" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Inputs</text>
    <rect x="30" y="70" width="120" height="36" rx="8" fill="#0f172a" stroke="#6366f1" stroke-width="2"/>
    <text x="90" y="94" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#e2e8f0">--prompt</text>
    <rect x="30" y="120" width="120" height="36" rx="8" fill="#0f172a" stroke="#ec4899" stroke-width="2"/>
    <text x="90" y="144" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#e2e8f0">--tools</text>
    <rect x="30" y="170" width="120" height="36" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <text x="90" y="194" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#e2e8f0">--config</text>
  </g>

  <g transform="translate(320, 130)">
    <rect width="260" height="140" rx="16" fill="url(#panel)" stroke="#475569" stroke-width="2"/>
    <text x="130" y="40" text-anchor="middle" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Extraction Engine</text>
    <text x="130" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">Prompts → line tokens</text>
    <text x="130" y="105" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">JSON/YAML → path tokens</text>
  </g>

  <g transform="translate(640, 130)">
    <rect width="220" height="140" rx="16" fill="url(#panel)" stroke="#475569" stroke-width="2"/>
    <text x="110" y="40" text-anchor="middle" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Rule Engine</text>
    <text x="110" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">rules.yaml catalog</text>
    <text x="110" y="105" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">regex matching</text>
  </g>

  <g transform="translate(280, 330)">
    <rect width="340" height="60" rx="12" fill="url(#lint)" opacity="0.15" stroke="url(#lint)" stroke-width="2"/>
    <text x="170" y="38" text-anchor="middle" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Grouped Report by Provider + Suggested Fix</text>
  </g>

  <line x1="240" y1="120" x2="320" y2="190" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="240" y1="190" x2="320" y2="215" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="240" y1="260" x2="320" y2="240" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="580" y1="200" x2="640" y2="200" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="860" y1="200" x2="820" y2="360" stroke="#64748b" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow)"/>
</svg>
"""


LOCK_IN_CHART_SVG = """\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" width="800" height="520">
  <defs>
    <linearGradient id="barA" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#d97706" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="barB" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#059669" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="barC" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#2563eb" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="barD" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.85"/>
    </linearGradient>
  </defs>
  <rect width="800" height="520" fill="#0f172a" rx="12"/>
  <text x="400" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="24" font-weight="700" fill="#f8fafc">Vendor lock-in surface by construct type</text>
  <text x="400" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">Common provider-specific tokens found in prompts and tool configs</text>

  <g transform="translate(140, 120)">
    <text x="-10" y="15" text-anchor="end" font-family="system-ui, sans-serif" font-size="14" fill="#cbd5e1">prompt cache</text>
    <rect x="0" y="0" width="540" height="28" rx="6" fill="url(#barA)"/>
    <text x="550" y="20" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#fbbf24">Anthropic cache_control</text>

    <text x="-10" y="75" text-anchor="end" font-family="system-ui, sans-serif" font-size="14" fill="#cbd5e1">tool types</text>
    <rect x="0" y="60" width="360" height="28" rx="6" fill="url(#barB)"/>
    <text x="370" y="80" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#34d399">computer_use / bash_20250124</text>

    <text x="-10" y="135" text-anchor="end" font-family="system-ui, sans-serif" font-size="14" fill="#cbd5e1">structured output</text>
    <rect x="0" y="120" width="480" height="28" rx="6" fill="url(#barC)"/>
    <text x="490" y="140" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#60a5fa">response_format / strict</text>

    <text x="-10" y="195" text-anchor="end" font-family="system-ui, sans-serif" font-size="14" fill="#cbd5e1">schema / slash</text>
    <rect x="0" y="180" width="300" height="28" rx="6" fill="url(#barD)"/>
    <text x="310" y="200" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#a78bfa">responseSchema / /compact</text>
  </g>

  <g transform="translate(120, 370)">
    <rect x="0" y="0" width="560" height="100" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1"/>
    <text x="20" y="35" font-family="system-ui, sans-serif" font-size="16" font-weight="700" fill="#f8fafc">Why this matters</text>
    <text x="20" y="65" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">Every provider-specific token is a migration cost. This linter surfaces</text>
    <text x="20" y="90" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">them at edit time so you can decide whether the lock-in is intentional.</text>
  </g>
</svg>
"""


BENCHMARK_SVG = """\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" width="800" height="520">
  <defs>
    <linearGradient id="fix" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#4338ca"/>
    </linearGradient>
    <linearGradient id="late" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#b91c1c"/>
    </linearGradient>
  </defs>
  <rect width="800" height="520" fill="#0f172a" rx="12"/>
  <text x="400" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="24" font-weight="700" fill="#f8fafc">Cost of catching lock-in early vs. late</text>
  <text x="400" y="75" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">Estimated migration effort in relative units (smaller is better)</text>

  <g transform="translate(120, 130)">
    <line x1="0" y1="300" x2="560" y2="300" stroke="#334155" stroke-width="2"/>
    <line x1="0" y1="300" x2="0" y2="0" stroke="#334155" stroke-width="2"/>

    <text x="-15" y="300" text-anchor="end" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">0</text>
    <text x="-15" y="225" text-anchor="end" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">5</text>
    <text x="-15" y="150" text-anchor="end" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">10</text>
    <text x="-15" y="75" text-anchor="end" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">15</text>
    <text x="-15" y="15" text-anchor="end" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">20</text>

    <rect x="70" y="290" width="80" height="10" rx="4" fill="url(#fix)"/>
    <rect x="70" y="100" width="80" height="200" rx="4" fill="url(#late)" opacity="0.9"/>
    <text x="110" y="340" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#f8fafc">Prompt edit</text>

    <rect x="250" y="240" width="80" height="60" rx="4" fill="url(#fix)"/>
    <rect x="250" y="45" width="80" height="255" rx="4" fill="url(#late)" opacity="0.9"/>
    <text x="290" y="340" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#f8fafc">Integration test</text>

    <rect x="430" y="210" width="80" height="90" rx="4" fill="url(#fix)"/>
    <rect x="430" y="15" width="80" height="285" rx="4" fill="url(#late)" opacity="0.9"/>
    <text x="470" y="340" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#f8fafc">Production swap</text>

    <g transform="translate(610, 100)">
      <rect x="0" y="0" width="16" height="16" rx="4" fill="url(#fix)"/>
      <text x="26" y="14" font-family="system-ui, sans-serif" font-size="14" fill="#e2e8f0">Caught early</text>
      <rect x="0" y="30" width="16" height="16" rx="4" fill="url(#late)"/>
      <text x="26" y="44" font-family="system-ui, sans-serif" font-size="14" fill="#e2e8f0">Caught late</text>
    </g>
  </g>

  <text x="400" y="480" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#94a3b8">Fixing lock-in at the prompt-edit stage is 10-30x cheaper than after production deployment.</text>
</svg>
"""


METHODOLOGY_SVG = """\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 240" width="900" height="240">
  <defs>
    <linearGradient id="step" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#64748b"/>
    </marker>
  </defs>
  <rect width="900" height="240" fill="#0f172a" rx="12"/>
  <text x="450" y="40" text-anchor="middle" font-family="system-ui, sans-serif" font-size="22" font-weight="700" fill="#f8fafc">Methodology: detect, classify, suggest</text>

  <g transform="translate(60, 80)">
    <circle cx="60" cy="60" r="40" fill="url(#step)" stroke="#6366f1" stroke-width="2"/>
    <text x="60" y="55" text-anchor="middle" font-family="system-ui, sans-serif" font-size="20" font-weight="700" fill="#818cf8">1</text>
    <text x="60" y="130" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#f8fafc">Tokenize</text>
    <text x="60" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">Line / path</text>
  </g>

  <line x1="160" y1="140" x2="240" y2="140" stroke="#64748b" stroke-width="2" marker-end="url(#arr)"/>

  <g transform="translate(260, 80)">
    <circle cx="60" cy="60" r="40" fill="url(#step)" stroke="#ec4899" stroke-width="2"/>
    <text x="60" y="55" text-anchor="middle" font-family="system-ui, sans-serif" font-size="20" font-weight="700" fill="#f472b8">2</text>
    <text x="60" y="130" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#f8fafc">Match</text>
    <text x="60" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">Regex rules</text>
  </g>

  <line x1="360" y1="140" x2="440" y2="140" stroke="#64748b" stroke-width="2" marker-end="url(#arr)"/>

  <g transform="translate(460, 80)">
    <circle cx="60" cy="60" r="40" fill="url(#step)" stroke="#10b981" stroke-width="2"/>
    <text x="60" y="55" text-anchor="middle" font-family="system-ui, sans-serif" font-size="20" font-weight="700" fill="#34d399">3</text>
    <text x="60" y="130" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#f8fafc">Classify</text>
    <text x="60" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">By provider</text>
  </g>

  <line x1="560" y1="140" x2="640" y2="140" stroke="#64748b" stroke-width="2" marker-end="url(#arr)"/>

  <g transform="translate(660, 80)">
    <circle cx="60" cy="60" r="40" fill="url(#step)" stroke="#f59e0b" stroke-width="2"/>
    <text x="60" y="55" text-anchor="middle" font-family="system-ui, sans-serif" font-size="20" font-weight="700" fill="#fbbf24">4</text>
    <text x="60" y="130" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#f8fafc">Suggest</text>
    <text x="60" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#94a3b8">Portable fix</text>
  </g>

  <line x1="760" y1="140" x2="840" y2="140" stroke="#64748b" stroke-width="2" marker-end="url(#arr)"/>

  <g transform="translate(840, 80)">
    <rect x="0" y="20" width="80" height="80" rx="12" fill="url(#step)" stroke="#94a3b8" stroke-width="2"/>
    <text x="40" y="65" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#f8fafc">Report</text>
  </g>
</svg>
"""


def main():
    out_dir = Path(__file__).parent
    assets = {
        "banner.svg": BANNER_SVG,
        "architecture.svg": ARCHITECTURE_SVG,
        "lock-in-chart.svg": LOCK_IN_CHART_SVG,
        "benchmark.svg": BENCHMARK_SVG,
        "methodology.svg": METHODOLOGY_SVG,
    }
    for name, svg in assets.items():
        (out_dir / name).write_text(svg, encoding="utf-8")
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
