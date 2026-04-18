import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="亚洲碳市场地缘推演 1997-2060", page_icon="🌍")

with st.sidebar:
    st.header("⚙️ 战略控制台")
    st.caption("Asian Carbon Market Sandbox V2.5")
    selected_year = st.slider("🕰️ 时代演进", min_value=1997, max_value=2060, value=2024, step=1)
    
    st.markdown("---")
    st.subheader("⚠️ 宏观挑战与冲击")
    cbam_trigger = st.toggle("启动欧盟 CBAM 关税制裁", value=False)
    link_trigger = st.toggle("启动东北亚碳市场链接", value=False)

    st.markdown("---")
    st.markdown("**图例说明:**\n* 🔴 **主导市场**：中国 (规模随年份膨胀)\n* 🔵 **成熟市场**：日、韩、新 (绝对限额/高碳税)\n* 🟡 **新兴市场**：印尼、越南 (NbS自然碳汇供应)\n* 🟢 **绿色资金/资产流**：跨境碳信用交易\n* 🚨 **合规压力流**：受CBAM影响的碳成本外流")

def get_dynamic_data(year, cbam_active, link_active):
    nodes = []
    if year >= 2011:
        size = 30000 if year < 2021 else (80000 if year < 2030 else 150000)
        nodes.append({"name": "中国", "lon": 116.4, "lat": 39.9, "color": [255, 50, 50, 200], "radius": size})
    if year >= 1997:
        size = 20000 if year < 2023 else 55000
        nodes.append({"name": "日本", "lon": 139.6, "lat": 35.6, "color": [50, 150, 255, 200], "radius": size})
    if year >= 2015: nodes.append({"name": "韩国", "lon": 126.9, "lat": 37.5, "color": [50, 150, 255, 200], "radius": 45000})
    if year >= 2019: nodes.append({"name": "新加坡", "lon": 103.8, "lat": 1.3, "color": [50, 150, 255, 200], "radius": 35000})
    if year >= 2023: nodes.append({"name": "印尼", "lon": 106.8, "lat": -6.2, "color": [255, 200, 50, 200], "radius": 40000})
    if year >= 2025: nodes.append({"name": "越南", "lon": 105.8, "lat": 21.0, "color": [255, 200, 50, 200], "radius": 30000})

    arcs = []
    if year >= 2020:
        flow_color = [50, 255, 120, 200]
        arcs.append({"s": [106.8, -6.2], "t": [103.8, 1.3], "c": flow_color})
        arcs.append({"s": [106.8, -6.2], "t": [139.6, 35.6], "c": flow_color})
    if cbam_active and year >= 2025:
        p_color = [255, 30, 30, 255]
        for lon, lat in [[116.4, 39.9], [105.8, 21.0], [126.9, 37.5]]:
            arcs.append({"s": [lon, lat], "t": [70.0, 50.0], "c": p_color})
    if link_active and year >= 2016:
        l_color = [255, 215, 0, 255]
        arcs.append({"s": [116.4, 39.9], "t": [126.9, 37.5], "c": l_color})
        arcs.append({"s": [126.9, 37.5], "t": [139.6, 35.6], "c": l_color})
        arcs.append({"s": [139.6, 35.6], "t": [116.4, 39.9], "c": l_color})

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

df_n, df_a = get_dynamic_data(selected_year, cbam_trigger, link_trigger)

st.title("🌍 亚洲碳市场与气候地缘世纪推演")
st.markdown("**SIPA 期末项目展示 | 研究员: Joey Wang**")

col1, col2 = st.columns([1, 2.5])

with col1:
    st.subheader(f"📅 历史节点: {selected_year} 年")
    if selected_year < 2011:
        st.info("**第一阶段：早期探索期**\n\n日本与韩国率先在地方层面摸索碳定价，亚洲碳市场处于碎片化萌芽状态。")
    elif 2011 <= selected_year < 2021:
        st.info("**第二阶段：试点与强制转型**\n\n中国开启7省市试点；韩国建立东亚首个全国强制市场。区域定价共识初步形成。")
    elif 2021 <= selected_year <= 2030:
        st.warning("**第三阶段：巨兽苏醒与全球冲击**\n\n中国全国市场启动并完成8大行业扩容，覆盖百亿吨排放。东南亚自然资产因本土NDC目标面临出口博弈。")
    else:
        st.success("**第四阶段：净零与深度整合**\n\n2050净零目标驱动能源系统彻底转型，中日韩市场链接将区域减排成本降低50%。")

    if cbam_trigger and selected_year >= 2025:
        st.error("🚨 **CBAM 冲击分析**：由于出口高碳产品，受灾国家正面临合规资本外流，本土碳价必须加速与国际对齐。")

with col2:
    view = pdk.ViewState(latitude=22.0, longitude=115.0, zoom=2.8, pitch=45)
    layers = []
    
    # 修复白屏的核心逻辑：加上这两道护盾，只有里面真有数据时，才画图层
    if not df_n.empty:
        layers.append(pdk.Layer("ScatterplotLayer", df_n, get_position="[lon, lat]", get_color="color", get_radius="radius", pickable=True, opacity=0.7))
    if not df_a.empty:
        layers.append(pdk.Layer("ArcLayer", df_a, get_source_position="s", get_target_position="t", get_source_color="c", get_target_color="c", get_width=4, pickable=True))
    
    st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view, map_style="mapbox://styles/mapbox/dark-v10", tooltip={"text": "{name}"}))
