import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import streamlit.components.v1 as components

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
        "subtitle": "亚洲能源安全 期末项目展示 | 面向气候投资与跨国战略决策",
        "sidebar_title": "⚙️ 战略控制台",
        "slider": "🕰️ 时代演进",
        "play": "▶️ 播放", "pause": "⏸️ 暂停",
        "challenge_header": "⚠️ 宏观挑战与冲击",
        "cbam_toggle": "启动欧盟 CBAM 关税制裁",
        "link_toggle": "启动东北亚碳市场链接",
        "legend_title": "**图例与动态资金流:**",
        "legend_text": "**【国家与区域节点】**\n* 🔴 **主导市场**：中国\n* 🔵 **成熟市场**：日、韩、新\n* 🟡 **新兴市场**：东盟与印度\n* 🟣 **中东枢纽**：沙特、阿联酋\n\n**【时间轴动态连线】**\n* 🟢 **绿色连线 (2020起)**：东南亚自然碳汇(NbS)出口\n* 🟠 **橙色连线 (2022-2025)**：印尼碳出口限制与贸易壁垒\n* 💖 **粉色大动脉 (2023起)**：中东主权资金投资亚洲气候资产\n* 🌐 **青色连线 (2024起)**：新越 Article 6 双边通道\n* ⚡ **紫色连线 (2027起)**：跨国物理绿电网\n\n**【手动开关触发】**\n* 🚨 **红色射线**：CBAM 碳合规成本倒灌\n* 🟡 **金色链路**：东北亚碳市场互联互通",
        "year_label": "📅 历史节点:",
        "phase1_text": "第一阶段：早期探索与地方试点 (1997—2020)",
        "phase2_text": "第二阶段：全国强制市场建立与快速扩张 (2021—2025)",
        "phase3_text": "第三阶段：强制履约深化与扩容 (2026—2030)",
        "phase4_text": "第四阶段：深度脱碳、区域一体化与净零 (2031—2060)",
        "cbam_alert": "🚨 **CBAM 冲击**：亚洲主要出口国面临碳成本倒灌。",
        "link_alert": "✨ **战略互联**：区域互联提升亚洲碳资产定价权。",
       "cn": "中国", "jp": "日本", "kr": "韩国", "sg": "新加坡", "id": "印尼", "in": "印度", "vn": "越南", "th": "泰国", "my": "马来西亚", "eu": "欧洲/CBAM", "me": "中东(沙特/UAE)",
        "au": "澳大利亚", "kpi_title": "📊 宏观量化指标预估", "kpi_1": "区域碳市场覆盖量", "kpi_2": "亚洲平均碳价基准"
    }
else:
    t = {
        "title": "🌍 Asian Carbon Market & Climate Geopolitics Sandbox",
        "subtitle": "Asian Energy Security Final Project | Strategic Briefing",
        "sidebar_title": "⚙️ Command Center",
        "slider": "🕰️ Timeline Evolution",
        "play": "▶️ Play", "pause": "Pause",
        "challenge_header": "⚠️ Macro Shocks",
        "cbam_toggle": "Activate EU CBAM",
        "link_toggle": "Activate NE-Asia Link",
        "legend_title": "**Legend & Dynamic Flows:**",
        "legend_text": "**[ Regional Nodes ]**\n* 🔴 **Dominant**: China\n* 🔵 **Mature**: JP, KR, SG\n* 🟡 **Emerging**: ASEAN & India\n* 🟣 **ME Hub**: Saudi Arabia, UAE\n\n**[ Timeline-Triggered Lines ]**\n* 🟢 **Green Lines (2020+)**: SE Asia NbS carbon exports\n* 🟠 **Orange Lines (2022-2025)**: Indonesia carbon export ban\n* 💖 **Pink Artery (2023+)**: ME sovereign wealth flowing to Asian climate assets\n* 🌐 **Cyan Lines (2024+)**: SG-VN Article 6 flow\n* ⚡ **Purple Lines (2027+)**: ASEAN cross-border green grid\n\n**[ Toggle-Triggered Lines ]**\n* 🚨 **Red Lines**: CBAM compliance cost outflow\n* 🟡 **Gold Lines**: Northeast Asia ETS interconnection",
        "year_label": "📅 Year:",
        "phase1_text": "Phase 1: Early Exploration (1997-2020)",
        "phase2_text": "Phase 2: National Expansion (2021-2025)",
        "phase3_text": "Phase 3: Deep Compliance (2026-2030)",
        "phase4_text": "Phase 4: Net-Zero Integration (2031-2060)",
        "cbam_alert": "🚨 **CBAM Insight**: Exporters face domestic carbon cost backflow.",
        "link_alert": "✨ **Strategic**: Regional integration boosts carbon premium.",
        "cn": "China", "jp": "Japan", "kr": "S.Korea", "sg": "Singapore", "id": "Indonesia", "in": "India", "vn": "Vietnam", "th": "Thailand", "my": "Malaysia", "eu": "Europe", "me": "Middle East",
        "au": "Australia", "kpi_title": "📊 Macro Quantitative Projections", "kpi_1": "Regional ETS Coverage", "kpi_2": "Avg Carbon Price Benchmark"
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
            1997: ("签署《京都议定书》，开始关注气候变化与碳排放。", "Signed Kyoto Protocol; began focusing on climate change."),
            2006: ("发布《国家气候变化战略》，明确低碳发展方向。", "Released National Climate Change Strategy for low-carbon development."),
            2012: ("启动排放监测和报告(MRV)框架，为碳交易铺路。", "Launched emissions MRV framework, paving the way for carbon pricing."),
            2017: ("宣布将在2019年施行碳税，成为亚洲首个实施碳税的国家。", "Announced carbon tax for 2019, becoming the first in Asia."),
            2019: ("正式实施碳税(5新元/吨)，覆盖年度排放达2.5万吨的设施。", "Implemented carbon tax ($5/t) for facilities >25,000t CO2e."),
            2021: ("发布'新加坡2030绿色发展蓝图'，明确减碳路径。", "Launched Singapore Green Plan 2030, clarifying decarbonization path."),
            2022: ("宣布大幅提高碳税：2024年增至25新元，2030年目标50-80新元。", "Announced steep tax hike: $25 by 2024, aiming for $50-$80 by 2030."),
            2024: ("新碳税(25新元)生效，允许使用高质量碳权抵消最高5%排放。", "New tax ($25) effective; allows high-quality offsets for up to 5% emissions."),
            2025: ("成功举办首场高标准碳权拍卖，吸引超10亿美金投标，确立枢纽地位。", "Held high-standard carbon auction (~$1B USD bids), securing hub status."),
            2030: ("实现碳排放达峰，较正常水平减少约31.89%-43.2%。", "Emissions peak achieved; reduced ~31.89%-43.2% from BAU."),
            2050: ("实现国家净零排放(Net-Zero)承诺。", "Achieved national net-zero emissions commitment."),
            2060: ("维持碳中和愿景，相关法规深度融入国家长期发展战略。", "Maintained carbon neutrality, deeply integrated into long-term strategy.")
        },
        "id": {
            1997: ("泥炭地大火引发全球对印尼土地利用(LULUCF)碳排放的关注。", "Peatland fires drew global attention to Indonesia's LULUCF carbon emissions."),
            2007: ("举办COP13通过《巴厘路线图》，奠定林业减碳国际地位。", "Hosted COP13 (Bali Action Plan), securing international status in forestry decarbonization."),
            2010: ("与挪威签署10亿美元REDD+备忘录，通过保护森林获取碳汇资金。", "Signed $1B REDD+ MoU with Norway to secure carbon funds by protecting forests."),
            2015: ("签署《巴黎协定》并提交国家自主贡献(NDC)减排目标。", "Signed Paris Agreement and submitted NDC reduction targets."),
            2021: ("颁布总统第98号条例确立碳经济价值；承诺2060净零排放。", "Issued PR 98/2021 on Carbon Economic Value; pledged Net Zero by 2060."),
            2022: ("提出JETP寻求资金退役煤电；因通胀推迟原定征收的碳税。", "Proposed JETP to retire coal; carbon tax delayed due to inflation."),
            2023: ("9月正式启动首个本土碳交易所(IDXCarbon)，首批为林业碳信用。", "Launched IDXCarbon in Sept, with forestry credits as initial trades."),
            2025: ("印尼碳交易所正式对外国投资者开放；碳税计划预期重启。", "IDXCarbon opens to foreign investors; carbon tax expected to resume."),
            2030: ("工业、能源和交通部门全面纳入配额交易体系。", "Industry, energy, and transport sectors fully integrated into ETS."),
            2050: ("目标实现电力部门碳中和。", "Target to achieve carbon neutrality in the power sector."),
            2060: ("依托ETS、森林碳汇及CCS技术实现全面净零排放。", "Achieve Net Zero through ETS, forestry sinks, and CCS technology.")
        },
        "vn": {
            1997: ("签署《京都议定书》，开始寻求国际碳资金合作的可能性。", "Signed Kyoto Protocol; sought international carbon finance cooperation."),
            2005: ("积极利用CDM机制，在能源等领域开发项目并出售CERs。", "Actively utilized CDM, developing energy projects and selling CERs."),
            2015: ("签署《巴黎协定》，承诺自主减排。", "Signed Paris Agreement, committing to self-determined emission reductions."),
            2020: ("修订《环境保护法》，确立建立ETS和碳信用市场的法律基础。", "Revised Environmental Protection Law, establishing legal basis for ETS."),
            2022: ("颁布06/2022/ND-CP决议，确立碳定价框架及ETS时间表。", "Issued Decree 06/2022/ND-CP, establishing carbon pricing framework and ETS timeline."),
            2024: ("确立碳盘查与报告合规要求，高碳排企业须年度报送。", "Established MRV compliance; high-emission enterprises must submit annual reports."),
            2025: ("启动国家ETS试点运行，纳入水泥、钢铁、火电等重点行业。", "Launch pilot national ETS, incorporating cement, steel, and thermal power."),
            2026: ("基于试点数据优化配额分配，尝试引入拍卖机制。", "Optimize quota allocation based on pilot data; introduce auctioning mechanism."),
            2027: ("正式实施碳交易市场，纳入更多高耗能企业。", "Officially implement carbon market, expanding to more energy-intensive enterprises.")
        },
        "in": {
            1997: ("《京都议定书》通过，作为发展中国家致力于推动机制建设。", "Kyoto Protocol adopted; committed to mechanism building as developing nation."),
            2005: ("通过清洁发展机制(CDM)成为全球最大CER供应国之一，专注新能源。", "Became a top CER supplier via CDM, focusing on renewable energy."),
            2011: ("发布国家增强能效使命(NMEEE)及PAT机制，是最早的强制碳交易尝试。", "Launched PAT mechanism under NMEEE, an early mandatory energy efficiency ETS."),
            2015: ("《巴黎协定》承诺减少单位GDP碳排放强度，探索国内碳市场。", "Paris Agreement pledge to reduce GDP emission intensity; explored domestic ETS."),
            2022: ("议会通过《能源节约修正案》，授权建立国家碳市场体系(ICM)。", "Passed Energy Conservation Amendment, authorizing Indian Carbon Market (ICM)."),
            2023: ("正式发布《碳信用交易计划(CCTS)》，标志强制性碳市场规则奠定。", "Published Carbon Credit Trading Scheme (CCTS), laying mandatory ETS rules."),
            2024: ("逐步将PAT机制转变为更成熟的碳交易体系，纳入电力与工业。", "Transitioning PAT to a mature ETS, incorporating power and industry sectors."),
            2030: ("NDC关键节点：非化石燃料装机占比达到50%，市场涵盖基础工业。", "NDC milestone: 50% non-fossil capacity; market covers heavy industries."),
            2040: ("碳排放预计达到峰值，碳市场交易活跃度达到顶峰。", "Emissions expected to peak; carbon market trading activity at its highest."),
            2050: ("NDC深化阶段：碳价格机制成熟，高耗能产业全面脱碳。", "Deepened NDC stage: mature carbon pricing, total decarbonization of heavy industry."),
            2060: ("全面接入负排放技术和碳捕集交易(CCS)，备战2070净零目标。", "Fully integrated negative emissions and CCS trading to prep for 2070 net-zero.")
        },
        "me": {
            1997: ("作为传统化石能源出口巨头，初期在国际气候谈判中持保守态度。", "Traditional fossil fuel exporters; initially conservative in climate negotiations."),
            2015: ("签署《巴黎协定》，海湾国家开始提出经济多元化与能源转型愿景。", "Signed Paris Agreement; Gulf states began envisioning economic diversification."),
            2021: ("沙特提出'绿色沙特倡议'及2060净零目标，阿联酋宣布2050净零目标。", "Saudi announced Green Initiative & 2060 Net Zero; UAE pledged Net Zero by 2050."),
            2022: ("沙特主权基金(PIF)牵头成立中东与北非自愿碳市场(RVCMC)。", "Saudi PIF established the MENA Regional Voluntary Carbon Market Co (RVCMC)."),
            2023: ("阿联酋举办COP28，大力发展碳金融，阿布扎比吸引众多绿色资管机构入驻。", "UAE hosted COP28, aggressively expanding carbon finance and green asset management."),
            2025: ("主权财富基金加速跨国布局，向亚洲(如印尼、印度)的绿色基建及碳汇注入巨资。", "Sovereign wealth funds poured capital into Asian green infrastructure and carbon sinks."),
            2030: ("中东从'化石能源出口中心'初步转型为连接亚欧的'气候金融与绿氢枢纽'。", "Transitioning from fossil fuel exporters to a climate finance & green hydrogen hub.")
        },
        "au": {
            1997: ("签署《京都议定书》，但由于国内化石能源利益，气候政策长期摇摆。", "Signed Kyoto but climate policy fluctuated heavily due to domestic fossil fuel interests."),
            2011: ("短暂引入碳定价机制(Carbon Pricing Mechanism)，但于2014年被废除。", "Briefly introduced a Carbon Pricing Mechanism, which was repealed in 2014."),
            2016: ("建立保障机制(Safeguard Mechanism)，要求大型排放设施控制基准线。", "Established Safeguard Mechanism to limit emissions from large facilities."),
            2023: ("彻底改革保障机制，要求高排企业每年减排4.9%，实质上转变为交易市场。", "Reformed Safeguard Mechanism (requiring 4.9% annual cuts), effectively becoming a baseline-and-credit market."),
            2025: ("加速对日韩的绿氢出口布局，并探索跨国碳捕集与封存(CCS)枢纽合作。", "Accelerated green hydrogen exports to JP/KR and explored cross-border CCS hub cooperation."),
            2030: ("转型为'可再生能源超级大国'，为亚洲提供大量零碳能源与高质量碳信用。", "Transitioning into a 'Renewable Energy Superpower', supplying zero-carbon energy and credits to Asia."),
            2050: ("实现净零排放，成为亚太地区负排放技术(CDR)和绿色大宗商品的核心基石。", "Achieved Net-Zero, becoming the APAC cornerstone for CDR and green commodities.")
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
    me_r = 30000 if year < 2021 else 55000
    au_r = 30000 if year < 2016 else 55000

    add("cn", t["cn"], 116.4, 39.9, [255, 50, 50, 200], cn_r)
    add("jp", t["jp"], 139.6, 35.6, [50, 150, 255, 200], jp_r)
    add("kr", t["kr"], 126.9, 37.5, [50, 150, 255, 200], kr_r)
    add("sg", t["sg"], 103.8, 1.3, [50, 150, 255, 200], sg_r)
    add("id", t["id"], 106.8, -6.2, [255, 200, 50, 200], id_r)
    add("in", t["in"], 78.9, 20.5, [255, 200, 50, 200], in_r)
    add("vn", t["vn"], 105.8, 21.0, [255, 200, 50, 200], vn_r)
    add("me", t["me"], 45.0, 24.0, [148, 0, 211, 200], me_r)
    add("au", t["au"], 133.2, -25.2, [255, 140, 0, 200], au_r) # 橙色节点代表澳洲
    
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
    # 中东 -> 亚洲 绿色资金/碳资产跨境流动
    if year >= 2023:
        for target in [[106.8, -6.2], [78.9, 20.5]]: # 飞向印尼、印度
            arcs.append({"s": [45.0, 24.0], "t": target, "c": [255, 20, 147, 200]}) # 深粉色资金线
    # arcs 连线的部分，追加：
    if year >= 2025:
        for target in [[139.6, 35.6], [126.9, 37.5]]: # 飞向日本、韩国
            arcs.append({"s": [133.2, -25.2], "t": target, "c": [0, 255, 127, 200]}) # 亮绿色代表绿氢/新能源供应链

    return pd.DataFrame(nodes), pd.DataFrame(arcs)

dn, da = get_data(selected_year, cbam_trigger, link_trigger, t, lang)

# ==========================================
# 6. 渲染与双标签页系统
# ==========================================
# 极简标题
st.markdown(f"<h3 style='margin-bottom: 0px;'>{t['title']}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color: gray; margin-top: 5px;'><b>{t['subtitle']}</b></p>", unsafe_allow_html=True)

# 创建四标签页
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 世纪地缘沙盘 (Geopolitics Sandbox)", 
    "📊 市场微观数据库 (Market Profiles)",
    "🎛️ 宏观战略政策简报 (Strategic Policy Briefing)",
    "📖 深度研究报告 (Comprehensive Report)"
])
# ------------------------------------------
# Tab 1: 主沙盘视图 (原有的所有内容)
# ------------------------------------------
with tab1:
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

    # 静态历史年表附录
    st.markdown("---")
    st.subheader("📜 亚洲碳市场发展年表（1997—2060）" if lang == "中文" else "📜 Asian Carbon Market Timeline (1997-2060)")

    if lang == "中文":
        st.markdown("""
        **第一阶段：早期探索与地方试点（1997—2020）**
        * **1997年**：日本颁布措施允许企业通过自愿碳额度抵消排放。
        * **2005年**：日本启动自愿排放交易体系（JVETS）。
        * **2010年**：日本东京都政府启动亚洲首个城市级强制性总量与交易计划（TMG ETS）。韩国颁布《低碳绿色增长基本法》。
        * **2011年**：中国发改委批准北京、上海等7省市开展碳排放权交易试点。日本埼玉县ETS启动并与东京都市场互联。
        * **2013年**：中国各地试点陆续正式开市，深圳率先启动。
        * **2015年**：韩国建立东亚首个全国性强制碳市场（K-ETS）。
        * **2016年**：亚洲协会政策研究院提出中日韩三国碳市场渐进式链接路线图。
        * **2019年**：新加坡引入碳税机制，初始税率5新元/吨。
        * **2020年**：东南亚自愿碳信用供应占全球约21%，达到历史高峰，随后快速萎缩。

        **第二阶段：全国强制市场建立与快速扩张（2021—2025）**
        * **2021年**：中国全国碳排放权交易市场正式启动。
        * **2022年**：韩国K-ETS进入第三阶段，覆盖范围扩至全国79%排放量。
        * **2023年**：日本推出绿色转型排放权交易市场（GX-ETS）；印尼启动燃煤电厂强制ETS；印度碳信用交易计划（CCTS）启动试点。
        * **2024年**：中国重启CCER市场，宣布ETS将扩容至钢铁等8大行业。新加坡碳税提升至25新元/吨。
        * **2025年**：越南全国试点碳市场启动。欧盟CBAM正式开始征收碳关税。

        **第三阶段：强制履约深化与行业扩容（2026—2030）**
        * **2026年**：日本GX-ETS转为强制履约。韩国引入"碳差额合约（CCfD）"。印度CCTS首个正式履约期开始。
        * **2027年**：中国全国ETS进入第二阶段，逐步引入拍卖机制。印尼ETS扩容。
        * **2028年**：日本引入GX附加费。印尼引入"总量上限—碳税—交易"混合机制。
        * **2029年**：越南全国碳市场正式全面运行。
        * **2030年**：中国实现碳达峰。东盟共同碳框架（ACCF）推动标准互认。

        **第四阶段：深度脱碳、区域一体化与净零目标（2031—2060）**
        * **2033年**：日本对电力行业高排放主体正式引入强制配额拍卖。
        * **2035年**：欧盟CBAM全面实施。中国全国碳市场免费配额基本退出。
        * **2040年**：中日韩三国碳市场链接框架趋于成熟。东南亚成为全球碳抵消枢纽。
        * **2050年**：日、韩、新实现碳中和或净零排放。
        * **2060年**：中国实现碳中和目标，全国碳市场转型为净零后的碳移除激励体系。
        """)
    else:
        st.markdown("*Please refer to the detailed timeline in the previous section or switch to Chinese for full details.*")

    with st.expander("📚 References"):
        st.markdown("""
        * Australian Government (DCCEEW). (2023). *Safeguard Mechanism Reforms*.
        * BloombergNEF. (2025). *Advancing Southeast Asia Carbon Market: Nature and Nurture*.
        * CLP. (2024). *CLP’s Climate Vision 2050*.
        * EWING, J. (2016). *Roadmap to a Northeast Asian Carbon Market*. Asia Society Policy Institute.
        * International Carbon Action Partnership. (2025). *Emissions Trading Worldwide: Status Report 2025*. ICAP.
        * International Energy Agency. (2021). *Net Zero by 2050*. IEA.
        * World Economic Forum, & Bain & Company. (2025). *Asia’s Carbon Markets: Strategic Imperatives for Corporations*. WEF.
        """)

# ------------------------------------------
# Tab 2: 市场微观数据库 (基于 ICAP 2025 报告)
# ------------------------------------------
with tab2:
    if lang == "中文":
        tab2_title = "📚 亚太区域碳市场微观数据库 (ICAP 2025)"
        tab2_desc = "本数据库基于 **International Carbon Action Partnership (ICAP) Emissions Trading Worldwide: Status Report 2025** 整理，收录了亚太地区 22 个核心国家与地方级碳市场的详细运作机制。"
        selector_label = "📌 请选择要查询的碳市场体系："
        lbl_status = "**市场现状：**"
        lbl_coverage = "**🏭 覆盖范围**"
        lbl_allocation = "**⚖️ 配额与分配**"
        lbl_offset = "**🔄 抵销机制与价格**"
        
        market_db = {
            "澳大利亚 (Australia)": {
                "status": "于2023年7月正式启动“保障机制”（Safeguard Mechanism），属于基于排放强度的碳交易体系。",
                "coverage": "涵盖采矿、制造业、国内交通运输以及石油、天然气和废弃物等行业。2022年经核查的覆盖排放量为1.387亿吨二氧化碳当量（占总排放量的26%）。纳入门槛为每年直接（范围1）排放量超过10万吨二氧化碳当量的设施。截至2023财年，共纳入219家主体。",
                "allocation": "采用基于实际产量和排放强度的基准法进行免费分配，标准基准线默认每年下降4.9%直至2030年。目前没有拍卖机制。",
                "offset": "允许无数量限制地使用澳大利亚碳信用（ACCU），但使用量超过基准30%时需公开说明原因。2024财年，超排设施可向监管机构以75澳元（约合50美元）的固定价格购买ACCU。"
            },
            "新西兰 (New Zealand)": {
                "status": "于2008年启动，是涵盖范围广泛的核心气候政策，其排放总量上限轨迹与国家2050年净零目标保持一致。",
                "coverage": "涵盖林业、固定能源、工业加工、液体化石燃料、废弃物和合成温室气体等行业。2025年的绝对排放总量上限为1,910万吨二氧化碳当量。农业排放报告义务已于2024年被废除。截至2024年底，共有4,617个注册主体（其中多数为自愿加入的林业主体）。",
                "allocation": "以拍卖为主（2024年拍卖配额占51%）。对排放密集且易受贸易影响的（EITE）行业采用基于产量和强度基准的免费分配。林业及其他移除活动可直接获得配额。",
                "offset": "目前不允许使用抵销信用（2015年6月后禁止国际信用）。2024年平均二级市场价格为59.31新西兰元（约合35.91美元），平均拍卖价格为64新西兰元。"
            },
            "北京 (Beijing)": {
                "status": "2013年11月启动，是中国三个由地方人大批准立法的区域碳市场之一，并率先实施了价格上下限稳定机制。",
                "coverage": "2022年排放上限约为4,400万吨二氧化碳当量，覆盖全市约30%的排放。涵盖供热、水泥、石化、制造业、服务业及公共交通等行业的882家单位。纳入门槛为年排放5,000吨二氧化碳当量。",
                "allocation": "采用基准法（如电力、数据中心等）或基于历史强度的祖父法免费分配，保留不超过5%的配额用于不定期拍卖。",
                "offset": "允许使用CCER和北京核证自愿减排量（BCER），上限为年度排放量的5%（其中至少50%需来自北京本地项目）。2024年二级市场平均价格为102元人民币（约合14美元）。"
            },
            "菲律宾 (Philippines)": {
                "status": "正在审议中。2025年2月众议院二读通过了第11375号法案，旨在建立碳定价框架和实施机制。",
                "coverage": "该法案要求能源、交通、工业、农业、林业和废弃物行业的大型排放源制定脱碳计划。",
                "allocation": "气候变化委员会（CCC）将汇总部门脱碳路径，并确定单个纳管主体的年度配额分配计划。",
                "offset": "纳管主体可通过购买国内外抵销信用（包括林业、可再生能源等项目），或按气候变化委员会设定的碳价为超排部分缴纳资金来履行合规义务。"
            },
            "中国 (China - 全国碳市场)": {
                "status": "2021年启动，是目前全球覆盖排放量最大的、基于排放强度的碳交易体系。",
                "coverage": "目前涵盖电力行业，并将于2024年至2026年间扩展至钢铁、水泥和铝冶炼行业。2024年排放总量上限约80亿吨二氧化碳当量（占全国总排放量60%以上），覆盖约3,500家年排放超26,000吨的单位。",
                "allocation": "目前100%采用基于产量的基准法免费分配。《暂行条例》明确提出未来将引入拍卖机制并逐步扩大适用范围。",
                "offset": "允许使用全国碳市场未涵盖项目产生的CCER，抵销上限为核查排放量的5%。2024年二级市场平均价格为95.96元人民币。"
            },
            "韩国 (Republic of Korea)": {
                "status": "2015年启动，为东亚首个全国性强制碳市场。目前正实施重大改革以对齐2030及2050净零目标。",
                "coverage": "2024年上限为5.671亿吨二氧化碳当量，覆盖韩国约79%的温室气体排放。涵盖电力、工业、建筑、交通等行业共816家企业。纳入门槛为企业年排放逾12.5万吨或设施逾2.5万吨。",
                "allocation": "对EITE行业100%免费分配，其余适用拍卖的行业配额至少有10%需通过拍卖获得（第三阶段基准法分配比例达60%，第四阶段将提高至75%）。",
                "offset": "允许使用国内及符合条件的国际抵销信用，总上限为每家企业履约义务的5%。2024年二级市场平均价格为9,238韩元（约合6.78美元），平均拍卖价为10,355韩元。"
            },
            "重庆 (Chongqing)": {
                "status": "2014年启动，是中国唯一覆盖非二氧化碳温室气体（如甲烷、HFCs等）的区域碳市场。自2021年起由绝对总量转为基于强度的排放上限。",
                "coverage": "涵盖所有工业领域（电解铝、水泥、钢铁等）的334家单位（2023年）。纳入门槛为年排放13,000吨或能耗5,000吨标煤。",
                "allocation": "采用历史强度法、基准法或祖父法免费分配，自2021年起辅以临时拍卖。对实现“减污降碳”或达到能效基准的企业有额外配额奖励。",
                "offset": "CQCER（“碳惠通”）抵销上限为履约义务的5%。另允许外购绿色电力抵销最多8%的缺口。2024年二级市场均价为40.05元人民币。"
            },
            "埼玉县 (Saitama)": {
                "status": "2011年启动，涵盖大型建筑和工厂，且自启动起便与东京总量与交易计划相链接。",
                "coverage": "2022年经核查排放量为630万吨二氧化碳当量。涵盖571个工商业建筑及工厂（门槛：连续三年耗能超150万升原油当量）。",
                "allocation": "100%免费分配。每个设施的绝对上限基于“基准年排放量 × (1-履约系数) × 5年”计算。第四履约期（2025-2029年）履约系数将收紧至50%（办公楼）或48%（工厂）。",
                "offset": "允许使用中小设施指标、县外指标、可再生能源及东京减排指标。场外可再生能源视为零排放。历史平均价格约为144日元（约合0.95美元）。"
            },
            "福建 (Fujian)": {
                "status": "2016年启动，拥有以碳汇和林业为重点的省级机制，连续七年履约率100%。",
                "coverage": "2022年上限为1.162亿吨二氧化碳当量。涵盖石化、化工、建材、钢铁、陶瓷、航空等行业的293家单位（电力于2019年移出）。门槛为年能耗5,000吨标煤。",
                "allocation": "主要通过祖父法（如陶瓷）或基准法（如化工、航空）免费分配。仅在2016年举行过一次拍卖。",
                "offset": "允许使用CCER（上限5%）和福建林业碳汇（FFCER）；若同时使用两者，抵销上限可达10%。2024年二级市场均价为21.52元人民币。"
            },
            "上海 (Shanghai)": {
                "status": "2013年启动，全国唯一自启动以来连续保持100%履约率的市场，抵销市场活跃且率先开展远期交易。",
                "coverage": "2023年上限1.05亿吨二氧化碳当量，涵盖工业、海运、建筑、国内航空等领域的378家单位。自2024年起扩展至数据中心及道路运输行业。",
                "allocation": "采用行业基准法或祖父法免费分配，辅以每年两次以上的固定拍卖。对达到减污降碳标准的企业有额外0.3-0.5%奖励。",
                "offset": "CCER和上海核证自愿减排量（SHCER）总抵销上限为5%。符合条件的跨省购买绿电可视为零排放。2024年二级市场均价为75.45元人民币，拍卖均价为77.87元。"
            },
            "广东 (Guangdong)": {
                "status": "2013年启动，是中国规模最大、现货交易量最高的区域碳市场。首个引入拍卖机制的试点。",
                "coverage": "2023年上限2.97亿吨二氧化碳当量，涵盖水泥、钢铁、石化、造纸、航空等，并扩容至陶瓷、纺织和数据中心的391家单位。门槛为年排放1万吨或能耗5,000吨标煤。",
                "allocation": "以免费分配为主（基准法及基于历史排放的祖父法）。新进入者（自2023起）仅提供6%免费配额。曾不定期进行拍卖。",
                "offset": "CCER和本地碳普惠（PHCER）使用上限为年度排放的10%，且其中70%必须来自广东省内。广东还对PHCER进行拍卖。2024年二级市场均价为51.37元人民币。"
            },
            "深圳 (Shenzhen)": {
                "status": "2013年启动，由地方人大专门立法监管，市场流动性活跃，率先实施跨区域交易。",
                "coverage": "2024年上限3,350万吨二氧化碳当量。涵盖制造、水务、交通、建筑等，2024年新增数据中心、固废、餐饮零售及公共机构等领域的737家单位。门槛为年排放超3,000吨。",
                "allocation": "采用基准法（如供水、天然气、数据中心）或祖父法免费分配，辅以不定期拍卖（如2014年和2022年）。",
                "offset": "CCER、碳普惠等抵销信用使用上限为清缴缺口的20%。自2024起绿电也纳入抵销。2024年二级市场均价为47.78元人民币。"
            },
            "湖北 (Hubei)": {
                "status": "2014年启动，是中国最活跃的区域碳市场之一，负责运营全国碳市场注册登记和结算系统。",
                "coverage": "2023年上限1.79亿吨二氧化碳当量。不预先限定行业，适用于所有年排放量≥13,000吨的工业单位，共涵盖449家。",
                "allocation": "采用基准法和祖父法免费分配，辅以“市场调整系数”调控总量，并设有20%或20万吨的履约缺口上限。每年通常举行两次配额拍卖。",
                "offset": "CCER上限为分配量的10%。另允许配额短缺的单位使用绿电证书及武汉市级抵销信用，上限均为10%。2024年二级市场均价为40.41元人民币。"
            },
            "中国台湾 (Taiwan, China)": {
                "status": "建设中。2023年《气候变迁因应法》规定将分阶段实施碳费及国内总量管制与交易计划（ETS）。",
                "coverage": "要求年排放超25,000吨二氧化碳当量的电力和制造业从2026年起（基于2025年排放）缴纳碳费。",
                "allocation": "初期以征收碳费为主，费率为每吨300新台币（约合9.34美元）。计划在四年内（最早2026年）由碳费过渡到ETS。",
                "offset": "允许使用国内自愿减排项目信用（上限10%），以及特定标准下的国际抵销信用（上限5%）。"
            },
            "印度 (India)": {
                "status": "建设中。基于《2001年节能法》修正案建立的碳信用交易计划（CCTS）正在制定中，首个合规期计划于2026财年开启。",
                "coverage": "属于基于强度的基准线与信用体系。初期将覆盖能源密集型行业的约800家实体（包括铝、水泥、钢铁、石化、化肥等9个行业），逐步取代现有的PAT计划。",
                "allocation": "政府将设定包含三年目标的温室气体强度轨迹。超额完成目标的企业将获发碳信用证书（CCCs），未达标者则需在市场上购买并注销等量CCCs。",
                "offset": "计划并行推出国内自愿抵销机制，允许非纳管实体开发减排/移除项目获取CCCs以提高市场流动性。价格机制由电力交易所及中央电力监管委员会（CERC）监管。"
            },
            "泰国 (Thailand)": {
                "status": "建设中。《气候变化法案》终稿预计于2025年提交内阁审批，并计划于2027年实施。提案机制包含ETS、碳税及碳边境调节机制。",
                "coverage": "将由泰国温室气体管理组织（TGO）制定分行业的温室气体上限，并由管理部门（DCCE）设立在线报告平台和交易登记系统。",
                "allocation": "分配计划每三至五年更新一次，包含绝对上限机制、逐步递减的配额总量，以及明确的拍卖与免费分配比例。",
                "offset": "法规将明确允许用于合规的碳信用（如国内的T-VER项目）数量上限及资质标准。自2013年起已运行自愿碳市场（V-ETS）试点并允许使用抵销信用。"
            },
            "印度尼西亚 (Indonesia)": {
                "status": "2023年推出针对电力行业的强制性、基于强度的碳市场（NEK Trading Scheme），计划于2025年转向“总量上限-税-交易”混合体系。",
                "coverage": "第一阶段（2023-2024）上限约2.568亿吨二氧化碳当量，涵盖146座并网燃煤电厂（装机≥25MW）。预计后续将扩容至自备燃煤电厂及燃气电厂等。",
                "allocation": "采用技术排放限额（PTBAE）进行基准法免费分配，首年100%免费，次年降至75-85%（依履约情况而定）。具备在IDXCarbon进行拍卖的机制但目前无交易量。",
                "offset": "允许无数量限制地使用国内抵销信用（SPE-GRK，需来自可再生能源或能效等项目）。2024年场外配额均价约12,000印尼盾（约0.76美元），二级市场SPE均价约58,800印尼盾。"
            },
            "天津 (Tianjin)": {
                "status": "2013年12月启动，与全国碳市场并行运行，目前正进行将海运、航空及数据中心纳入管控的公众咨询。",
                "coverage": "2023年上限为7,400万吨二氧化碳当量。涵盖所有年排放≥20,000吨的工业领域，共包含159家单位。",
                "allocation": "采用祖父法（大多数行业依据2023年排放量设定0.96-0.98的调整系数）或基准法（建材行业、新进入者）进行免费分配。曾于2019至2021年间举行五次临时拍卖。",
                "offset": "允许使用CCER和天津本地林业碳汇，总使用量不得超过年度义务的10%（仅限2013年后非水电类CO2减排项目）。外购非化石能源也可抵销。2024年二级市场均价为23.66元人民币。"
            },
            "日本 (Japan)": {
                "status": "十年绿色转型（GX）政策的核心部分。自愿性GX-ETS于2023-2024启动，将在2026财年全面过渡为强制性碳市场。",
                "coverage": "第一阶段（自愿期）已有超700家企业参与，占全国排放总量的50%以上。",
                "allocation": "第一阶段基于基准线与信用体系运行。计划从2033财年起，向电力行业的高排放纳管主体引入强制拍卖机制。",
                "offset": "允许使用J-Credits（国内机制）以及JCM（联合信用机制）的国际抵销信用。此外将于2028财年起对化石燃料进口和开采商征收碳附加费（GX-Surcharge）。"
            },
            "东京都 (Tokyo)": {
                "status": "2010年4月启动，是全球首个城市级碳市场。与埼玉县市场相连接，即将进入减排要求极为严格的第四履约期（2025-2029年）。",
                "coverage": "2024年上限1,220万吨二氧化碳当量（占都会区20%），覆盖约1,200个年耗能超1,500千升原油当量的工商业建筑及工厂。",
                "allocation": "100%免费分配。绝对上限基于“基准年排放 × (1-履约系数) × 5年”。第四履约期系数收紧至50%（办公楼）或48%（工厂）。达标设施可将超额减排量作为指标交易。",
                "offset": "允许使用中小设施指标、东京都外指标（上限1/3）、可再生能源及埼玉减排指标。场外可再生能源及绿电合约均被视为零排放。2024年均价约600日元（约合3.96美元）。"
            },
            "马来西亚 (Malaysia)": {
                "status": "建设中。2022年推出了全球首个符合伊斯兰教法的自愿碳市场平台（BCX），且2024年发布了包含国内ETS条款的《气候变化法案》咨询文件。",
                "coverage": "法案提议建立国内排放交易体系（ETS），在设施层面引入温室气体排放门槛。砂拉越州也已通过包含工业强制排放门槛的气候法案。",
                "allocation": "目前正在与世界银行合作开展碳定价工具的可行性研究，重点聚焦政策与市场设计、注册系统开发以及基准线分配与基础设施开发。",
                "offset": "计划利用现有的Bursa Carbon Exchange (BCX) 平台支持合规市场及自愿市场的碳信用交易与注销。"
            },
            "越南 (Vietnam)": {
                "status": "建设中。基于2021年修订的《环境保护法》，政府获得了建立国家信用机制（NCM）和国内ETS的法律授权。预计2025年6月开启试点，2029年全面运行。",
                "coverage": "年排放超过3,000吨二氧化碳当量的设施自2025年起负有报告义务。试点阶段主要针对高排放部门。",
                "allocation": "试点期（2025-2028）的排放配额将向高排放行业100%免费发放，自然资源和环境部（MONRE）将制定排放限额与分配方法。全面运行后可能引入拍卖机制。",
                "offset": "允许在规定门槛内使用认证碳信用（CCCs）进行合规，来源包括国内项目及CDM、JCM和《巴黎协定》第6.4条等国际机制。"
            }
        }
    else:
        tab2_title = "📚 Asia-Pacific Carbon Market Profiles (ICAP 2025)"
        tab2_desc = "This database is compiled based on the **International Carbon Action Partnership (ICAP) Emissions Trading Worldwide: Status Report 2025**, covering the operational mechanisms of 22 national and sub-national carbon markets across the APAC region."
        selector_label = "📌 Select a Carbon Market Profile:"
        lbl_status = "**Market Status:**"
        lbl_coverage = "**🏭 Coverage**"
        lbl_allocation = "**⚖️ Allocation & Distribution**"
        lbl_offset = "**🔄 Offsets & Pricing**"
        
        market_db = {
            "Australia": {
                "status": "The Safeguard Mechanism was officially launched as an intensity-based emissions trading system in July 2023.",
                "coverage": "Covers around 220 facilities in the mining, manufacturing, domestic transport, oil, gas, and waste sectors. In 2022, verified covered emissions were 138.7 MtCO2e (26% of total emissions). The inclusion threshold is direct (Scope 1) emissions of over 100,000 tCO2e per year. In FY2023, 219 entities were covered.",
                "allocation": "Free allocation is conducted using a production-adjusted emissions intensity framework (output-based benchmarking). The standard baseline decline rate is set at a default of 4.9% per year until 2030. Allowances are currently not auctioned.",
                "offset": "Unlimited use of Australian Carbon Credit Units (ACCUs) is allowed, but facilities surrendering ACCUs equal to more than 30% of their baseline must publicly state why more onsite abatement was not undertaken. In FY2024, facilities exceeding their baseline could purchase ACCUs from the regulator at a fixed price of AUD 75 (approx. USD 50)."
            },
            "New Zealand": {
                "status": "Launched in 2008, the NZ ETS is a central climate policy with a cap trajectory aligned with the country's 2050 net-zero targets.",
                "coverage": "Covers forestry, stationary energy, industrial processing, liquid fossil fuels, and waste. The 2025 cap is 19.1 MtCO2e. Agricultural emission reporting obligations were repealed in 2024. As of late 2024, there are 4,617 registered entities (mostly voluntary forestry participants).",
                "allocation": "Primarily allocated via auctioning (51% in 2024). Free allocation is provided based on output and intensity benchmarks for emissions-intensive, trade-exposed (EITE) activities. Forestry and other removal activities are granted units for sequestration.",
                "offset": "Offset credits (and international units since 2015) are not allowed. Average 2024 auction price was NZD 64, and the secondary market price was NZD 59.31."
            },
            "Beijing": {
                "status": "Launched in November 2013, it is one of three Chinese pilots backed by regional congress legislation and pioneered a price corridor mechanism.",
                "coverage": "The 2022 cap was ~44 MtCO2e, covering ~30% of the city’s emissions. Regulates 882 entities across heat, cement, petrochemicals, manufacturing, service, and public transport. Inclusion threshold is 5,000 tCO2 per year.",
                "allocation": "Allowances are distributed for free via benchmarking or grandparenting. Up to 5% is set aside for irregular auctions.",
                "offset": "CCERs and local BCERs are allowed up to 5% of annual emissions (at least 50% must originate from Beijing). The 2024 average secondary market price was CNY 102 (USD 14)."
            },
            "Philippines": {
                "status": "Under consideration. House Bill No. 11375 establishing a Carbon Emission Pricing Framework was approved on 2nd Reading in February 2025.",
                "coverage": "Mandates large emitters from energy, transportation, industry, agriculture, forestry, and waste sectors to develop decarbonization plans.",
                "allocation": "The Climate Change Commission (CCC) will consolidate sectoral pathways and determine annual allowance allocation plans for covered entities.",
                "offset": "Entities exceeding allowances can purchase carbon allowances, internationally recognized offset credits, or contribute funds towards decarbonization equivalent to the CCC's established carbon price."
            },
            "China (National)": {
                "status": "Operating since 2021 as an intensity-based system, it is the world's largest ETS by covered emissions.",
                "coverage": "Cap is estimated at ~8,000 MtCO2 (2024), representing >60% of national emissions. Currently covers the power sector, with ongoing expansion to steel, cement, and aluminum smelters (2024–2026). Covers ~3,500 entities with emissions over 26,000 tCO2e/year.",
                "allocation": "100% free allocation using output-based benchmarking. Interim Regulations clarify that auctioning will be introduced and gradually expanded.",
                "offset": "Covered entities can use CCERs for up to 5% of their verified emissions. The 2024 average secondary market price was CNY 95.96 (USD 13.33)."
            },
            "Republic of Korea": {
                "status": "Launched in 2015 as East Asia's first nationwide mandatory ETS. Currently undergoing major reforms through the Basic Plan for 2026-2035.",
                "coverage": "The 2024 cap was 567.1 MtCO2e (79% of GHG emissions). Covers 816 entities in power, industry, buildings, waste, transport, aviation, and maritime. Threshold: >125,000 tCO2/company or >25,000 tCO2/facility.",
                "allocation": "100% free allocation for EITE sectors. Eligible sectors must procure at least 10% of allowances via auction. Benchmarking reaches 60% of primary allocation in Phase 3 and will rise to 75% in Phase 4.",
                "offset": "Domestic and international offsets are allowed up to 5% combined. The 2024 average auction price was KRW 10,355 (USD 7.60), and the secondary market average was KRW 9,238 (USD 6.78)."
            },
            "Chongqing": {
                "status": "Launched in 2014, it is the only Chinese pilot covering non-CO2 GHGs. Shifted from absolute caps to intensity-based caps in 2021.",
                "coverage": "Covers 334 entities (2023) across industrial sectors (e.g., aluminum, cement, steel). Inclusion threshold is 13,000 tCO2e or 5,000 tce/year.",
                "allocation": "Utilizes benchmarking, historical intensity, and grandparenting for free allocation. Ad hoc auctions were introduced in 2021. Rewards entities meeting air pollution/efficiency standards with bonus allocations.",
                "offset": "Only local CQCERs allowed for up to 5% of compliance obligations. Non-fossil energy purchases outside the city can offset up to 8% of shortfalls. The 2024 average secondary market price was CNY 40.05 (USD 5.56)."
            },
            "Saitama": {
                "status": "Launched in April 2011, it has been linked to the Tokyo Cap-and-Trade program since inception and covers large buildings and factories.",
                "coverage": "Verified emissions were 6.3 MtCO2 (2021), accounting for ~17% of prefectural emissions. Regulates 571 commercial and industrial facilities consuming ≥1,500 kL crude oil equivalent annually.",
                "allocation": "100% free allocation based on absolute historical base-year emissions and a compliance factor. The reduction factor tightens to 50% (office) or 48% (factory) in the fourth period (2025–2029).",
                "offset": "Allows specific offsets (Saitama, outside Saitama, Tokyo, and renewable credits) with quantitative limits (up to 1/3 or 50% for outside credits). Off-site renewable energy counts as zero emissions. Average price: JPY 144 (USD 0.95)."
            },
            "Fujian": {
                "status": "Launched in September 2016. Maintained 100% compliance for seven years and places a strong emphasis on forestry offsets.",
                "coverage": "The 2022 cap was 116.2 MtCO2. Regulates 293 entities in petrochemical, chemical, building materials, steel, aviation, and ceramics. Threshold: 5,000 tce/year.",
                "allocation": "Free allocation is predominantly based on grandparenting or benchmarking. Only one ad hoc auction was held in 2016.",
                "offset": "CCER limit is 5%; combined limit increases to 10% if domestic Fujian Forestry credits (FFCERs) are also used. The 2024 average secondary market price was CNY 21.52 (USD 2.99)."
            },
            "Shanghai": {
                "status": "Launched in November 2013, the pilot has consistently maintained a 100% compliance rate. Operates the national ETS exchange platform and has broadened to road transport and data centers.",
                "coverage": "2023 cap was 105 MtCO2. Regulates 378 entities in industry, aviation, maritime, buildings, data centers, and road transport. Thresholds vary (e.g., 20,000 tCO2 for industry, 10,000 tCO2 for road transport).",
                "allocation": "Free allocation utilizes benchmarking and historical intensity. Between 2020 and 2023, auctions were held twice a year (three in 2024) to provide additional supply.",
                "offset": "CCERs and local SHCERs allowed up to 5%. Eligible green power transactions count as zero emissions. 2024 average auction price was CNY 77.87 (USD 10.82), and secondary market price was CNY 75.45 (USD 10.48)."
            },
            "Guangdong": {
                "status": "Launched in December 2013. It is the largest regional ETS in China and the first to introduce auctioning and Tan Pu Hui mechanisms.",
                "coverage": "2023 cap was 297 MtCO2. Regulates 391 entities across cement, steel, petrochemicals, paper, aviation, ceramics, textiles, ports, and data centers. Threshold: 10,000 tCO2 or 5,000 tce/year.",
                "allocation": "Primarily free allocation (benchmarking and grandparenting). Ad hoc auctions have been held but suspended since 2020. New entrants (since 2023) receive only 6% free allocation.",
                "offset": "CCERs and local PHCERs are limited to 10% (at least 70% must originate in Guangdong). PHCERs are also auctioned. The 2024 average secondary market price was CNY 51.37 (USD 7.14)."
            },
            "Shenzhen": {
                "status": "Launched in June 2013 as the only Chinese pilot operating at a sub-provincial level, backed by a dedicated ETS bill. Exhibits the highest liquidity.",
                "coverage": "2024 cap is 33.5 MtCO2. Covers 737 entities in water, gas, manufacturing, waste, public buildings, data centers, and the service sector. Threshold: 3,000 tCO2/year.",
                "allocation": "Largely distributed for free using benchmarking and grandparenting based on historical intensity or GDP. Two ad hoc auctions have been held (2014 and 2022).",
                "offset": "CCERs, Tan Pu Hui, and local offsets can cover up to 20% of shortfalls. Green power can also offset shortfalls starting in 2024. The 2024 average secondary market price was CNY 47.78 (USD 6.64)."
            },
            "Hubei": {
                "status": "Launched in April 2014. One of the most active pilots, and its exchange operates the registry and clearing system for the national ETS.",
                "coverage": "2023 cap was 179 MtCO2. It covers all industrial sectors, establishing an inclusion threshold (instead of targeting specific sectors) of 13,000 tCO2/year (from 2023). Covers 449 entities.",
                "allocation": "Uses benchmarking and grandparenting for free allocation, along with a 'market adjustment factor'. Regular ad hoc auctions are held twice a year.",
                "offset": "CCERs limited to 10%. Green electricity certificates and Wuhan city credits can be used specifically to offset shortfalls (capped at 10%). The 2024 average secondary market price was CNY 40.41 (USD 5.75)."
            },
            "Taiwan, China": {
                "status": "Under development. The 2023 Climate Change Response Act mandates a carbon fee transitioning to a domestic ETS within four years (as early as 2026).",
                "coverage": "The initial carbon fee will apply to power and manufacturing industries emitting more than 25,000 tCO2e annually, based on 2025 emissions.",
                "allocation": "The system begins with a carbon fee of TWD 300 (USD 9.34) per tCO2e in 2026, transitioning into a full cap-and-trade mechanism.",
                "offset": "Emission reduction credits from domestic voluntary/offset projects can cover up to 10% of chargeable emissions. Low-leakage risk facilities can use international credits for up to 5%."
            },
            "India": {
                "status": "Under development. Following the Energy Conservation Act amendment, a legal framework was established for an intensity-based Carbon Credit Trading Scheme (CCTS), launching its first compliance period in FY2026.",
                "coverage": "Initially covers ~800 entities from 9 energy-intensive sectors (e.g., aluminium, cement, iron, steel) transitioning from the existing PAT scheme.",
                "allocation": "Output-based free allocation with GHG intensity targets (baselines) set for 3-year periods. Overachievers earn Carbon Credit Certificates (CCCs); underachievers must surrender CCCs.",
                "offset": "A voluntary domestic crediting mechanism will allow non-covered entities to generate CCCs to boost liquidity. The Central Electricity Regulatory Commission will regulate trading on power exchanges."
            },
            "Thailand": {
                "status": "Under development. The final draft of the Climate Change Act is expected for cabinet approval in 2025 and enforcement in 2027. Includes an ETS, carbon tax, and CBAM.",
                "coverage": "The Department of Climate Change and Environment (DCCE) will set emission caps and manage reporting platforms for industries defined by ministerial regulations.",
                "allocation": "Allocation plans will be updated every 3 to 5 years, defining the caps, phase-down mechanisms, and the share of allowances to be auctioned.",
                "offset": "Covered entities can surrender eligible carbon credits (like domestic T-VERs) under defined limits. A voluntary ETS (V-ETS) pilot has been running since 2013."
            },
            "Indonesia": {
                "status": "Operating since 2023. A mandatory, intensity-based ETS for the power sector that will eventually transition into a hybrid 'cap-tax-and-trade' system by 2025.",
                "coverage": "Phase 1 (2023-2024) cap was ~256.8 MtCO2e. Regulates 146 grid-connected coal-fired power plants (≥25 MW) operated mostly by PLN. Expected to expand to captive CFPPs and gas-fired plants.",
                "allocation": "Allowances (PTBAE-PU) are distributed via output-based benchmarking (100% free first year; 75-85% thereafter). Auctioning via IDXCarbon is planned but not currently utilized.",
                "offset": "Unlimited use of domestic offset credits (SPE-GRK) from renewable and efficiency projects. 2024 average OTC allowance price: IDR 12,000 (USD 0.76); secondary offset price: IDR 58,800 (USD 3.66)."
            },
            "Tianjin": {
                "status": "Launched in December 2013, operates in parallel with the national ETS. Currently holding public consultations to expand to maritime, aviation, and data centers.",
                "coverage": "2023 cap was 74 MtCO2. Covers 159 entities across all industrial sectors emitting ≥20,000 tCO2/year.",
                "allocation": "Free allocation via grandparenting (0.96-0.98 reduction factors applied for 2024) and benchmarking (for building materials and new entrants). Five ad hoc auctions were held between 2019 and 2021.",
                "offset": "CCERs (post-2013 non-hydro CO2 projects) and Tianjin forestry offsets allowed up to 10%. Eligible non-fossil power may also offset obligations. The 2024 average secondary market price was CNY 23.66 (USD 3.29)."
            },
            "Japan": {
                "status": "Voluntary GX-ETS launched in 2023/2024. Will transition into a mandatory ETS from FY2026 alongside a fossil fuel carbon levy (GX-Surcharge) starting in FY2028.",
                "coverage": "The voluntary phase involves more than 700 companies accounting for over 50% of the nation's GHG emissions.",
                "allocation": "Operates currently as a baseline-and-credit system. Auctioning will be introduced for high-emitting entities in the power sector from FY2033.",
                "offset": "Domestic J-Credits and international Joint Crediting Mechanism (JCM) credits are permitted for compliance."
            },
            "Tokyo": {
                "status": "Launched in April 2010. The world’s first city-wide ETS, linked to Saitama's system. Preparing for aggressive cuts in the fourth compliance period (FY2025–2029).",
                "coverage": "2024 cap was 12.2 MtCO2 (covering ~20% of Tokyo's emissions). Covers ~1,200 commercial/industrial facilities consuming ≥1,500 kL crude oil equivalent annually.",
                "allocation": "100% free allocation. Baselines calculated via absolute historical emissions multiplied by a compliance factor. This factor tightens to 50% (office buildings) and 48% (factories) in the fourth period.",
                "offset": "Permits various offsets (outside Tokyo, small/mid-size, renewables, Saitama credits) capped generally at one-third of the facility's obligations. Off-site renewables count as zero emissions. 2024 average price: JPY 600 (USD 3.96)."
            },
            "Malaysia": {
                "status": "Under development. Launched the Bursa Carbon Exchange (BCX) for the voluntary market in 2022. The 2024 draft National Climate Change Bill sets the legal framework for a Domestic ETS.",
                "coverage": "The draft legislation includes provisions to introduce mandatory emissions thresholds at the facility level to manage and trade allowances.",
                "allocation": "The government, in cooperation with the World Bank, is currently executing feasibility studies regarding market design, registry development, and ETS infrastructure.",
                "offset": "The framework heavily emphasizes integrating BCX (voluntary market exchange) with broader domestic compliance structures."
            },
            "Vietnam": {
                "status": "Under development. The 2021 Law on Environmental Protection provides the legal mandate. Pilot ETS begins in June 2025, operating fully by 2029.",
                "coverage": "Facilities with annual GHG emissions >3,000 tCO2e must report biennially starting in 2025. Pilot phase targets high-emitting sectors.",
                "allocation": "During the pilot (2025–2028), emissions allowances will be allocated 100% for free to covered high-emitters. Auctioning mechanisms are anticipated post-2029.",
                "offset": "Integration of Certified Carbon Credits (CCCs) from domestic and international sources (including CDM, JCM, and Paris Agreement Article 6.4) is permitted within defined limits."
            }
        }

    st.subheader(tab2_title)
    st.markdown(tab2_desc)
    
    selected_market = st.selectbox(selector_label, list(market_db.keys()))
    data = market_db[selected_market]
    
    st.markdown(f"### {selected_market}")
    st.info(f"{lbl_status} {data['status']}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(lbl_coverage)
        st.write(data['coverage'])
    with c2:
        st.markdown(lbl_allocation)
        st.write(data['allocation'])
        
    st.markdown(lbl_offset)
    st.success(data['offset'])
# ------------------------------------------
# Tab 3: 宏观战略政策简报 (Strategic Policy Briefing)
# ------------------------------------------
with tab3:
    st.subheader("📑 亚洲能源安全与气候地缘战略简报 (Strategic Policy Briefing)")
    
    if lang == "中文":
        st.markdown("""
        **致：宏观政策制定者、气候外交官与能源战略研究员** 本简报基于“世纪地缘沙盘”的动态推演结果，提炼了影响未来亚洲能源安全的**三大核心地缘政治趋势**。
        """)
        
        st.info("**💡 核心洞察一：绿色保护主义与“碳主权”的觉醒 (The Rise of Green Protectionism)**")
        st.markdown("""
        * **地缘现象**：随着欧盟 CBAM（碳边境调节机制）在 2026 年后全面落地，亚洲传统的“高碳出口驱动型”经济体面临严峻的碳成本倒灌。
        * **战略推演**：CBAM 本质上是气候话语权与资本的跨国转移。如果亚洲国家不加速建立本土强制碳市场并提升碳价，其原本可用于国内能源转型的资金将以“关税”形式流失至欧洲。
        * **政策建议**：亚洲各国必须在 2030 年前完成碳定价机制的强制化与金融化，以捍卫本国“碳主权”。
        """)
        
        st.success("**💡 核心洞察二：东北亚区域互联是争夺定价权的唯一出路 (NE Asia ETS Integration)**")
        st.markdown("""
        * **地缘现象**：中、日、韩三国目前拥有亚洲最成熟、体量最大的碳市场，但各自为政导致碳资产存在巨大价差，在国际上缺乏统一的定价权。
        * **战略推演**：沙盘推演显示，若中日韩在 2030-2040 年间实现碳配额（Allowance）的跨国互认与链接，将彻底重塑全球碳金融格局，使东北亚成为抗衡欧洲 ETS 的全球第二极。
        * **政策建议**：建议以双边 Article 6 协议为起点，逐步探索中日韩及东盟共同碳框架（ACCF），建立亚洲区域碳价基准。
        """)
        
        st.warning("**💡 核心洞察三：中东资本与东南亚碳汇的新型“气候轴心” (The New Climate Finance Axis)**")
        st.markdown("""
        * **地缘现象**：沙特、阿联酋等传统化石能源巨头正在疯狂投资绿色基建；而印尼、马来西亚等东盟国家手握全球最丰富的自然碳汇（NbS）潜力，但极度缺乏转型资金。
        * **战略推演**：2025年以后，中东主权财富基金与东南亚气候资产的结合，正在形成一条完全独立于西方体系的“南南合作”绿色大动脉。
        * **政策建议**：亚洲能源安全不再仅仅是“石油与天然气的保供”，更是“绿电基建、碳汇抵消与主权绿色资本”的深度跨国绑定。
        """)

    else:
        st.markdown("""
        **To: Policymakers, Climate Diplomats, and Energy Strategists** Based on the sandbox simulations, this briefing extracts **three core geopolitical trends** shaping the future of Asian Energy Security.
        """)
        
        st.info("**💡 Insight I: Green Protectionism and the Defense of 'Carbon Sovereignty'**")
        st.markdown("""
        * **Geopolitical Shift**: With the EU's CBAM fully implemented post-2026, Asia's traditional carbon-intensive export economies face severe compliance cost outflows.
        * **Strategic Implication**: CBAM acts as a cross-border wealth transfer. If Asian nations do not aggressively develop domestic mandatory ETS and raise local carbon prices, capital needed for their own green transition will be drained as tariffs to Europe.
        * **Policy Recommendation**: Accelerate the transition from voluntary to mandatory, financialized carbon pricing by 2030 to defend domestic "carbon sovereignty."
        """)
        
        st.success("**💡 Insight II: Northeast Asia Integration as the Counterbalance (NE Asia ETS Integration)**")
        st.markdown("""
        * **Geopolitical Shift**: China, Japan, and South Korea host Asia's largest and most mature carbon markets. However, fragmentation prevents Asia from holding global carbon pricing power.
        * **Strategic Implication**: Sandbox projections indicate that linking the C-J-K markets between 2030-2040 would fundamentally reshape global carbon finance, creating a true counterbalance to the EU ETS.
        * **Policy Recommendation**: Utilize Article 6 bilateral agreements as a stepping stone toward an ASEAN Common Carbon Framework (ACCF) and a unified Asian carbon price benchmark.
        """)
        
        st.warning("**💡 Insight III: The Middle East - ASEAN 'Climate Finance Axis'**")
        st.markdown("""
        * **Geopolitical Shift**: Traditional petrostates (Saudi Arabia, UAE) are pivoting toward massive green investments, while ASEAN countries (Indonesia, Malaysia) hold vast Nature-based Solutions (NbS) potential but lack transition capital.
        * **Strategic Implication**: Post-2025, the convergence of Middle Eastern sovereign wealth and Southeast Asian climate assets forms a new "South-South" green artery, largely bypassing Western financial dominance.
        * **Policy Recommendation**: Redefine Asian Energy Security to encompass not just fossil fuel supply chains, but the deep cross-border integration of green grid infrastructure, carbon offsets, and sovereign green capital.
        """)
# ------------------------------------------
# Tab 4: 深度研究报告 (Comprehensive Report)
# ------------------------------------------
with tab4:
    st.subheader("📖 亚洲碳定价的觉醒：从机制碎片化到地缘战略防御")
    st.caption("综合研究报告 | 基于沙盘推演、市场微观数据与 CBAM 冲击分析")
    st.markdown("---")
    
    if lang == "中文":
        st.markdown("""
        *(您可以将您写好的详细报告正文粘贴在这里)*
        
        #### 一、 执行摘要 (Executive Summary)
        亚洲能源安全的定义正在被改写。传统的“化石能源保供”正在向“低碳供应链安全与碳定价权争夺”转移...
        
        #### 二、 历史地缘演变：从跟随者到规则制定者
        通过【世纪地缘沙盘】的演进可以看出，亚洲碳市场经历了从 CDM 时代的被动跟随，到如今本土 ETS 的全面觉醒...
        
        #### 三、 市场微观洞察：碎片化与不对称的亚洲格局
        基于【市场微观数据库】对亚太22个机制的梳理，当前亚洲碳定价面临的最大挑战是机制的极度碎片化...
        
        #### 四、 2026 CBAM 冲击：亚洲的财务敞口与战略反击
        正如【战略简报】所揭示，欧盟 CBAM 的实质是气候话语权与资本的跨国转移...
        
        #### 五、 结语
        未来的亚洲能源安全，谁掌握了碳定价权和绿色基础设施，谁就掌握了下一个世纪的地缘主导权。
        """)
    else:
        st.markdown("""
        *(Paste your English report content here)*
        
        #### I. Executive Summary
        The definition of Asian Energy Security is being rewritten...
        
        #### II. Historical Geopolitics: From Followers to Rule-Makers
        As observed in the [Geopolitics Sandbox]...
        
        #### III. Market Observations: A Fragmented Landscape
        Based on the [Market Profiles] of 22 APAC systems...
        
        #### IV. The 2026 CBAM Shock & Strategic Defense
        As highlighted in the [Policy Briefing], CBAM acts as a cross-border wealth transfer...
        
        #### V. Conclusion
        In the future of Asian energy security, pricing power equals geopolitical power.
        """)
# ==========================================
# 7. 静态历史年表附录与参考文献
# ==========================================
st.markdown("---")
st.subheader("📜 亚洲碳市场发展年表（1997—2060）" if lang == "中文" else "📜 Asian Carbon Market Timeline (1997-2060)")

if lang == "中文":
    st.markdown("""
    **第一阶段：早期探索与地方试点（1997—2020）**
    * **1997年**：日本颁布措施允许企业通过自愿碳额度抵消排放，成为亚洲碳市场机制的最早探索者。
    * **2005年**：日本启动自愿排放交易体系（JVETS），为日后全国市场的设计积累了数据经验。
    * **2010年**：日本东京都政府启动亚洲首个城市级强制性总量与交易计划（TMG ETS）。韩国颁布《低碳绿色增长基本法》。
    * **2011年**：中国国家发改委批准北京、上海等7个省市开展碳排放权交易试点。日本埼玉县ETS启动并与东京都市场互联。
    * **2013年**：中国各地试点陆续正式开市，深圳率先启动。试点的总覆盖量构成当时全球规模第二大的碳市场。
    * **2015年**：韩国正式建立东亚首个全国性强制碳市场（K-ETS），初期覆盖全国68%排放量。
    * **2016年**：亚洲协会政策研究院提出中日韩三国碳市场渐进式链接的五步路线图。
    * **2019年**：新加坡引入碳税机制，初始税率5新元/吨。
    * **2020年**：东南亚自愿碳信用供应占全球约21%，达到历史高峰，随后供应快速萎缩。

    **第二阶段：全国强制市场建立与快速扩张（2021—2025）**
    * **2021年**：中国全国碳排放权交易市场正式启动，初期覆盖电力行业约2000家企业，成为全球最大碳市场。《巴黎协定》第六条确立跨境规则。
    * **2022年**：韩国K-ETS进入第三阶段，覆盖范围扩至全国79%排放量。
    * **2023年**：日本推出绿色转型排放权交易市场（GX-ETS）；印尼启动燃煤电厂强制ETS；印度碳信用交易计划（CCTS）启动试点。欧盟CBAM过渡期启动。
    * **2024年**：中国重启CCER市场，宣布ETS将扩容至钢铁等8个高碳行业。新加坡将碳税大幅提升至25新元/吨。东南亚自愿碳信用全球供应占比骤降至9%。
    * **2025年**：越南全国试点碳市场正式启动。泰国提交《气候变化法案》草案。欧盟CBAM正式开始征收碳关税。

    **第三阶段：强制履约深化与行业扩容（2026—2030）**
    * **2026年**：日本GX-ETS转为强制履约。韩国电力行业拍卖比例提升至50%，引入"碳差额合约（CCfD）"。印度CCTS首个正式履约期开始。马来西亚征收碳税。
    * **2027年**：中国全国ETS进入第二阶段，逐步引入拍卖机制。印尼ETS扩容至燃气和燃油电厂。
    * **2028年**：日本引入GX附加费。印尼引入"总量上限—碳税—交易"混合机制。
    * **2029年**：越南全国碳市场完成试点，正式全面运行。
    * **2030年**：中国实现碳达峰，全国ETS完成向8大行业的全面扩容，机制转为绝对总量上限。新加坡完成碳税阶梯式提升。东盟共同碳框架（ACCF）推动标准互认。

    **第四阶段：深度脱碳、区域一体化与净零目标（2031—2060）**
    * **2033年**：日本对电力行业高排放主体正式引入强制配额拍卖。
    * **2035年**：欧盟CBAM进入全面实施阶段。中国全国碳市场免费配额基本退出。
    * **2040年**：中日韩三国碳市场链接框架趋于成熟。前沿碳消除技术（DACCS, BECCS）占据重要份额。东南亚成为全球碳抵消枢纽。
    * **2050年**：日本、韩国、新加坡实现碳中和或净零排放。亚洲碳市场在能源系统彻底转型中发挥核心倒逼作用。
    * **2060年**：中国实现碳中和目标，全国碳市场转型为净零后的碳移除激励体系。
    """)
else:
    st.markdown("""
    **Phase 1: Early Exploration & Local Pilots (1997—2020)**
    * **1997**: Japan allows companies to offset emissions via voluntary carbon credits, pioneering Asian carbon market mechanisms.
    * **2005**: Japan launches the voluntary emissions trading scheme (JVETS), accumulating data for future national market design.
    * **2010**: Tokyo Metropolitan Government launches Asia's first city-level mandatory cap-and-trade program (TMG ETS). South Korea enacts the Framework Act on Low Carbon, Green Growth.
    * **2011**: China's NDRC approves 7 regional ETS pilots (Beijing, Shanghai, etc.). Saitama Prefecture ETS launches in Japan and links with Tokyo.
    * **2013**: China's regional pilots officially start trading, led by Shenzhen, becoming the world's second-largest carbon market at the time.
    * **2015**: South Korea establishes East Asia's first national mandatory carbon market (K-ETS), covering 68% of national emissions.
    * **2016**: Asia Society Policy Institute publishes a roadmap for linking China, Japan, and Korea carbon markets.
    * **2019**: Singapore introduces a carbon tax covering ~80% of emissions at 5 SGD/t.
    * **2020**: Southeast Asian voluntary carbon credit supply peaks at ~21% of the global total, dominated by nature-based projects, before rapidly shrinking.

    **Phase 2: National Mandatory Markets & Rapid Expansion (2021—2025)**
    * **2021**: China's national ETS officially launches for the power sector, becoming the world's largest. Article 6 of the Paris Agreement establishes cross-border trading rules.
    * **2022**: South Korea's K-ETS enters Phase 3, expanding to 79% of national emissions.
    * **2023**: Japan launches the GX-ETS; Indonesia launches mandatory ETS for coal plants; India launches CCTS pilot; EU CBAM transition period begins.
    * **2024**: China restarts CCER and announces ETS expansion to 8 sectors. Singapore hikes carbon tax to 25 SGD/t. SE Asia voluntary credit global share drops to 9%.
    * **2025**: Vietnam launches pilot national ETS. Thailand submits Climate Change Bill. EU CBAM officially begins levying carbon tariffs.

    **Phase 3: Deep Compliance & Sector Expansion (2026—2030)**
    * **2026**: Japan's GX-ETS transitions to mandatory compliance. Korea implements K-ETS Phase 4 (50% auctioning for power, CCfD introduced). India CCTS first compliance period begins. Malaysia taxes steel and energy sectors.
    * **2027**: China ETS Phase 2 introduces auctioning. Indonesia ETS expands to gas and oil plants.
    * **2028**: Japan introduces GX Surcharge. Indonesia introduces Cap-Tax-Trade hybrid mechanism.
    * **2029**: Vietnam national ETS becomes fully operational with auctioning.
    * **2030**: China achieves carbon peak; ETS covers 8 sectors with absolute caps. Singapore hits target carbon tax rate. ASEAN Common Carbon Framework (ACCF) promotes standard mutual recognition.

    **Phase 4: Deep Decarbonization, Integration & Net-Zero (2031—2060)**
    * **2033**: Japan introduces mandatory quota auctions for high-emission power entities.
    * **2035**: EU CBAM fully implemented. China ETS transitions to full auctioning, phasing out free allocation.
    * **2040**: C-J-K carbon market linkage matures. Frontier tech (DACCS, BECCS) gains share. SE Asia remains a core global offset hub.
    * **2050**: Japan, Korea, and Singapore achieve net-zero. Carbon markets drive major energy system transformations across Asia.
    * **2060**: China achieves carbon neutrality. National ETS transforms into a carbon removal incentive system for net-negative emissions.
    """)

# 参考文献折叠面板 (双语环境下均保持英文)
with st.expander("📚 References"):
    st.markdown("""
    * BloombergNEF. (2025). *Advancing Southeast Asia Carbon Market: Nature and Nurture*. BloombergNEF.
    * CLP. (2024). *CLP’s Climate Vision 2050*. CLP.
    * EWING, J. (2016). *Roadmap to a Northeast Asian Carbon Market*. Asia Society Policy Institute.
    * Fortune Business Insights. (2026). Carbon Offsets Market Size, Share & Industry Analysis, By Type (Compliance Market and Voluntary Market), By Project Type (Avoidance/Reduction Projects and Removal/Sequestration Projects), By End-user (Renewable Energy, Forestry and Land, Industrial, Household and Appliances, Transportation, and Others), and Regional Forecast, 2026-2034. In *Fortune Business Insights*. Fortune Business Insights. https://www.fortunebusinessinsights.com/carbon-offsets-market-109080
    * International Carbon Action Partnership. (2025). *Emissions Trading Worldwide: Status Report 2025*. International Carbon Action Partnership.
    * International Energy Agency. (2021). *Net Zero by 2050*. International Energy Agency.
    * Tamellini, L., Marullaz, J., Assous, A., & Barre, C. (2025). *Carbon pricing trends in Asia* (K. Diab, Ed.). Carbon Market Watch.
    * World Economic Forum, & Bain & Company. (2025). *Asia’s Carbon Markets: Strategic Imperatives for Corporations*. World Economic Forum.
    """)

# ==========================================
# 8. 循环驱动
# ==========================================
if st.session_state.is_playing: 
    st.rerun()
