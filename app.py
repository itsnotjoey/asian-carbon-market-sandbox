import streamlit as st
import pandas as pd
import pydeck as pdk

# ==========================================
# 1. 页面基本配置
# ==========================================
st.set_page_config(layout="wide", page_title="Asian Carbon Sandbox | 亚洲碳市场沙盘", page_icon="🌍")

# ==========================================
# 2. 语言字典 (双语切换底座)
# ==========================================
with st.sidebar:
    # 中英切换核心开关
    lang = st.radio("🌐 语言 / Language", ["中文", "English"], horizontal=True)
    st.markdown("---")

# 根据选择的语言，加载不同的文本
if lang == "中文":
    t = {
        "title": "🌍 亚洲碳市场与气候地缘世纪推演 (1997-2060)",
        "subtitle": "SIPA 期末项目展示 | 研究员: Joey Wang",
        "sidebar_title": "⚙️ 战略控制台",
        "slider": "🕰️ 时代演进",
        "challenge_header": "⚠️ 宏观挑战与冲击",
        "cbam_toggle": "启动欧盟 CBAM 关税制裁",
        "link_toggle": "启动东北亚碳市场链接",
        "legend_title": "**图例说明:**",
        "legend_text": "* 🔴 **主导市场**：中国 (规模随年份膨胀)\n* 🔵 **成熟市场**：日、韩、新 (绝对限额/高碳税)\n* 🟡 **新兴市场**：印尼、越南等 (资源供应方)\n* 🟢 **绿色资产流**：NbS自然碳汇矩阵\n* 🚨 **合规压力流**：受CBAM影响的碳成本外流\n* 🟡 **战略链路**：区域市场互联互通\n* 🌐 **特定事件线**：Article 6 双边合作通道",
        "year_label": "📅 历史节点:",
        "phase1_title": "**第一阶段：早期探索期 (1997-2010)**",
        "phase1_text": "日本与韩国率先在地方层面摸索碳定价，亚洲碳市场处于碎片化萌芽状态。",
        "phase2_title": "**第二阶段：试点与强制转型 (2011-2020)**",
        "phase2_text": "中国开启7省市试点；韩国建立东亚首个全国强制市场。区域定价共识初步形成。",
        "phase3_title": "**第三阶段：巨兽苏醒与全球冲击 (2021-2030)**",
        "phase3_text": "中国全国市场启动并完成8大行业扩容。2024年新加坡与越南达成Article 6双边合作，打通跨国碳流生命线。",
        "phase4_title": "**第四阶段：净零与深度整合 (2031-2060)**",
        "phase4_text": "2050净零目标驱动能源系统彻底转型，中日韩市场链接将区域减排成本降低50%。",
        "cbam_alert": "🚨 **CBAM 冲击分析**：亚洲五大出口中心面临合规资本外流，迫使本土加速低碳技术转型以对冲碳关税。",
        "link_alert": "✨ **战略解读**：区域碳市场互联互通打破了规则碎片化，显著提升了亚洲碳资产的市场溢价。",
        # 国家名称中文
        "cn": "中国", "jp": "日本", "kr": "韩国", "sg": "新加坡", 
        "id": "印尼", "in": "印度", "vn": "越南", "th": "泰国", "my": "马来西亚", "eu": "欧洲/CBAM源"
    }
else:
    t = {
        "title": "🌍 Asian Carbon Market & Climate Geopolitics Sandbox",
        "subtitle": "SIPA Final Project | Researcher: Joey Wang",
        "sidebar_title": "⚙️ Command Center",
        "slider": "🕰️ Timeline Evolution",
        "challenge_header": "⚠️ Macro Shocks & Challenges",
        "cbam_toggle": "Activate EU CBAM Sanctions",
        "link_toggle": "Activate Northeast Asia ETS Link",
        "legend_title": "**Legend:**",
        "legend_text": "* 🔴 **Dominant Market**: China (Scale inflates over time)\n* 🔵 **Mature Markets**: JP, KR, SG (Cap & Trade / Carbon Tax)\n* 🟡 **Emerging Markets**: ID, VN, etc. (NbS Suppliers)\n* 🟢 **Green Asset Flow**: NbS / Green Energy Matrix\n* 🚨 **Compliance Flow**: CBAM-induced capital outflow\n* 🟡 **Strategic Link**: Regional ETS Interconnection\n* 🌐 **Specific Event**: Article 6 Bilateral Channel",
        "year_label": "📅 Historical Node:",
        "phase1_title": "**Phase 1: Early Exploration (1997-2010)**",
        "phase1_text": "Japan and Korea pioneered sub-national carbon pricing. Asian carbon markets were in a fragmented, nascent stage.",
        "phase2_title": "**Phase 2: Pilots & Mandatory Transition (2011-2020)**",
        "phase2_text": "China launched 7 regional pilots; Korea established East Asia's first national ETS. Regional pricing consensus began to form.",
        "phase3_title": "**Phase 3: The Behemoth & Global Shocks (2021-2030)**",
        "phase3_text": "China's national ETS launched. In 2024, Singapore & Vietnam established an Article 6 bilateral channel, pioneering cross-border compliance flows.",
        "phase4_title": "**Phase 4: Net-Zero & Deep Integration (2031-2060)**",
        "phase4_text": "Net-Zero 2050 targets drive energy transition. The C-J-K ETS link reduces regional abatement costs by 50%.",
        "cbam_alert": "🚨 **CBAM Impact Analysis**: Top 5 Asian export hubs face massive compliance capital outflows, forcing rapid domestic low-carbon transitions.",
        "link_alert": "✨ **Strategic Insight**: Regional ETS interconnection breaks regulatory fragmentation, boosting the premium of Asian carbon assets.",
        # 国家名称英文
        "cn": "China", "jp": "Japan", "kr": "South Korea", "sg": "Singapore", 
        "id": "Indonesia", "in": "India", "vn": "Vietnam", "th": "Thailand", "my": "Malaysia", "eu": "Europe (CBAM)"
    }

# ==========================================
# 3. 侧边栏控件填充
# ==========================================
with st.sidebar:
    st.header(t["sidebar_title"])
    selected_year = st.slider(t["slider"], min_value=1997, max_value=2060, value=2024, step=1)
    
    st.markdown("---")
    st.subheader(t["challenge_header"])
    cbam_trigger = st.toggle(t["cbam_toggle"], value=False)
    link_trigger = st.toggle(t["link_toggle"], value=False)

    st.markdown("---")
    st.markdown(t["legend_title"] + "\n" + t["legend_text"])

# ==========================================
# 4. 核心动态引擎 (引入双语国家名 + 特定事件线)
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
    
    # 基础绿色流动矩阵
    if year >= 2020:
        flow_color = [50, 255, 120, 180]
        suppliers = [[106.8, -6.2], [101.9, 4.2]] 
        buyers = [[103.8, 1.3], [139.6, 35.6], [126.9, 37.5]] 
        for s in suppliers:
            for b in buyers:
                arcs.append({"s": s, "t": b, "c": flow_color})
                
    # ======== 【特定年份专属事件线】 ========
    # 剧本：2024年，新加坡-越南基于 Article 6 建立了一条粗壮的双边专属通道
    if year >= 2024:
        # 使用耀眼的青色(Cyan)代表这种高质量的主权双边碳信用流动，并且线条更粗
        article6_color = [0, 255, 255, 255] 
        arcs.append({"s": [105.8, 21.0], "t": [103.8, 1.3], "c": article6_color})
    # ========================================

    # CBAM 冲击波
    if cbam_active and year >= 2025:
        p_color = [255, 30, 30, 230]
        eu_target = [10.0, 50.0]
        targets = [[116.4, 39.9], [105.8, 21.0], [126.9, 37.5], [139.6, 35.6], [78.9, 20.5]]
        for hub in targets:
            arcs.append({"s": hub, "t": eu_target, "c": p_color})

    # 东北亚连接
    if link_active and year >= 2016:
        l_color = [255, 215, 0, 255]
        core = [[116.4, 39.9], [139.6, 35.6], [126.9, 37.5]]
        arcs.append({"s": core[0], "t": core[1], "c": l_color})
        arcs.append({"s": core[1], "t": core[2], "c": l_color})
        arcs.append({"s": core[2], "t": core[0], "c": l_color})

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

df_n, df_a = get_dynamic_data(selected_year, cbam_trigger, link_trigger, t)

# ==========================================
# 5. 叙事与 UI 呈现
# ==========================================
st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")

col1, col2 = st.columns([1, 2.8])

with col1:
    st.subheader(f"{t['year_label']} {selected_year}")
    
    if selected_year < 2011:
        st.info(t["phase1_title"] + "\n\n" + t["phase1_text"])
    elif 2011 <= selected_year < 2021:
        st.info(t["phase2_title"] + "\n\n" + t["phase2_text"])
    elif 2021 <= selected_year <= 2030:
        st.warning(t["phase3_title"] + "\n\n" + t["phase3_text"])
    else:
        st.success(t["phase4_title"] + "\n\n" + t["phase4_text"])

    if cbam_trigger and selected_year >= 2025:
        st.error(t["cbam_alert"])
    
    if link_trigger and selected_year >= 2016:
        st.success(t["link_alert"])

with col2:
    view = pdk.ViewState(latitude=22.0, longitude=112.0, zoom=2.7, pitch=45)
    
    layers = []
    if not df_n.empty:
        layers.append(pdk.Layer("ScatterplotLayer", df_n, get_position="[lon, lat]", get_color="color", get_radius="radius", pickable=True, opacity=0.7))
    if not df_a.empty:
        # 特定事件线的实现：我们让线条的宽度支持动态渲染（如果在真实数据中，可以依据某列决定宽度。这里我们保持全局美观统一为 4）
        layers.append(pdk.Layer("ArcLayer", df_a, get_source_position="s", get_target_position="t", get_source_color="c", get_target_color="c", get_width=4, pickable=True))
    
    st.pydeck_chart(pdk.Deck(
        layers=layers, 
        initial_view_state=view, 
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json", 
        tooltip={"text": "{name}"}
    ))
