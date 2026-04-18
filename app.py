import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# ==========================================
# 1. 页面基本配置
# ==========================================
st.set_page_config(layout="wide", page_title="Asian Carbon Sandbox", page_icon="🌍")

if 'play_year' not in st.session_state:
    st.session_state.play_year = 1997
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

if st.session_state.is_playing:
    time.sleep(1.2) # 因为史料变多了，稍微再放慢一点点播放速度供阅读
    if st.session_state.play_year < 2060:
        st.session_state.play_year += 1
    else:
        st.session_state.is_playing = False

# ==========================================
# 2. 语言字典
# ==========================================
with st.sidebar:
    lang = st.radio("🌐 Language", ["中文", "English"], horizontal=True)
    st.markdown("---")

if lang == "中文":
    t = {
        "title": "🌍 亚洲碳市场与气候地缘世纪推演 (1997-2060)",
        "subtitle": "SIPA 期末项目展示 | 研究员: Joey Wang",
        "sidebar_title": "⚙️ 战略控制台",
        "slider": "🕰️ 时代演进",
        "play": "▶️ 播放", "pause": "⏸️ 暂停",
        "challenge_header": "⚠️ 宏观挑战与冲击",
        "cbam_toggle": "启动欧盟 CBAM 关税制裁",
        "link_toggle": "启动东北亚碳市场链接",
        "legend_title": "**图例说明:**",
        "legend_text": "* 🔴 **主导市场**：中国\n* 🔵 **成熟市场**：日、韩、新\n* 🟡 **新兴市场**：东盟与印度\n* 🟢 **绿色资产流**：NbS交易矩阵\n* 🚨 **合规压力流**：CBAM关税冲击线",
        "year_label": "📅 历史节点:",
        "phase1_text": "第一阶段：早期探索与地方试点 (1997—2020)",
        "phase2_text": "第二阶段：全国强制市场建立与快速扩张 (2021—2025)",
        "phase3_text": "第三阶段：强制履约深化与行业扩容 (2026—2030)",
        "phase4_text": "第四阶段：深度脱碳、区域一体化与净零 (2031—2060)",
        "cbam_alert": "🚨 **CBAM 冲击分析**：亚洲主要出口国面临碳成本倒灌风险。",
        "link_alert": "✨ **战略解读**：区域互联显著提升了亚洲碳资产的市场定价权。",
        "cn": "中国", "jp": "日本", "kr": "韩国", "sg": "新加坡", "id": "印尼", "in": "印度", "vn": "越南", "th": "泰国", "my": "马来西亚", "eu": "欧洲/CBAM"
    }
else:
    t = {
        "title": "🌍 Asian Carbon Market & Climate Geopolitics Sandbox",
        "subtitle": "SIPA Final Project | Researcher: Joey Wang",
        "sidebar_title": "⚙️ Command Center",
        "slider": "🕰️ Timeline Evolution",
        "play": "▶️ Play", "pause": "Pause",
        "challenge_header": "⚠️ Macro Shocks",
        "cbam_toggle": "Activate EU CBAM",
        "link_toggle": "Activate NE-Asia Link",
        "legend_title": "**Legend:**",
        "legend_text": "* 🔴 **Leader**: China\n* 🔵 **Mature**: JP, KR, SG\n* 🟡 **Emerging**: ASEAN & India\n* 🟢 **Green Flow**: NbS Matrix\n* 🚨 **CBAM**: Carbon Tariff Flows",
        "year_label": "📅 Year:",
        "phase1_text": "Phase 1: Early Exploration (1997-2020)",
        "phase2_text": "Phase 2: National Expansion (2021-2025)",
        "phase3_text": "Phase 3: Deep Compliance (2026-2030)",
        "phase4_text": "Phase 4: Net-Zero Integration (2031-2060)",
        "cbam_alert": "🚨 **CBAM Insight**: Major exporters face domestic carbon cost backflow.",
        "link_alert": "✨ **Strategic**: Regional integration boosts carbon asset premium.",
        "cn": "China", "jp": "Japan", "kr": "S.Korea", "sg": "Singapore", "id": "Indonesia", "in": "India", "vn": "Vietnam", "th": "Thailand", "my": "Malaysia", "eu": "欧洲/CBAM"
    }

# ==========================================
# 3. 侧边栏
# ==========================================
with st.sidebar:
    st.header(t["sidebar_title"])
    c_p1, c_p2 = st.columns(2)
    if c_p1.button(t["play"]): 
        st.session_state.is_playing = True
        st.rerun()
    if c_p2.button(t["pause"]): 
        st.session_state.is_playing = False
        st.rerun()
    selected_year = st.slider(t["slider"], 1997, 2060, key="play_year")
    st.markdown("---")
    st.subheader(t["challenge_header"])
    cbam_trigger = st.toggle(t["cbam_toggle"], value=False)
    link_trigger = st.toggle(t["link_toggle"], value=False)
    st.markdown("---")
    st.markdown(t["legend_title"] + "\n" + t["legend_text"])

# ==========================================
# 4. 【史诗级】国家历史数据库 (全面整合中日韩深度史料)
# ==========================================
def get_detailed_history(country, year, lang):
    db = {
        "cn": {
            1997: ("签署《京都议定书》，以发展中国家身份开始接触碳排放概念。", "Signed Kyoto Protocol, introduced to carbon emission concepts."),
            2002: ("积极开展清洁发展机制(CDM)项目建设。", "Actively developed Clean Development Mechanism (CDM) projects."),
            2005: ("CDM项目蓬勃发展，成为当时全球最大CDM碳信用供应国。", "Became the world's largest supplier of CDM carbon credits."),
            2011: ("发改委批准北京、天津、广东等七省市开展碳交易试点。", "NDRC approved 7 regional carbon trading pilots."),
            2013: ("深圳、上海、北京碳排放权交易试点先后启动交易。", "Pilot ETS launched sequentially in Shenzhen, Shanghai, and Beijing."),
            2015: ("在巴黎气候大会承诺争取2030年前碳达峰。", "Committed at Paris Agreement to peak carbon emissions before 2030."),
            2017: ("《全国碳排放权交易市场建设方案》印发，启动全国市场建设。", "National ETS construction plan issued, initiating the market framework."),
            2020: ("联合国大会宣布'3060'双碳目标。", "Announced '3060' dual carbon goals at the UN General Assembly."),
            2021: ("全国碳市场正式上线，首批纳入发电行业，成为全球最大碳市场。", "National ETS officially launched for the power sector, becoming the world's largest."),
            2023: ("推进第二履约周期，研究纳入石化、钢铁等高耗能行业。", "Advanced 2nd compliance period, researching expansion to high-emission sectors."),
            2024: ("重启CCER；首部行政法规发布；明确钢铁、水泥、铝冶炼纳入全国碳市场。", "CCER restarted; First ETS regulation issued; steel, cement & aluminum included."),
            2025: ("全国碳市场实现八大高耗能行业全覆盖，交易机制趋于成熟。", "National ETS covers all 8 major energy-intensive sectors."),
            2030: ("实现碳达峰。碳市场成熟，碳价有效反映减排成本。", "Carbon peak achieved. ETS matures with effective price signals."),
            2035: ("风光装机容量大幅提升，碳排放进入显著下降通道。", "Wind and solar capacity surges, emissions enter significant decline."),
            2060: ("实现碳中和。通过碳交易、CCUS及大规模碳汇抵消剩余排放。", "Carbon neutrality achieved via ETS, CCUS, and massive carbon sinks.")
        },
        "jp": {
            1997: ("COP3在京都召开通过《京都议定书》；经团连实施自愿性环保行动。", "COP3 held in Kyoto, Kyoto Protocol adopted. Keidanren launches voluntary plans."),
            2005: ("环境省开始推动'国内自愿性碳排放交易制度'。", "MOE promotes domestic voluntary emissions trading scheme."),
            2008: ("各项自愿计划整合为'国内碳排放交易整合市场'。", "Voluntary plans integrated into the domestic emissions trading market."),
            2009: ("发布《绿色经济与社会变革》政策草案。", "Draft policy for 'Green Economy and Social Change' released."),
            2011: ("福岛地震导致核电停摆，化石能源依赖增加，重新评估减排策略。", "Fukushima disaster halts nuclear power, increasing fossil fuel reliance."),
            2012: ("开始实施针对特定能源利用的配套法规。", "Implemented supporting regulations for specific energy utilization."),
            2013: ("启动了包含日元碳减排市场在内的自愿性机制。", "Launched voluntary mechanisms including the J-Credit scheme."),
            2020: ("正式提出2050年碳中和承诺，公布'绿色增长战略'。", "Officially pledged 2050 carbon neutrality; published 'Green Growth Strategy'."),
            2021: ("设定具体目标：2030年较2018年减排46%—50%。", "Set 2030 target: 46%-50% emission reduction from 2018 levels."),
            2023: ("10月正式启动GX（绿色转型）碳信用市场。", "Officially launched the GX (Green Transformation) carbon credit market."),
            2024: ("逐步完善GX联盟交易规则，企业开始强制报告并自愿交易。", "GX League rules refined; mandatory reporting with voluntary trading begins."),
            2025: ("设定2035年减排60%新目标，并计划在2028年征收碳税。", "New target: 60% reduction by 2035. Carbon tax planned for 2028."),
            2030: ("达到中期减排目标（较2018年减排46%-50%）。", "Achieved mid-term reduction target (46%-50% vs 2018)."),
            2040: ("目标较2013年减排73%，可再生能源发电占比力争50%。", "Target: 73% reduction (vs 2013); aim for 50% renewable power generation."),
            2050: ("全面实现碳中和（净零排放）。", "Comprehensive carbon neutrality (net-zero emissions) achieved."),
            2060: ("维持负碳排放以对抗气候变化。", "Maintain negative carbon emissions to combat climate change.")
        },
        "kr": {
            1997: ("签署《京都议定书》，开启国内气候变化政策研究。", "Signed Kyoto Protocol; initiated domestic climate policy research."),
            2005: ("《京都议定书》正式生效，开始逐步制定温室气体减排规划。", "Kyoto Protocol effective; began drafting GHG reduction plans."),
            2010: ("通过《低碳绿色增长基本法》，确立建立碳交易体系的法律基础。", "Passed Low Carbon Green Growth Act, establishing legal basis for ETS."),
            2012: ("通过《温室气体排放许可法》，标志亚洲首个全国性强制碳市场诞生。", "Passed GHG Emission Trading Act, establishing K-ETS legal framework."),
            2015: ("K-ETS第一阶段正式启动，以免费配额为主，涵盖电力、钢铁等。", "K-ETS Phase 1 launched (mostly free allocation) covering power, steel, etc."),
            2018: ("K-ETS第二阶段启动，设定碳排放基准并提高减排目标。", "K-ETS Phase 2: Benchmarking introduced, reduction targets increased."),
            2019: ("碳市场引入做市商和机构投资者，开启碳市场金融属性。", "Market makers and institutions introduced to boost financialization."),
            2020: ("文在寅总统提出'绿色新政'，10月正式宣布2050年实现碳中和。", "Proposed 'Green New Deal'; announced 2050 carbon neutrality target in Oct."),
            2021: ("K-ETS第三阶段启动，引入有偿竞拍；承诺2030年减排35%。", "K-ETS Phase 3: Paid auctions introduced; committed to 35% reduction by 2030."),
            2022: ("加快碳市场金融化，探索碳期货产品。", "Accelerated market financialization; exploring carbon futures."),
            2023: ("规划并逐步推出碳期货产品，以增强碳市场的避险功能。", "Rolled out carbon futures to enhance market hedging capabilities."),
            2026: ("K-ETS第四阶段，免费配额降至极低，碳价显著提升以倒逼技术升级。", "K-ETS Phase 4: Free quotas minimized; carbon prices rise to force tech upgrades."),
            2030: ("确保实现较2018年减排35%以上的承诺。", "Secured commitment of >35% emission reduction compared to 2018."),
            2050: ("实现碳中和（净零排放）目标。", "Achieved carbon neutrality (net-zero emissions)."),
            2060: ("通过CCUS等负排放技术维持净负排放，巩固碳中和成果。", "Achieved net-negative emissions via CCUS to solidify carbon neutrality.")
        },
        "sg": {
            2019: ("引入碳税机制，覆盖全国80%排放，初始税率5新元/吨。", "Introduced carbon tax ($5/t) covering 80% of national emissions."),
            2024: ("碳税大幅提升至25新元/吨，积极推动《巴黎协定》第六条双边合作。", "Tax raised to $25/t; advancing Article 6 bilateral cooperation.")
        },
        "id": {
            2023: ("启动针对燃煤电厂的强制ETS，是东南亚首个强制碳市场。", "Launched mandatory ETS for coal plants, first in SE-Asia."),
            2028: ("引入'总量上限—碳税—交易'混合机制，碳税与市场价挂钩。", "Introduced Cap-Tax-Trade hybrid mechanism linked to market prices.")
        },
        "vn": {
            2025: ("全国试点碳市场正式启动，覆盖电力、钢铁和水泥行业。", "National pilot ETS launched for power, steel, and cement."),
            2029: ("全国碳市场完成试点，正式全面运行，逐步引入拍卖机制。", "ETS pilot completed; full mandatory operation begins with auctions.")
        },
        "in": {
            2023: ("碳信用交易计划(CCTS)启动交易试点。", "CCTS trading pilot launched."),
            2026: ("CCTS首个正式履约期开始，九大工业部门全面过渡至该体系。", "CCTS first compliance period begins for 9 major industrial sectors.")
        }
    }
    
    if country not in db: return ""
    years = sorted([y for y in db[country].keys() if y <= year])
    if not years: return "前期酝酿与能力建设阶段 / Preparation phase"
    
    latest = years[-1]
    msg = db[country][latest][0] if lang == "中文" else db[country][latest][1]
    return f"【{latest}】{msg}"

# ==========================================
# 5. 绘图引擎 (终极可见度修复)
# ==========================================
def get_data(year, cbam, link, t, lang):
    nodes = []
    def add(code, name, lon, lat, color, radius):
        desc = get_detailed_history(code, year, lang)
        nodes.append({"name": name, "lon": lon, "lat": lat, "color": color, "radius": radius, "status": desc})

    # 稍微加大了所有早期的基础物理半径，让它们更像一个“国家级节点”
    cn_r = 40000 if year < 2011 else (90000 if year < 2030 else 160000)
    jp_r = 40000 if year < 2010 else (60000 if year < 2023 else 80000)
    kr_r = 40000 if year < 2015 else 60000
    sg_r = 30000 if year < 2019 else 45000
    id_r = 40000 if year < 2023 else 55000
    in_r = 40000 if year < 2023 else 60000
    vn_r = 30000 if year < 2025 else 45000

    add("cn", t["cn"], 116.4, 39.9, [255, 50, 50, 200], cn_r)
    add("jp", t["jp"], 139.6, 35.6, [50, 150, 255, 200], jp_r)
    add("kr", t["kr"], 126.9, 37.5, [50, 150, 255, 200], kr_r)
    add("sg", t["sg"], 103.8, 1.3, [50, 150, 255, 200], sg_r)
    add("id", t["id"], 106.8, -6.2, [255, 200, 50, 200], id_r)
    add("in", t["in"], 78.9, 20.5, [255, 200, 50, 200], in_r)
    add("vn", t["vn"], 105.8, 21.0, [255, 200, 50, 200], vn_r)
    
    nodes.append({"name": t["th"], "lon": 100.9, "lat": 15.8, "color": [255, 200, 50, 200], "radius": 30000 if year < 2025 else 40000, "status": "2025: 提交气候变化法案草案" if lang=="中文" else "2025: Proposed Climate Bill"})
    nodes.append({"name": t["my"], "lon": 101.9, "lat": 4.2, "color": [255, 200, 50, 200], "radius": 30000 if year < 2026 else 40000, "status": "2026: 计划征收钢铁行业碳税" if lang=="中文" else "2026: Carbon tax on steel"})
    nodes.append({"name": t["eu"], "lon": 10.0, "lat": 50.0, "color": [255, 255, 255, 50], "radius": 10000, "status": "CBAM 高压区 / Pressure Zone" if lang=="中文" else "CBAM Pressure Zone"})

    arcs = []
    if year >= 2020:
        for s in [[106.8, -6.2], [105.8, 21.0]]:
            for b in [[103.8, 1.3], [139.6, 35.6]]:
                arcs.append({"s": s, "t": b, "c": [50, 255, 120, 150]})
    if year >= 2024: arcs.append({"s": [105.8, 21.0], "t": [103.8, 1.3], "c": [0, 255, 255, 255]})
    if 2022 <= year <= 2025: arcs.append({"s": [106.8, -6.2], "t": [103.8, 1.3], "c": [255, 140, 0, 255]})
    if year >= 2027:
        for p in [[[100.9, 15.8], [101.9, 4.2]], [[101.9, 4.2], [103.8, 1.3]]]:
            arcs.append({"s": p[0], "t": p[1], "c": [180, 0, 255, 255]})
    if cbam and year >= 2025:
        for h in [[116.4, 39.9], [126.9, 37.5], [139.6, 35.6]]:
            arcs.append({"s": h, "t": [10.0, 50.0], "c": [255, 30, 30, 200]})
    if link and year >= 2016:
        c = [[116.4, 39.9], [139.6, 35.6], [126.9, 37.5]]
        for i in range(3): arcs.append({"s": c[i], "t": c[(i+1)%3], "c": [255, 215, 0, 255]})

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

dn, da = get_data(selected_year, cbam_trigger, link_trigger, t, lang)

# ==========================================
# 6. 渲染 (引入 radius_min_pixels 黑科技)
# ==========================================
st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")

col1, col2 = st.columns([1, 2.8])
with col1:
    st.subheader(f"{t['year_label']} {selected_year}")
    if selected_year < 2021: st.info(t["phase1_text"])
    elif selected_year <= 2025: st.info(t["phase2_text"])
    elif selected_year <= 2030: st.warning(t["phase3_text"])
    else: st.success(t["phase4_text"])
    if cbam_trigger and selected_year >= 2025: st.error(t["cbam_alert"])
    if link_trigger and selected_year >= 2016: st.success(t["link_alert"])

with col2:
    view = pdk.ViewState(latitude=22.0, longitude=112.0, zoom=2.7, pitch=40)
    
    # 核心修复点：加入了 radius_min_pixels=7，强行锁定在屏幕上的最小尺寸
    layers = [
        pdk.Layer("ScatterplotLayer", dn, get_position="[lon, lat]", get_color="color", get_radius="radius", radius_min_pixels=7, pickable=True, opacity=0.8),
        pdk.Layer("ArcLayer", da, get_source_position="s", get_target_position="t", get_source_color="c", get_target_color="c", get_width=4)
    ]
    
    st.pydeck_chart(pdk.Deck(
        layers=layers,
        initial_view_state=view,
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        tooltip={"html": "<b>{name}</b><br/>{status}"}
    ))

if st.session_state.is_playing: st.rerun()
