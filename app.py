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
        "subtitle": "SIPA 期末项目展示 | 面向气候投资与跨国战略决策",
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

# 创建双标签页
tab1, tab2 = st.tabs(["🌍 世纪地缘沙盘 (Geopolitics Sandbox)", "📊 市场微观数据库 (Market Profiles)"])

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
    st.subheader("📚 亚太区域碳市场微观数据库 (ICAP 2025)")
    st.markdown("本数据库基于 **International Carbon Action Partnership (ICAP) 2025 状态报告** 整理，收录了亚太地区核心国家与地方级碳市场的运作机制。")
    
    # 市场数据库字典
    market_db = {
        "中国 (全国碳市场)": {
            "status": "2021年启动，是全球覆盖排放量最大的碳市场。",
            "coverage": "目前覆盖电力行业（含自备电厂），并计划于2024-2026年逐步扩展至钢铁、水泥和铝冶炼行业。2024年排放总量上限约80亿吨二氧化碳当量，覆盖全国总排放量的60%以上。纳入门槛为年排放量达到26,000吨，2024年覆盖约3,500家单位。",
            "allocation": "目前100%采用基于产量的基准法免费分配，未来计划引入拍卖机制。",
            "offset": "允许使用全国核证自愿减排量（CCER）抵销不超过5%的核查排放量。2024年平均二级市场价格为95.96元人民币。"
        },
        "韩国 (K-ETS)": {
            "status": "2015年启动，是东亚首个全国强制性碳市场。目前正处于向第四版基本计划过渡的重大改革期。",
            "coverage": "2024年排放总量上限为5.67亿吨二氧化碳当量，覆盖韩国约79%的排放量。涵盖电力、工业、交通、航空、废弃物、建筑等行业的816家企业。纳入门槛为年排放超过12.5万吨的公司或2.5万吨的设施。",
            "allocation": "采用祖父法和基准法免费分配，同时对非易受贸易影响行业强制进行至少10%的拍卖，第四阶段将进一步扩大拍卖比例。",
            "offset": "允许使用国内及符合条件的国际抵销信用，上限均为5%。2024年平均二级市场价格为9,238韩元（约6.78美元）。"
        },
        "澳大利亚 (Safeguard Mechanism)": {
            "status": "2023年7月正式启动“保障机制”改革，属于基于排放强度的碳交易体系。",
            "coverage": "涵盖采矿、制造、交通、油气及废弃物等。2022年覆盖排放量为1.387亿吨（占总排放量26%）。门槛为每年直接排放超10万吨，共纳入219家主体。",
            "allocation": "基于实际产量和排放强度的基准法免费分配，基准线每年下降4.9%直至2030年。目前无拍卖。",
            "offset": "可无数量限制使用澳大利亚碳信用（ACCU），超过30%需公开说明。2024财年超排设施可以75澳元（约50美元）购买ACCU。"
        },
        "印度尼西亚 (IDXCarbon)": {
            "status": "2023年启动了基于强度的电力行业碳交易机制。",
            "coverage": "第一阶段涵盖146座25兆瓦及以上燃煤电厂，绝对排放总量上限约为2.57亿吨二氧化碳当量。",
            "allocation": "基于技术排放批准限额（PTBAE）免费分配，首年100%免费，次年降至75-85%，支持拍卖交易。",
            "offset": "允许使用印尼碳减排指标（SPE-GRK）。2024年二级市场抵销信用平均价格约58,800印尼盾（约3.66美元）。"
        },
        "新西兰 (NZ ETS)": {
            "status": "2008年启动，碳排放总量上限与国家2050年净零目标保持一致。",
            "coverage": "2025年绝对上限为1,910万吨。覆盖林业、能源、工业、废弃物等，含4,617个注册主体（多数为林业）。",
            "allocation": "拍卖占据主导（2024年占51%）。高排放且贸易暴露行业（EITE）获部分免费配额，林业直接获得配额。",
            "offset": "目前不允许使用任何抵销信用。2024年平均拍卖价格为64新西兰元（约35.91美元）。"
        },
        "北京 (区域试点)": {
            "status": "2013年11月启动，中国三个由地方人大批准立法的区域碳市场之一。",
            "coverage": "2022年上限约4,400万吨，覆盖全市约30%的排放量，含882家单位。纳入门槛5,000吨。",
            "allocation": "祖父法或基准法免费分配。政府保留不超过5%的配额用于拍卖。",
            "offset": "CCER及BCER抵销上限5%（半数需来自北京）。2024年均价102元人民币。"
        },
        "广东 (区域试点)": {
            "status": "2013年12月启动，是中国规模最大、现货交易量最高的区域碳市场。",
            "coverage": "2023年配额总量2.97亿吨。覆盖九大行业的391家单位。门槛为年排放10,000吨或能耗5,000吨标煤。",
            "allocation": "基准法和祖父法免费分配，首个引入配额拍卖的地方市场。",
            "offset": "CCER和PHCER上限10%（70%需来自本省）。2024年均价51.37元人民币。"
        },
        "上海 (区域试点)": {
            "status": "2013年11月启动，唯一连续100%履约的区域碳市场，金融创新中心。",
            "coverage": "2023年上限1.05亿吨。涵盖工业、建筑、交通等378家单位。电力行业已转至全国碳市场。",
            "allocation": "基准法和祖父法免费分配，辅以固定拍卖。",
            "offset": "CCER和SHCER上限5%，绿电消费可视作零排放。2024年均价75.45元人民币。"
        },
        "日本东京都 (TMG ETS)": {
            "status": "2010年4月启动，全球首个城市级碳市场，与埼玉县链接。",
            "coverage": "2022年核查排放1,120万吨，覆盖约20%城市排放，含1,200个大型建筑及工厂。门槛为消耗150万升原油当量。",
            "allocation": "100%免费分配，结合履约系数（办公楼降至50%）。",
            "offset": "允许使用可再生能源等指标。2024年均价约600日元（约3.96美元）。"
        }
    }

    # 交互式选择器
    selected_market = st.selectbox("📌 请选择要查询的碳市场体系：", list(market_db.keys()))
    
    # 渲染数据卡片
    data = market_db[selected_market]
    st.markdown(f"### {selected_market}")
    st.info(f"**市场现状：** {data['status']}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🏭 覆盖范围 (Coverage)**")
        st.write(data['coverage'])
    with c2:
        st.markdown("**⚖️ 配额与分配 (Allocation)**")
        st.write(data['allocation'])
        
    st.markdown("**🔄 抵销机制与价格 (Offsets & Pricing)**")
    st.success(data['offset'])

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
