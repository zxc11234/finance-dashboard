#!/usr/bin/env python3
"""Fix QDII data direction reversal and update all values to screenshot data."""
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
replacements = []

def do_replace(old, new, desc=""):
    global html
    if old not in html:
        print(f"WARNING: Cannot find: {desc} :: {old[:80]}...")
        return False
    count = html.count(old)
    if count > 1:
        print(f"WARNING: Multiple ({count}) matches for: {desc} :: {old[:80]}...")
    html = html.replace(old, new)
    replacements.append(f"OK [{count}x]: {desc}")
    return True

# ═══════════════════════════════════════════════════════
# 1. KPI Card (line ~292)
# ═══════════════════════════════════════════════════════
do_replace(
    '🕐 今日收益 (7/16 盘中)</div><div class="kpi-value red">-22,800</div><div class="kpi-sub">017811 -18,870 + 020470 -3,985 / QDII基本持平',
    '🕐 今日收益 (7/16)</div><div class="kpi-value red">-31,285</div><div class="kpi-sub">支付宝实际：017811 -19,348 + 020470 -6,216 + QDII 5只 -5,739 / 嘉实017731待出',
    "KPI today profit"
)

# Total assets KPI (line 290)
do_replace(
    '2,601,020</div><div class="kpi-sub">基金 ~1,565,000 + 余额宝 1,036,020',
    '2,597,000</div><div class="kpi-sub">基金 ~1,541,000 + 余额宝 1,036,038',
    "KPI total assets"
)

# ═══════════════════════════════════════════════════════
# 2. fn[]/fp[] arrays (today gain chart, line ~1060-1061)
# ═══════════════════════════════════════════════════════
# fn order: 017731,018147,539002,006373,018036,020470,017811
# New fp: 017731=0(待出), 018147=-0.99, 539002=-0.97, 006373=-1.63, 018036=-0.56, 020470=-3.85, 017811=-6.74
do_replace(
    "const fp=[0.13,0.13,0.13,0.19,0.18,-2.47,-6.57];",
    "const fp=[0,-0.99,-0.97,-1.63,-0.56,-3.85,-6.74];",
    "fp array (today gain chart)"
)

# Also fix bar chart color logic: currently v>=0 is red. Now most are negative (green bars).
# The current code: backgroundColor:fp.map(v=>v>=0?'rgba(239,68,68,.7)':'rgba(34,197,94,.7)')
# This means positive=red(涨), negative=green(跌) which is the A-share convention. Keep as-is.

# ═══════════════════════════════════════════════════════
# 3. Holding table - row by row
# ═══════════════════════════════════════════════════════

# 017811 row (line 389)
do_replace(
    '<td data-label="市值">268,000</td><td data-label="今日" class="red">-18,870</td><td data-label="累计" class="green">+48,869</td><td data-label="收益率" class="green">+12.6%</td>',
    '<td data-label="市值">267,814</td><td data-label="今日" class="red">-19,348</td><td data-label="累计" class="green">+29,472</td><td data-label="收益率" class="green">+12.3%</td>',
    "017811 holding row"
)

# 020470 row (line 390)
do_replace(
    '<td data-label="市值">157,000</td><td data-label="今日" class="red">-3,985</td><td data-label="累计" class="green">+48,458</td><td data-label="收益率" class="green">+35.4%</td>',
    '<td data-label="市值">155,229</td><td data-label="今日" class="red">-6,216</td><td data-label="累计" class="green">+38,970</td><td data-label="收益率" class="green">+33.5%</td>',
    "020470 holding row"
)

# 国内基金小计 (line 391)
do_replace(
    '<td data-label="成本">354,597.47</td><td data-label="市值">425,000</td><td data-label="今日" class="red">-22,855</td><td data-label="累计" class="green">+97,327</td><td data-label="收益率" class="green">+19.8%</td>',
    '<td data-label="成本">354,639</td><td data-label="市值">423,043</td><td data-label="今日" class="red">-25,564</td><td data-label="累计" class="green">+68,442</td><td data-label="收益率" class="green">+19.3%</td>',
    "domestic subtotal row"
)

# 017731 row (line 394) - mark as 7/15 data
do_replace(
    '<td data-label="成本">490,000.00</td><td data-label="市值">530,000</td><td data-label="今日" class="green">+690</td><td data-label="累计" class="green">+39,654</td><td data-label="收益率" class="green">+8.09%</td>',
    '<td data-label="成本">490,000.00</td><td data-label="市值">515,472<span style="font-size:.6rem;color:var(--muted)"> ⏳7/15</span></td><td data-label="今日" class="muted">待出</td><td data-label="累计" class="green">+25,472</td><td data-label="收益率" class="green">+5.20%</td>',
    "017731 holding row"
)

# 018147 row (line 395)
do_replace(
    '<td data-label="成本">150,000.00</td><td data-label="市值">265,000</td><td data-label="今日" class="green">+345</td><td data-label="累计" class="green">+108,017</td><td data-label="收益率" class="green">+76.6%</td>',
    '<td data-label="成本">150,002</td><td data-label="市值">261,889</td><td data-label="今日" class="red">-2,607</td><td data-label="累计" class="green">+111,887</td><td data-label="收益率" class="green">+74.6%</td>',
    "018147 holding row"
)

# 018036 row (line 396)
do_replace(
    '<td data-label="成本">115,000.00</td><td data-label="市值">168,000</td><td data-label="今日" class="green">+300</td><td data-label="累计" class="green">+49,196</td><td data-label="收益率" class="green">+45.8%</td>',
    '<td data-label="成本">115,003</td><td data-label="市值">166,447</td><td data-label="今日" class="red">-941</td><td data-label="累计" class="green">+51,444</td><td data-label="收益率" class="green">+44.7%</td>',
    "018036 holding row"
)

# 539002 row (line 397)
do_replace(
    '<td data-label="成本">60,000.00</td><td data-label="市值">104,000</td><td data-label="今日" class="green">+135</td><td data-label="累计" class="green">+41,569</td><td data-label="收益率" class="green">+73.8%</td>',
    '<td data-label="成本">60,000.00</td><td data-label="市值">103,074</td><td data-label="今日" class="red">-1,010</td><td data-label="累计" class="green">+43,074</td><td data-label="收益率" class="green">+71.8%</td>',
    "539002 holding row"
)

# 006373 row (line 398)
do_replace(
    '<td data-label="成本">41,566.79</td><td data-label="市值">73,000</td><td data-label="今日" class="green">+139</td><td data-label="累计" class="green">+29,172</td><td data-label="收益率" class="green">+74.8%</td>',
    '<td data-label="成本">41,562</td><td data-label="市值">71,335</td><td data-label="今日" class="red">-1,181</td><td data-label="累计" class="green">+29,773</td><td data-label="收益率" class="green">+71.6%</td>',
    "006373 holding row"
)

# QDII subtotal (line 399)
do_replace(
    '<td data-label="成本">856,566.79</td><td data-label="市值">1,140,000</td><td data-label="今日" class="green">+1,609</td><td data-label="累计" class="green">+267,608</td><td data-label="收益率" class="green">+31.2%</td>',
    '<td data-label="成本">856,567</td><td data-label="市值">1,118,217</td><td data-label="今日" class="red">-5,739</td><td data-label="累计" class="green">+261,650</td><td data-label="收益率" class="green">+30.5%</td>',
    "QDII subtotal row"
)

# Grand total row (line 401)
do_replace(
    '<td data-label="成本">2,247,184.54</td><td data-label="市值" style="font-weight:700">2,601,020</td><td data-label="今日" class="red">-21,246</td><td data-label="累计" class="green">+372,796</td><td data-label="收益率" class="green">+26.6%</td>',
    '<td data-label="成本">2,247,226</td><td data-label="市值" style="font-weight:700">2,597,000</td><td data-label="今日" class="red">-31,285</td><td data-label="累计" class="green">+330,092</td><td data-label="收益率" class="green">+14.7%</td>',
    "grand total row"
)

# ═══════════════════════════════════════════════════════
# 4. Highlight section (line 404-410)
# ═══════════════════════════════════════════════════════
do_replace(
    '· 📊 <strong>今日收益 -22,800</strong>：017811 -18,870（-6.57%）+ 020470 -3,985（-2.47%），QDII 5只基本持平。<br>',
    '· 📊 <strong>今日收益 -31,285</strong>：017811 -19,348（-6.74%）+ 020470 -6,216（-3.85%），QDII全线下跌5只合计 -6,740。嘉实017731 7/16待出。<br>',
    "highlight today profit line"
)

# ═══════════════════════════════════════════════════════
# 5. Stress test amber card (line 328) - fix QDII 持平 text
# ═══════════════════════════════════════════════════════
do_replace(
    'QDII 持平(0%)<br>A股情绪余震 -0.5%(-¥3K)<br>半导体单日流出218亿',
    'QDII全线下跌(-0.8%)<br>A股半导体暴跌 -3%(-¥25K)<br>半导体单日流出218亿',
    "stress test amber card"
)

# ═══════════════════════════════════════════════════════
# 6. us-note (line 353)
# ═══════════════════════════════════════════════════════
do_replace(
    '💡 美股7/15收盘：纳指+0.62%三连涨，但MU-8%（长鑫竞争恐惧）。TSMC盘后公布Q2净利T$706.6亿(+77%)创纪录，大超预期，ADR盘后+0.97%报$423.50。A股7/16收盘：上证-1.83%深成-2.07%，半导体主力流出218亿。',
    '💡 7/16 A股收盘：上证-1.83%，半导体-218亿流出。QDII全线下跌，昨晚美股回调。TSMC Q2 +77%创纪录，今晚美股半导体方向是关键。',
    "us-note text"
)

# ═══════════════════════════════════════════════════════
# 7. Capital structure table (lines 481-500)
# ═══════════════════════════════════════════════════════
do_replace(
    '总资产 ~¥2,601,020',
    '总资产 ~¥2,597,000',
    "capital structure title"
)

# QDII section header (line 483)
do_replace(
    '🌍 QDII 海外基金（5 只）— 占比 43.8%',
    '🌍 QDII 海外基金（5 只）— 占比 43.1%',
    "QDII section header in capital table"
)

# 017731 in capital table (line 484)
do_replace(
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">530,000</td><td data-label="占比">20.4%</td>',
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">515,472</td><td data-label="占比">19.8%</td>',
    "017731 in capital table"
)

# 018147 in capital table (line 485)
do_replace(
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">265,000</td><td data-label="占比">10.2%</td>',
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">261,889</td><td data-label="占比">10.1%</td>',
    "018147 in capital table"
)

# 018036 in capital table (line 486)
do_replace(
    '<td data-label="方向">🚗 新能源车</td><td data-label="市值" class="green">168,000</td><td data-label="占比">6.5%</td>',
    '<td data-label="方向">🚗 新能源车</td><td data-label="市值" class="green">166,447</td><td data-label="占比">6.4%</td>',
    "018036 in capital table"
)

# 539002 in capital table (line 487)
do_replace(
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">104,000</td><td data-label="占比">4.0%</td>',
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">103,074</td><td data-label="占比">4.0%</td>',
    "539002 in capital table"
)

# 006373 in capital table (line 488)
do_replace(
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">73,000</td><td data-label="占比">2.8%</td>',
    '<td data-label="方向">全球半导体/科技</td><td data-label="市值" class="green">71,335</td><td data-label="占比">2.7%</td>',
    "006373 in capital table"
)

# QDII subtotal in capital table (line 489)
do_replace(
    '<td data-label="市值">1,140,000</td><td data-label="占比">43.8%',
    '<td data-label="市值">1,118,217</td><td data-label="占比">43.1%',
    "QDII subtotal in capital table"
)

# A股 section header (line 491)
do_replace(
    '🇨🇳 A股基金（2 只）— 占比 16.3%',
    '🇨🇳 A股基金（2 只）— 占比 16.3%',
    "A股 section header"
)

# 017811 in capital table (line 492)
do_replace(
    '<td data-label="方向">🔬 半导体设备/AI</td><td data-label="市值" class="green">268,000</td><td data-label="占比">10.3%</td>',
    '<td data-label="方向">🔬 半导体设备/AI</td><td data-label="市值" class="green">267,814</td><td data-label="占比">10.3%</td>',
    "017811 in capital table"
)

# 020470 in capital table (line 493)
do_replace(
    '<td data-label="方向">🔬 半导体综合</td><td data-label="市值" class="green">157,000</td><td data-label="占比">6.0%</td>',
    '<td data-label="方向">🔬 半导体综合</td><td data-label="市值" class="green">155,229</td><td data-label="占比">6.0%</td>',
    "020470 in capital table"
)

# A股 subtotal in capital table (line 494)
do_replace(
    '<td data-label="市值">425,000</td><td data-label="占比">16.3%',
    '<td data-label="市值">423,043</td><td data-label="占比">16.3%',
    "A股 subtotal in capital table"
)

# Cash section header (line 496)
do_replace(
    '💵 现金 — 占比 39.8%',
    '💵 现金 — 占比 39.9%',
    "cash section header"
)

# 余额宝 in capital table (line 497)
do_replace(
    '<td data-label="市值">1,036,020</td><td data-label="占比">39.8%',
    '<td data-label="市值">1,036,038</td><td data-label="占比">39.9%',
    "余额宝 in capital table"
)

# Cash subtotal (line 498)
do_replace(
    '<td data-label="市值">1,036,020</td><td data-label="占比">39.8%</td></tr>\n\n    <tr class="subtotal" style="background:rgba(59,130,246,.04)"><td>总计</td><td data-label="方向">—</td><td data-label="市值" style="font-weight:700">2,601,020</td>',
    '<td data-label="市值">1,036,038</td><td data-label="占比">39.9%</td></tr>\n\n    <tr class="subtotal" style="background:rgba(59,130,246,.04)"><td>总计</td><td data-label="方向">—</td><td data-label="市值" style="font-weight:700">2,597,000</td>',
    "cash subtotal and total"
)

# ═══════════════════════════════════════════════════════
# 8. Theme exposure table (lines 508-513)
# ═══════════════════════════════════════════════════════
# 全球半导体/科技: 017731+018147+539002+006373 = 515,472+261,889+103,074+71,335 = 951,770
do_replace(
    "017731+018147+539002+006373</td><td data-label=\"市值\" class=\"green\">972,000</td><td data-label=\"占比\"><strong>37.4%</strong>",
    "017731+018147+539002+006373</td><td data-label=\"市值\" class=\"green\">951,770</td><td data-label=\"占比\"><strong>36.7%</strong>",
    "theme: global semi/tech"
)

# A股半导体设备 017811
do_replace(
    '<td data-label="基金">017811</td><td data-label="市值">268,000</td><td data-label="占比"><strong>10.3%</strong>',
    '<td data-label="基金">017811</td><td data-label="市值">267,814</td><td data-label="占比"><strong>10.3%</strong>',
    "theme: A股半导体设备"
)

# A股半导体非设备 020470
do_replace(
    '<td data-label="基金">020470</td><td data-label="市值">157,000</td><td data-label="占比">6.0%',
    '<td data-label="基金">020470</td><td data-label="市值">155,229</td><td data-label="占比">6.0%',
    "theme: A股半导体非设备"
)

# 全球新能源车 018036
do_replace(
    '<td data-label="基金">018036</td><td data-label="市值">168,000</td><td data-label="占比">6.3%',
    '<td data-label="基金">018036</td><td data-label="市值">166,447</td><td data-label="占比">6.4%',
    "theme: 全球新能源车"
)

# 现金 in theme table
do_replace(
    '<td data-label="基金">余额宝</td><td data-label="市值">1,036,020</td><td data-label="占比"><strong>39.8%</strong>',
    '<td data-label="基金">余额宝</td><td data-label="市值">1,036,038</td><td data-label="占比"><strong>39.9%</strong>',
    "theme: cash"
)

# 半导体总集中度 (全球半导体951,770 + A股设备267,814 + A股非设备155,229 = 1,374,813 → 52.9%)
do_replace(
    '⚠️ 半导体总集中度（全球+A股）</td><td data-label="市值" class="red">1,397,000</td><td data-label="占比" class="red"><strong>53.7%</strong>',
    '⚠️ 半导体总集中度（全球+A股）</td><td data-label="市值" class="red">1,374,813</td><td data-label="占比" class="red"><strong>52.9%</strong>',
    "theme: semi total concentration"
)

# ═══════════════════════════════════════════════════════
# 9. P&L Structure table (lines 521-529)
# ═══════════════════════════════════════════════════════
# 018147
do_replace(
    '018147 建信新兴市场 C</td><td data-label="市值">265,000</td><td data-label="成本">150,000</td><td data-label="盈亏" class="green">+115,000</td><td data-label="收益率" class="green">+76.7%',
    '018147 建信新兴市场 C</td><td data-label="市值">261,889</td><td data-label="成本">150,002</td><td data-label="盈亏" class="green">+111,887</td><td data-label="收益率" class="green">+74.6%',
    "P&L: 018147"
)

# 017811
do_replace(
    '017811 东方人工智能</td><td data-label="市值">268,000</td><td data-label="成本">238,342</td><td data-label="盈亏" class="green">+29,658</td><td data-label="收益率" class="green">+12.4%',
    '017811 东方人工智能</td><td data-label="市值">267,814</td><td data-label="成本">238,380</td><td data-label="盈亏" class="green">+29,434</td><td data-label="收益率" class="green">+12.3%',
    "P&L: 017811"
)

# 020470
do_replace(
    '020470 长城半导体</td><td data-label="市值">157,000</td><td data-label="成本">116,256</td><td data-label="盈亏" class="green">+40,744</td><td data-label="收益率" class="green">+35.0%',
    '020470 长城半导体</td><td data-label="市值">155,229</td><td data-label="成本">116,259</td><td data-label="盈亏" class="green">+38,970</td><td data-label="收益率" class="green">+33.5%',
    "P&L: 020470"
)

# 539002
do_replace(
    '539002 建信新兴市场 A</td><td data-label="市值">104,000</td><td data-label="成本">60,000</td><td data-label="盈亏" class="green">+44,000</td><td data-label="收益率" class="green">+73.3%',
    '539002 建信新兴市场 A</td><td data-label="市值">103,074</td><td data-label="成本">60,000</td><td data-label="盈亏" class="green">+43,074</td><td data-label="收益率" class="green">+71.8%',
    "P&L: 539002"
)

# 017731
do_replace(
    '017731 嘉实全球产业升级</td><td data-label="市值">530,000</td><td data-label="成本">490,000</td><td data-label="盈亏" class="green">+40,000</td><td data-label="收益率" class="green">+8.16%',
    '017731 嘉实全球产业升级</td><td data-label="市值">515,472</td><td data-label="成本">490,000</td><td data-label="盈亏" class="green">+25,472</td><td data-label="收益率" class="green">+5.20%',
    "P&L: 017731"
)

# 018036
do_replace(
    '018036 长城全球新能源车</td><td data-label="市值">168,000</td><td data-label="成本">115,000</td><td data-label="盈亏" class="green">+53,000</td><td data-label="收益率" class="green">+46.1%',
    '018036 长城全球新能源车</td><td data-label="市值">166,447</td><td data-label="成本">115,003</td><td data-label="盈亏" class="green">+51,444</td><td data-label="收益率" class="green">+44.7%',
    "P&L: 018036"
)

# 006373
do_replace(
    '006373 国富全球科技</td><td data-label="市值">73,000</td><td data-label="成本">41,567</td><td data-label="盈亏" class="green">+31,433</td><td data-label="收益率" class="green">+75.6%',
    '006373 国富全球科技</td><td data-label="市值">71,335</td><td data-label="成本">41,562</td><td data-label="盈亏" class="green">+29,773</td><td data-label="收益率" class="green">+71.6%',
    "P&L: 006373"
)

# P&L subtotal: 基金合计 7只
# mkt total: 267,814+155,229+515,472+261,889+166,447+103,074+71,335 = 1,541,260
# cost total: 238,380+116,259+490,000+150,002+115,003+60,000+41,562 = 1,211,206
# profit: 330,054, pct: 27.3%
do_replace(
    '基金合计（7只）</td><td data-label="市值">1,565,000</td><td data-label="成本">1,211,154</td><td data-label="盈亏" class="green">+353,839</td><td data-label="收益率" class="green">+29.2%',
    '基金合计（7只）</td><td data-label="市值">1,541,260</td><td data-label="成本">1,211,206</td><td data-label="盈亏" class="green">+330,054</td><td data-label="收益率" class="green">+27.3%',
    "P&L: subtotal 7 funds"
)

# P&L total with cash
do_replace(
    '含现金总计</td><td data-label="市值">2,601,020</td><td data-label="成本">2,247,174</td><td data-label="盈亏" class="green">+353,839</td><td data-label="收益率" class="green">+15.7%',
    '含现金总计</td><td data-label="市值">2,577,298</td><td data-label="成本">2,247,244</td><td data-label="盈亏" class="green">+330,054</td><td data-label="收益率" class="green">+14.7%',
    "P&L: total with cash"
)

# ═══════════════════════════════════════════════════════
# 10. alloc highlight (line 537)
# ═══════════════════════════════════════════════════════
do_replace(
    '当前 QDII 占比约43.8%，国内基金约16.3%，现金约39.8%。',
    '当前 QDII 占比约43.1%，国内基金约16.3%，现金约39.9%。',
    "alloc highlight QDII percentage"
)

do_replace(
    '⚠️ 半导体总集中度 53.7%（全球37.4%+A股16.3%）',
    '⚠️ 半导体总集中度 52.9%（全球36.7%+A股16.3%）',
    "alloc highlight semi concentration"
)

# ═══════════════════════════════════════════════════════
# 11. News item (line 570)
# ═══════════════════════════════════════════════════════
do_replace(
    '017811东方AI今日-6.57%(-18,870)，020470长城半导体-2.47%(-3,985)。QDII 5只基本持平。',
    '017811东方AI今日-6.74%(-19,348)，020470长城半导体-3.85%(-6,216)。QDII全线下跌，5只QDII合计亏损约¥6,740。',
    "news item: today summary"
)

# ═══════════════════════════════════════════════════════
# 12. Comprehensive analysis text (line 607)
# ═══════════════════════════════════════════════════════
do_replace(
    '当前持仓：国内2只（017811 ¥26.8万+020470 ¥15.7万）+ QDII 5只（¥114万）。现金¥104万(39.8%)待命。半导体集中度已从61.9%降至53.7%。',
    '当前持仓：国内2只（017811 ¥26.8万+020470 ¥15.5万）+ QDII 5只（¥112万）。现金¥104万(39.9%)待命。半导体集中度已从61.9%降至52.9%。',
    "comprehensive analysis: position summary"
)

# ═══════════════════════════════════════════════════════
# 13. AI analysis (line 785)
# ═══════════════════════════════════════════════════════
do_replace(
    '国内敞口仅剩017811（¥26.8万利润垫+12.6%）和020470（¥15.7万利润垫+35.4%），浮亏清零。QDII端5只（¥114万）不受A股踩踏影响——TSMC创纪录+77%直接利好017731。现金¥104万(39.8%)是当前最大优势。',
    '国内敞口仅剩017811（¥26.8万利润垫+12.3%）和020470（¥15.5万利润垫+33.5%），浮亏清零。QDII端未能幸免，5只QDII合计 -¥6,740，昨晚美股回调传导至QDII端，建信新兴C -0.99%、国富全球科技 -1.63%。现金¥104万(39.9%)是当前最大优势。',
    "AI analysis: QDII section"
)

# ═══════════════════════════════════════════════════════
# 14. Stress test static note (line 341)
# ═══════════════════════════════════════════════════════
do_replace(
    '基于当前持仓(QDII ¥114万/A股 ¥43万/现金 ¥104万)静态测算',
    '基于当前持仓(QDII ¥112万/A股 ¥42万/现金 ¥104万)静态测算',
    "stress test note"
)

# ═══════════════════════════════════════════════════════
# 15. alertData[] (lines 976-983)
# ═══════════════════════════════════════════════════════
do_replace(
    "{name:'017731 嘉实产业升级',cost:490000.00,mkt:530000,pct:8.2},",
    "{name:'017731 嘉实产业升级',cost:490000.00,mkt:515472,pct:5.2},",
    "alertData: 017731"
)
do_replace(
    "{name:'017811 东方人工智能',cost:238341.55,mkt:268000,pct:12.4},",
    "{name:'017811 东方人工智能',cost:238380,mkt:267814,pct:12.3},",
    "alertData: 017811"
)
do_replace(
    "{name:'020470 长城半导体',cost:116255.92,mkt:157000,pct:35.0},",
    "{name:'020470 长城半导体',cost:116259,mkt:155229,pct:33.5},",
    "alertData: 020470"
)
do_replace(
    "{name:'018036 新能源车',cost:115000.00,mkt:168000,pct:46.1},",
    "{name:'018036 新能源车',cost:115003,mkt:166447,pct:44.7},",
    "alertData: 018036"
)
do_replace(
    "{name:'539002 建信新兴A',cost:60000.00,mkt:104000,pct:73.3},",
    "{name:'539002 建信新兴A',cost:60000.00,mkt:103074,pct:71.8},",
    "alertData: 539002"
)
do_replace(
    "{name:'006373 国富科技',cost:41566.79,mkt:73000,pct:75.6},",
    "{name:'006373 国富科技',cost:41562,mkt:71335,pct:71.6},",
    "alertData: 006373"
)
do_replace(
    "{name:'018147 建信新兴C',cost:150000.00,mkt:265000,pct:76.7},",
    "{name:'018147 建信新兴C',cost:150002,mkt:261889,pct:74.6},",
    "alertData: 018147"
)

# ═══════════════════════════════════════════════════════
# 16. radarFunds (lines 1005-1008)
# ═══════════════════════════════════════════════════════
# Format: data:[pct, profit, today_pct, weight, pct]
do_replace(
    "'017811':{name:'017811 东方AI',color:'#3b82f6',data:[12.4,29658,-6.57,10.3,12.4]}",
    "'017811':{name:'017811 东方AI',color:'#3b82f6',data:[12.3,29434,-6.74,10.3,12.3]}",
    "radarFunds: 017811"
)
do_replace(
    "'017731':{name:'017731 嘉实产业',color:'#f59e0b',data:[8.2,40000,0.13,20.4,8.2]}",
    "'017731':{name:'017731 嘉实产业',color:'#f59e0b',data:[5.2,25472,0,19.8,5.2]}",
    "radarFunds: 017731"
)
do_replace(
    "'018147':{name:'018147 建信C',color:'#a855f7',data:[76.7,115000,0.13,10.2,76.7]}",
    "'018147':{name:'018147 建信C',color:'#a855f7',data:[74.6,111887,-0.99,10.1,74.6]}",
    "radarFunds: 018147"
)
do_replace(
    "'020470':{name:'020470 长城半导体',color:'#10b981',data:[35.0,40744,-2.47,6.0,35.0]}",
    "'020470':{name:'020470 长城半导体',color:'#10b981',data:[33.5,38970,-3.85,6.0,33.5]}",
    "radarFunds: 020470"
)

# ═══════════════════════════════════════════════════════
# 17. allocPie chart data (line 1063)
# ═══════════════════════════════════════════════════════
# Labels: 余额宝, 017731, 017811, 018147, 020470, 018036, 539002, 006373
do_replace(
    "data:[1036020.28,530000,268000,265000,157000,168000,104000,73000]",
    "data:[1036038,515472,267814,261889,155229,166447,103074,71335]",
    "allocPie data"
)

# ═══════════════════════════════════════════════════════
# 18. allocDonut chart (line 1182)
# ═══════════════════════════════════════════════════════
do_replace(
    "labels:['国内基金','QDII','现金'],datasets:[{data:[16.3,43.8,39.8],backgroundColor:['#3b82f6','#f59e0b','#94a3b8']",
    "labels:['国内基金','QDII','现金','其他'],datasets:[{data:[16.3,43.1,39.9,0.7],backgroundColor:['#3b82f6','#f59e0b','#94a3b8','#64748b']",
    "allocDonut data"
)

# ═══════════════════════════════════════════════════════
# 19. allocTrend (lines 1194-1196)
# ═══════════════════════════════════════════════════════
do_replace(
    "const allocQDII=[0,10,25,40,52,60,43.8];",
    "const allocQDII=[0,10,25,40,52,60,43.1];",
    "allocTrend QDII"
)
do_replace(
    "const allocCash=[20,20,15,10,8,5,39.8];",
    "const allocCash=[20,20,15,10,8,5,39.9];",
    "allocTrend cash"
)

# ═══════════════════════════════════════════════════════
# 20. Roadmap note (line 476)
# ═══════════════════════════════════════════════════════
do_replace(
    '半导体集中度已降至53.7%，不急于增加敞口',
    '半导体集中度已降至52.9%，不急于增加敞口',
    "roadmap note"
)

# ═══════════════════════════════════════════════════════
# 21. 余额宝 in holding table (line 386)
# ═══════════════════════════════════════════════════════
do_replace(
    '1,036,020.28</td><td data-label="市值" style="font-weight:700">1,036,020.28</td><td data-label="今日" class="muted">0.00</td>',
    '1,036,019.90</td><td data-label="市值" style="font-weight:700">1,036,038.30</td><td data-label="今日" class="green">+18.40</td>',
    "余额宝 holding row"
)

# ═══════════════════════════════════════════════════════
# 22. QDII Lag Board - update dates
# ═══════════════════════════════════════════════════════
do_replace(
    '7/14 → 延迟1天',
    '7/15 → 7/16待更新',
    "QDII lag board dates (all)"
)

# ═══════════════════════════════════════════════════════
# 23. Footer
# ═══════════════════════════════════════════════════════
do_replace(
    '2026年7月16日 15:30更新',
    '2026年7月17日 01:30更新（修正QDII数据）',
    "footer timestamp"
)

# ═══════════════════════════════════════════════════════
# Write output
# ═══════════════════════════════════════════════════════
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n{'='*60}")
print(f"Total replacements: {len(replacements)}")
for r in replacements:
    print(f"  {r}")
print(f"File size: {original_len} → {len(html)} (delta: {len(html)-original_len})")
print(f"{'='*60}")
