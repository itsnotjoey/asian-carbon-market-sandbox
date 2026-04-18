import streamlit as st
import pandas as pd
import pydeck as pdk

# ==========================================
# 1. 页面基本配置：开启宽屏模式与深色主题
# ==========================================
st.set_page_config(layout="wide", page_title="亚洲碳市场地缘推演 1997-2060", page_icon="🌍")

# ==========================================
# 2. 侧边栏：战略控制中心
# ==========================================
with st.sidebar:
    st.header("⚙️ 战略控制台")
    st.caption("Asian Carbon Market Sandbox V2.5")
    
    # 时间轴滑动条：覆盖你调研的 60 年史诗
    selected_year = st.slider("🕰️ 时代演进", min_value=1997, max_value=2060, value=2024, step=1)
    
    st.markdown("---")
    st.subheader("⚠️ 宏观挑战与冲击")
    cbam_trigger = st.toggle("启动欧盟 CBAM 关税制裁", value=False)
    link_trigger = st.toggle("启动东北亚碳市场链接", value=False)

    st.markdown("---")
    st.markdown("""
    **图例说明:**
    * 🔴 **主导市场**：中国 (规模随年份膨胀)
    * 🔵 **成熟市场**：日、韩、新 (绝对限额/高碳税)
    * 🟡 **新兴市场**：印尼、越南 (NbS自然碳汇供应)
    * 🟢 **绿色资金/资产流**：跨境碳信用交易
    * 🚨 **合规压力流**：受CBAM影响的碳成本外流
    """)

# ==========================================
# 3. 后台数据引擎：根据年份实时计算地图状态
# ==========================================
def get_dynamic_data(year, cbam_active, link_active):
    # --- 节点数据 (国家坐标与规模) ---
    nodes = []
    
    # 中国逻辑：2011试点 -> 2021全国 -> 2030扩容
    if year >= 2011:
        size = 30000 if year < 2021 else (80000 if year < 2030 else 150000)
        nodes.append({"name": "中国", "lon": 116.4, "lat": 39.9, "color": [255, 50, 50, 200], "radius": size})
    
    # 日本逻辑：1997探索 -> 2023正式
    if year >= 1997:
        size = 20000 if year < 2023 else 55000
        nodes.append({"name": "日本", "lon": 139.6, "lat": 35.6, "color": [50, 150, 255, 200], "radius": size})
    
    # 韩国与新加坡
    if year >= 2015: nodes.append({"name": "韩国", "lon": 126.9, "lat": 37.5, "color": [50, 150, 255, 200], "radius": 45000})
    if year >= 2019: nodes.append({"name": "新加坡", "lon": 103.8, "lat": 1.3, "color": [50, 150, 255, 200], "radius": 35000})
    
    # 东南亚新兴节点
    if year >= 2023: nodes.append({"name": "印尼", "lon": 106.8, "lat": -6.2, "color": [255, 200, 50, 200], "radius": 40000})
    if year >= 2025: nodes.append({"name": "越南", "lon": 105.8, "lat": 21.0, "color": [255, 200, 50, 200], "radius": 30000})

    # --- 飞线数据 (流动路径) ---
    arcs = []
    # 基础NbS流动：印尼 -> 新、日 (2020起)
    if year >= 2020:
        flow_color = [50, 255, 120, 200]
        arcs.append({"s": [106.8, -6.2], "t": [103.8, 1.3], "c": flow_color})
        arcs.append({"s": [106.8, -6.2], "t": [139.6, 35.6], "c": flow_color})

    # CBAM 逻辑：红色压力线飞向外部
    if cbam_active and year >= 2025:
        p_color = [255, 30, 30, 255]
        for lon, lat in [[116.4, 39.9], [105.8, 21.0], [126.9, 37.5]]:
            arcs.append({"s": [lon, lat], "t": [70.0, 50.0], "c": p_color}) # 飞向西北方向(欧洲)

    # 东北亚链接：金色三角
    if link_active and year >= 2016:
        l_color = [255, 215, 0, 255]
        arcs.append({"s": [116.4, 39.9], "t": [126.9, 37.5], "c": l_color})
        arcs.append({"s": [126.9, 37.5], "t": [139.6, 35.6], "c": l_color})
        arcs.append({"s": [139.6, 35.6], "t": [116.4, 39.9], "c": l_color})

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

# 执行计算
df_n, df_a = get_dynamic_data(selected_year, cbam