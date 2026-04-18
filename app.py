import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# ==========================================
# 1. 页面基本配置
# ==========================================
st.set_page_config(layout="wide", page_title="Asian Carbon Sandbox", page_icon="🌍")

# ==========================================
# 2. 状态初始化 (State Initialization)
# ==========================================
# 确保滑块和自动播放共享同一个‘play_year’状态
if 'play_year' not in st.session_state:
    st.session_state.play_year = 2024
if 'is_playing' not in st.session_state:
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
# 4. 侧边栏双控逻辑 (Sync Logic)
# ==========================================
with st.sidebar:
    st.header(t["sidebar_title"])
    
    # 播放控制按钮
    col_p1, col_p2 = st.columns(2)
    if col_p1.button(t["play"]): st.session_state.is_playing = True
    if col_p2.button(t["pause"]): st.session_state.is_playing = False

    # 核心同步滑块：绑定到 play_year 状态
    # 一旦用户手动拖动，session_state 也会同步更新
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
    # 节点规模随年份动态膨胀
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
    # 1. 绿色 NbS 网络
    if year >= 2020:
        flow_color = [50, 255, 120, 180]
        for s in [[106.8, -6.2], [105.8, 21.0], [101.9, 4.2]]:
            for b in [[103.8, 1.3], [139.6, 35.6], [126.9, 37.5]]:
                arcs.append({"s": s, "t": b, "c": flow_color})
    
    # 2. 特定事件线
    if year >= 2024: arcs.append({"s": [105.8, 21.0], "t": [103.8, 1.3], "c": [0, 255, 255, 255]}) # Art 6
    if 2022 <= year <= 2025: arcs.append({"s": [106.8, -6.2], "t": [103.8, 1.3], "c": [255, 140, 0, 255]}) # Export Ban
    if year >= 2027:
        grid_color = [180, 0, 255, 255] # Electric Purple Grid
        arcs.append({"s": [100.9, 15.8], "t": [101.9, 4.2], "c": grid_color})
        arcs.append({"s": [101.9, 4.2], "t": [103.8, 1.3], "c": grid_color})

    # 3. CBAM & Link 开关
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
# 7. 自动播放驱动 (Auto-Play Driver)
# ==========================================
if st.session_state.is_playing:
    if st.session_state.play_year < 2060:
        time.sleep(0.7) # 播放速度调节
        st.session_state.play_year += 1
        st.rerun()
    else:
        st.session_state.is_playing = False
