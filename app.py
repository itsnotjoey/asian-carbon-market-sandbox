import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# ==========================================
# 1. 页面基本配置
# ==========================================
st.set_page_config(layout="wide", page_title="Asian Carbon Sandbox", page_icon="🌍")

# ==========================================
# 2. 状态初始化 & 顶层播放引擎
# ==========================================
if 'play_year' not in st.session_state:
    st.session_state.play_year = 1997
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

if st.session_state.is_playing:
    time.sleep(0.8) # 播放速度调节
    if st.session_state.play_year < 2060:
        st.session_state.play_year += 1
    else:
        st.session_state.is_playing = False

# ==========================================
# 3. 语言字典
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
        "legend_text": "* 🔴 **主导市场**：中国\n* 🔵 **成熟市场**：日、韩、新\n* 🟡 **新兴市场**：印尼、越南、印度等\n* 🟢 **绿色资产流**：NbS自然碳汇矩阵\n* 🚨 **合规压力流**：受CBAM影响的碳成本外流\n* 🟡 **战略链路**：区域市场互联互通\n* 🌐 **特定事件**：Article 6 合作/跨境电网",
        "year_label": "📅 历史节点:",
        "phase1_text": "第一阶段：早期探索期 (1997-2010)",
        "phase2_text": "第二阶段：试点与强制转型 (2011-2020)",
        "phase3_text": "第三阶段：巨兽苏醒与全球冲击 (2021-2030)",
        "phase4_text": "第四阶段：净零与深度整合 (2031-2060)",
        "cbam_alert": "🚨 **CBAM 冲击分析**：亚洲出口中心正面临合规资本外流压力。",
        "link_alert": "✨ **战略解读**：区域互联显著提升了亚洲碳资产的市场溢价。",
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
        "cbam_toggle": "Activate EU CBAM Sanctions",
        "link_toggle": "Activate Northeast Asia Link",
        "legend_title": "**Legend:**",
        "legend_text": "* 🔴 **Dominant**: China\n* 🔵 **Mature**: JP, KR, SG\n* 🟡 **Emerging**: ID, VN, IN\n* 🟢 **Green Flow**: NbS / Asset Matrix\n* 🚨 **Compliance**: CBAM-induced outflow\n* 🟡 **Link**: ETS Interconnection\n* 🌐 **Events**: Article 6 / Cross-border Grid",
        "year_label": "📅 Year:",
        "phase1_text": "Phase 1: Early Exploration (1997-2010)",
        "phase2_text": "Phase 2: Pilots & Transition (2011-2020)",
        "phase3_text": "Phase 3: The Behemoth (2021-2030)",
        "phase4_text": "Phase 4: Net-Zero Integration (2031-2060)",
        "cbam_alert": "🚨 **CBAM Impact**: Export hubs facing compliance capital outflows.",
        "link_alert": "✨ **Strategic**: Integration boosts the premium of Asian carbon assets.",
        "cn": "China", "jp": "Japan", "kr": "S.Korea", "sg": "Singapore", "id": "Indonesia", "in": "India", "vn": "Vietnam", "th": "Thailand", "my": "Malaysia", "eu": "Europe/CBAM"
    }

# ==========================================
# 4. 侧边栏交互
# ==========================================
with st.sidebar:
    st.header(t["sidebar_title"])
    col_p1, col_p2 = st.columns(2)
    if col_p1.button(t["play"]): 
        st.session_state.is_playing = True
        st.rerun()
    if col_p2.button(t["pause"]): 
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
# 5. 国家历史事件数据库 (Dynamic Tooltip Engine)
# ==========================================
def get_country_status(country_code, current_year, lang):
    # 此处浓缩了你查阅的所有核心文献数据
    history = {
        "cn": {
            1997: ("尚未启动市场机制", "No market mechanism"),
            2011: ("批准7省市开展碳交易试点", "Approved 7 regional ETS pilots"),
            2013: ("地方试点正式开市(相对限额)", "Regional pilots officially launched"),
            2021: ("启动全国碳市场(电力行业)", "National ETS launched (Power sector)"),
            2024: ("重启CCER，扩容至8大行业", "CCER restarted, expansion to 8 sectors"),
            2027: ("引入拍卖机制，关注绝对减排", "Auctioning introduced, focus on absolute caps"),
            2030: ("扩容完成，转为绝对总量上限", "Expansion complete, hard cap implemented"),
            2060: ("达成碳中和", "Carbon Neutrality achieved")
        },
        "jp": {
            1997: ("允许自愿碳额度抵消", "Voluntary carbon offsets allowed"),
            2010: ("东京都启动亚洲首个强制ETS", "Tokyo launches Asia's first city-level ETS"),
            2023: ("启动全国GX-ETS(自愿参与)", "GX-ETS launched (Voluntary phase)"),
            2026: ("GX-ETS转为强制履约", "GX-ETS becomes mandatory"),
            2028: ("引入GX附加费", "GX Surcharge introduced"),
            2033: ("电力行业强制配额拍卖", "Mandatory power sector auctions")
        },
        "kr": {
            1997: ("前期酝酿阶段", "Preparation phase"),
            2010: ("颁布《低碳绿色增长基本法》", "Low Carbon Green Growth Act enacted"),
            2015: ("启动东亚首个全国强制K-ETS", "Launched East Asia's first national K-ETS"),
            2026: ("第四版计划: 引入碳差额合约(CCfD)", "Phase 4: CCfD mechanism introduced")
        },
        "sg": {
            1997: ("前期酝酿阶段", "Preparation phase"),
            2019: ("引入碳税机制 (5新元/吨)", "Carbon tax introduced ($5 SGD/t)"),
            2024: ("碳税提至25新元，推进Art 6双边合作", "Tax raised to $25 SGD, Art 6 deals advanced")
        },
        "id": {
            1997: ("NbS自然碳汇初步发展", "Early NbS development"),
            2023: ("启动燃煤电厂强制ETS", "Mandatory ETS for coal plants launched"),
            2025: ("ETS扩容至燃油/燃气电厂", "ETS expanded to oil/gas plants"),
            2028: ("引入'上限-碳税-交易'混合机制", "Cap-Tax-Trade hybrid mechanism introduced")
        },
        "vn": {
            1997: ("前期酝酿阶段", "Preparation phase"),
            2025: ("全国试点碳市场启动", "National pilot ETS launched"),
            2029: ("碳市场全面强制运行", "Carbon market fully operational")
        },
        "in": {
            1997: ("前期酝酿阶段", "Preparation phase"),
            2023: ("碳信用交易计划(CCTS)启动试点", "CCTS pilot launched"),
            2026: ("CCTS首个正式履约期开始", "CCTS first compliance period begins")
        }
    }
    
    if country_code not in history:
        return "数据收集中 / Data compiling..."
        
    # 核心逻辑：找出小于等于当前年份的【最新】事件
    past_years = [y for y in history[country_code].keys() if y <= current_year]
    if not past_years:
        return "酝酿中 / Developing"
        
    latest_year = max(past_years)
    # 根据语言返回中文[0]或英文[1]
    event_text = history[country_code][latest_year][0] if lang == "中文" else history[country_code][latest_year][1]
    
    return f"📍 {latest_year}: {event_text}"

# ==========================================
# 6. 数据引擎 (注入 Tooltip 数据)
# ==========================================
def get_dynamic_data(year, cbam_active, link_active, t, lang):
    nodes = []
    
    def add_node(code, name, lon, lat, color, size):
        status = get_country_status(code, year, lang)
        nodes.append({"name": name, "lon": lon, "lat": lat, "color": color, "radius": size, "status": status})

    # 规模计算逻辑
    cn_size = 35000 if year < 2021 else (85000 if year < 2030 else 160000)
    jp_size = 20000 if year < 2023 else 55000

    if year >= 2011: add_node("cn", t["cn"], 116.4, 39.9, [255, 50, 50, 200], cn_size)
    if year >= 1997: add_node("jp", t["jp"], 139.6, 35.6, [50, 150, 255, 200], jp_size)
    if year >= 2015: add_node("kr", t["kr"], 126.9, 37.5, [50, 150, 255, 200], 45000)
    if year >= 2019: add_node("sg", t["sg"], 103.8, 1.3, [50, 150, 255, 200], 35000)
    
    if year >= 2023: 
        add_node("id", t["id"], 106.8, -6.2, [255, 200, 50, 200], 45000)
        add_node("in", t["in"], 78.9, 20.5, [255, 200, 50, 200], 50000)
    if year >= 2025: 
        add_node("vn", t["vn"], 105.8, 21.0, [255, 200, 50, 200], 30000)
        # 泰国马来由于历史事件较少，用占位符
        nodes.append({"name": t["th"], "lon": 100.9, "lat": 15.8, "color": [255, 200, 50, 200], "radius": 28000, "status": "2025: 拟议气候变化法案"})
        nodes.append({"name": t["my"], "lon": 101.9, "lat": 4.2, "color": [255, 200, 50, 200], "radius": 28000, "status": "2026: 钢铁能源行业碳税计划"})

    # 外部目标点
    nodes.append({"name": t["eu"], "lon": 10.0, "lat": 50.0, "color": [255, 255, 255, 50], "radius": 10000, "status": "CBAM 碳关税高压区" if lang=="中文" else "CBAM Pressure Zone"})

    arcs = []
    if year >= 2020:
        flow_color = [50, 255, 120, 180]
        for s in [[106.8, -6.2], [105.8, 21.0], [101.9, 4.2]]:
            for b in [[103.8, 1.3], [139.6, 35.6], [126.9, 37.5]]:
                arcs.append({"s": s, "t": b, "c": flow_color})
    
    if year >= 2024: arcs.append({"s": [105.8, 21.0], "t": [103.8, 1.3], "c": [0, 255, 255, 255]})
    if 2022 <= year <= 2025: arcs.append({"s": [106.8, -6.2], "t": [103.8, 1.3], "c": [255, 140, 0, 255]})
    if year >= 2027:
        grid_color = [180, 0, 255, 255]
        arcs.append({"s": [100.9, 15.8], "t": [101.9, 4.2], "c": grid_color})
        arcs.append({"s": [101.9, 4.2], "t": [103.8, 1.3], "c": grid_color})

    if cbam_active and year >= 2025:
        p_color = [255, 30, 30, 230]
        for h in [[116.4, 39.9], [105.8, 21.0], [126.9, 37.5], [139.6, 35.6], [78.9, 20.5]]:
            arcs.append({"s": h, "t": [10.0, 50.0], "c": p_color})
    if link_active and year >= 2016:
        l_color = [255, 215, 0, 255]
        core = [[116.4, 39.9], [139.6, 35.6], [126.9, 37.5]]
        arcs.append({"s": core[0], "t": core[1], "c": l_color})
        arcs.append({"s": core[1], "t": core[2], "c": l_color})
        arcs.append({"s": core[2], "t": core[0], "c": l_color})

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

df_n, df_a = get_dynamic_data(selected_year, cbam_trigger, link_trigger, t, lang)

# ==========================================
# 7. UI 呈现
# ==========================================
st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")

c1, c2 = st.columns([1, 2.8])
with c1:
    st.subheader(f"{t['year_label']} {selected_year}")
    if selected_year < 2011: st.info(t["phase1_text"])
    elif 2011 <= selected_year < 2021: st.info(t["phase2_text"])
    elif 2021 <= selected_year <= 2030: st.warning(t["phase3_text"])
    else: st.success(t["phase4_text"])
    if cbam_trigger and selected_year >= 2025: st.error(t["cbam_alert"])
    if link_trigger and selected_year >= 2016: st.success(t["link_alert"])

with c2:
    view = pdk.ViewState(latitude=22.0, longitude=112.0, zoom=2.7, pitch=45)
    layers = []
    if not df_n.empty:
        layers.append(pdk.Layer(
            "ScatterplotLayer", 
            df_n, 
            get_position="[lon, lat]", 
            get_color="color", 
            get_radius="radius", 
            pickable=True, 
            opacity=0.7
        ))
    if not df_a.empty:
        layers.append(pdk.Layer(
            "ArcLayer", 
            df_a, 
            get_source_position="s", 
            get_target_position="t", 
            get_source_color="c", 
            get_target_color="c", 
            get_width=4, 
            pickable=True
        ))
    
    # 【黑科技】使用 HTML 渲染高颜值的 Tooltip
    tooltip_html = """
    <div style="font-family: Arial, sans-serif; font-size: 14px;">
        <b style="color: #4CAF50; font-size: 16px;">{name}</b><br/>
        <span style="color: #ECEFF1;">{status}</span>
    </div>
    """
    
    st.pydeck_chart(pdk.Deck(
        layers=layers, 
        initial_view_state=view, 
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json", 
        tooltip={"html": tooltip_html}
    ))

# 循环收尾
if st.session_state.is_playing:
    st.rerun()        "subtitle": "SIPA 期末项目展示 | 研究员: Joey Wang",
        "sidebar_title": "⚙️ 战略控制台",
        "slider": "🕰️ 时代演进",
        "play": "▶️ 播放", "pause": "⏸️ 暂停",
        "challenge_header": "⚠️ 宏观挑战与冲击",
        "cbam_toggle": "启动欧盟 CBAM 关税制裁",
        "link_toggle": "启动东北亚碳市场链接",
        "legend_title": "**图例说明:**",
        "legend_text": "* 🔴 **主导市场**：中国\n* 🔵 **成熟市场**：日、韩、新\n* 🟡 **新兴市场**：印尼、越南、印度等\n* 🟢 **绿色资产流**：NbS自然碳汇矩阵\n* 🚨 **合规压力流**：受CBAM影响的碳成本外流\n* 🟡 **战略链路**：区域市场互联互通\n* 🌐 **特定事件**：Article 6 合作/跨境电网",
        "year_label": "📅 历史节点:",
        "phase1_text": "第一阶段：早期探索期 (1997-2010)",
        "phase2_text": "第二阶段：试点与强制转型 (2011-2020)",
        "phase3_text": "第三阶段：巨兽苏醒与全球冲击 (2021-2030)",
        "phase4_text": "第四阶段：净零与深度整合 (2031-2060)",
        "cbam_alert": "🚨 **CBAM 冲击分析**：亚洲出口中心正面临合规资本外流压力。",
        "link_alert": "✨ **战略解读**：区域互联显著提升了亚洲碳资产的市场溢价。",
        "cn": "中国", "jp": "日本", "kr": "韩国", "sg": "新加坡", "id": "印尼", "in": "印度", "vn": "越南", "th": "泰国", "my": "马来西亚", "eu": "欧洲"
    }
else:
    t = {
        "title": "🌍 Asian Carbon Market & Climate Geopolitics Sandbox",
        "subtitle": "SIPA Final Project | Researcher: Joey Wang",
        "sidebar_title": "⚙️ Command Center",
        "slider": "🕰️ Timeline Evolution",
        "play": "▶️ Play", "pause": "Pause",
        "challenge_header": "⚠️ Macro Shocks",
        "cbam_toggle": "Activate EU CBAM Sanctions",
        "link_toggle": "Activate Northeast Asia Link",
        "legend_title": "**Legend:**",
        "legend_text": "* 🔴 **Dominant**: China\n* 🔵 **Mature**: JP, KR, SG\n* 🟡 **Emerging**: ID, VN, IN\n* 🟢 **Green Flow**: NbS / Asset Matrix\n* 🚨 **Compliance**: CBAM-induced outflow\n* 🟡 **Link**: ETS Interconnection\n* 🌐 **Events**: Article 6 / Cross-border Grid",
        "year_label": "📅 Year:",
        "phase1_text": "Phase 1: Early Exploration (1997-2010)",
        "phase2_text": "Phase 2: Pilots & Transition (2011-2020)",
        "phase3_text": "Phase 3: The Behemoth (2021-2030)",
        "phase4_text": "Phase 4: Net-Zero Integration (2031-2060)",
        "cbam_alert": "🚨 **CBAM Impact**: Export hubs facing compliance capital outflows.",
        "link_alert": "✨ **Strategic**: Integration boosts the premium of Asian carbon assets.",
        "cn": "China", "jp": "Japan", "kr": "S.Korea", "sg": "Singapore", "id": "Indonesia", "in": "India", "vn": "Vietnam", "th": "Thailand", "my": "Malaysia", "eu": "Europe"
    }

# ==========================================
# 4. 侧边栏交互 (画出界面)
# ==========================================
with st.sidebar:
    st.header(t["sidebar_title"])
    
    col_p1, col_p2 = st.columns(2)
    if col_p1.button(t["play"]): 
        st.session_state.is_playing = True
        st.rerun() # 按钮点下后，立刻重新从头跑代码，触发顶部的 +1 逻辑
    if col_p2.button(t["pause"]): 
        st.session_state.is_playing = False
        st.rerun()

    # 滑块现在安全了，它只会读取顶部已经算好的年份
    selected_year = st.slider(t["slider"], 1997, 2060, key="play_year")
    
    st.markdown("---")
    st.subheader(t["challenge_header"])
    cbam_trigger = st.toggle(t["cbam_toggle"], value=False)
    link_trigger = st.toggle(t["link_toggle"], value=False)
    st.markdown("---")
    st.markdown(t["legend_title"] + "\n" + t["legend_text"])

# ==========================================
# 5. 数据引擎
# ==========================================
def get_dynamic_data(year, cbam_active, link_active, t):
    nodes = []
    if year >= 2011:
        size = 35000 if year < 2021 else (85000 if year < 2030 else 160000)
        nodes.append({"name": t["cn"], "lon": 116.4, "lat": 39.9, "color": [255, 50, 50, 200], "radius": size})
    if year >= 1997:
        size = 20000 if year < 2023 else 55000
        nodes.append({"name": t["jp"], "lon": 139.6, "lat": 35.6, "color": [50, 150, 255, 200], "radius": size})
    if year >= 2015: nodes.append({"name": t["kr"], "lon": 126.9, "lat": 37.5, "color": [50, 150, 255, 200], "radius": 45000})
    if year >= 2019: nodes.append({"name": t["sg"], "lon": 103.8, "lat": 1.3, "color": [50, 150, 255, 200], "radius": 35000})
    if year >= 2023: 
        nodes.append({"name": t["id"], "lon": 106.8, "lat": -6.2, "color": [255, 200, 50, 200], "radius": 45000})
        nodes.append({"name": t["in"], "lon": 78.9, "lat": 20.5, "color": [255, 200, 50, 200], "radius": 50000})
    if year >= 2025: 
        nodes.append({"name": t["vn"], "lon": 105.8, "lat": 21.0, "color": [255, 200, 50, 200], "radius": 30000})
        nodes.append({"name": t["th"], "lon": 100.9, "lat": 15.8, "color": [255, 200, 50, 200], "radius": 28000})
        nodes.append({"name": t["my"], "lon": 101.9, "lat": 4.2, "color": [255, 200, 50, 200], "radius": 28000})
    nodes.append({"name": t["eu"], "lon": 10.0, "lat": 50.0, "color": [255, 255, 255, 50], "radius": 10000})

    arcs = []
    if year >= 2020:
        flow_color = [50, 255, 120, 180]
        for s in [[106.8, -6.2], [105.8, 21.0], [101.9, 4.2]]:
            for b in [[103.8, 1.3], [139.6, 35.6], [126.9, 37.5]]:
                arcs.append({"s": s, "t": b, "c": flow_color})
    
    if year >= 2024: arcs.append({"s": [105.8, 21.0], "t": [103.8, 1.3], "c": [0, 255, 255, 255]})
    if 2022 <= year <= 2025: arcs.append({"s": [106.8, -6.2], "t": [103.8, 1.3], "c": [255, 140, 0, 255]})
    if year >= 2027:
        grid_color = [180, 0, 255, 255]
        arcs.append({"s": [100.9, 15.8], "t": [101.9, 4.2], "c": grid_color})
        arcs.append({"s": [101.9, 4.2], "t": [103.8, 1.3], "c": grid_color})

    if cbam_active and year >= 2025:
        p_color = [255, 30, 30, 230]
        for h in [[116.4, 39.9], [105.8, 21.0], [126.9, 37.5], [139.6, 35.6], [78.9, 20.5]]:
            arcs.append({"s": h, "t": [10.0, 50.0], "c": p_color})
    if link_active and year >= 2016:
        l_color = [255, 215, 0, 255]
        core = [[116.4, 39.9], [139.6, 35.6], [126.9, 37.5]]
        arcs.append({"s": core[0], "t": core[1], "c": l_color})
        arcs.append({"s": core[1], "t": core[2], "c": l_color})
        arcs.append({"s": core[2], "t": core[0], "c": l_color})

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

df_n, df_a = get_dynamic_data(selected_year, cbam_trigger, link_trigger, t)

# ==========================================
# 6. UI 呈现
# ==========================================
st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")

c1, c2 = st.columns([1, 2.8])
with c1:
    st.subheader(f"{t['year_label']} {selected_year}")
    if selected_year < 2011: st.info(t["phase1_text"])
    elif 2011 <= selected_year < 2021: st.info(t["phase2_text"])
    elif 2021 <= selected_year <= 2030: st.warning(t["phase3_text"])
    else: st.success(t["phase4_text"])
    if cbam_trigger and selected_year >= 2025: st.error(t["cbam_alert"])
    if link_trigger and selected_year >= 2016: st.success(t["link_alert"])

with c2:
    view = pdk.ViewState(latitude=22.0, longitude=112.0, zoom=2.7, pitch=45)
    layers = []
    if not df_n.empty:
        layers.append(pdk.Layer("ScatterplotLayer", df_n, get_position="[lon, lat]", get_color="color", get_radius="radius", pickable=True, opacity=0.7))
    if not df_a.empty:
        layers.append(pdk.Layer("ArcLayer", df_a, get_source_position="s", get_target_position="t", get_source_color="c", get_target_color="c", get_width=4, pickable=True))
    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view, map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json", tooltip={"text": "{name}"}))

# ==========================================
# 7. 循环收尾：如果正在播放，告诉服务器马上再跑一次
# ==========================================
if st.session_state.is_playing:
    st.rerun()
