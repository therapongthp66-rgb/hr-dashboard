import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าจอ Dashboard
st.set_page_config(page_title="HR Dashboard: วิเคราะห์ค่าตอบแทนและสิทธิประโยชน์", layout="wide")

# ==========================================
# 1. การโหลดและเตรียมข้อมูล (Data Loading & Preprocessing)
# ==========================================
@st.cache_data
def load_data():
    # แก้ไขชื่อไฟล์เป็น data.csv ตามที่กำหนดแล้ว
    file_name = "data.csv"
    df = pd.read_csv(file_name)
    
    # ดึงคอลัมน์ที่เกี่ยวข้องกับค่าตอบแทนและสิทธิประโยชน์
    col_salary_1 = '1. เงินเดือน / ค่าจ้าง หมายถึง ค่าตอบแทนแรงงานที่ ปณท จ่ายให้ผู้ปฏิบัติงานเป็นรายเดือน [1.1 เงินเดือน/ค่าจ้างที่ ปณท จ่ายให้ฉันเหมาะสมกับหน้าที่ที่รับผิดชอบ]'
    col_salary_2 = '1. เงินเดือน / ค่าจ้าง หมายถึง ค่าตอบแทนแรงงานที่ ปณท จ่ายให้ผู้ปฏิบัติงานเป็นรายเดือน [1.2 เงินเดือน/ค่าจ้างที่ ปณท จ่ายให้ฉันเพียงพอกับการดำรงชีพ]'
    col_benefit_1 = '2. สวัสดิการและสิทธิประโยชน์ หมายถึง ค่าตอบแทนและบริการต่าง ๆ ที่ ปณท จัดให้แก่บุคลากร (นอกเหนือจากเงินเดือนค่าจ้าง) เพื่อให้ได้รับความสะดวกสบายในการทำงานมีความมั่นคงในอาชีพมีหลักประกันที่แน่นอนในการดำเนินชีวิต [2.1 สวัสดิการสิทธิประโยชน์และบริการอื่น ๆ ที่ ปณท จัดให้ช่วยอำนวยความสะดวกในการทำงานให้แก่ฉัน]'
    col_benefit_2 = '2. สวัสดิการและสิทธิประโยชน์ หมายถึง ค่าตอบแทนและบริการต่าง ๆ ที่ ปณท จัดให้แก่บุคลากร (นอกเหนือจากเงินเดือนค่าจ้าง) เพื่อให้ได้รับความสะดวกสบายในการทำงานมีความมั่นคงในอาชีพมีหลักประกันที่แน่นอนในการดำเนินชีวิต [2.2 สวัสดิการสิทธิประโยชน์และบริการอื่น ๆ ที่ ปณท จัดให้ สร้างความมั่นคงในอาชีพให้แก่ฉัน]'
    
    # แปลงระดับความพึงพอใจที่เป็นข้อความให้เป็นตัวเลขคะแนน 1-5
    score_mapping = {
        'น้อยที่สุด': 1, 'น้อย': 2, 'ปานกลาง': 3, 'มาก': 4, 'มากที่สุด': 5
    }
    
    df['score_salary_1'] = df[col_salary_1].map(score_mapping)
    df['score_salary_2'] = df[col_salary_2].map(score_mapping)
    df['score_benefit_1'] = df[col_benefit_1].map(score_mapping)
    df['score_benefit_2'] = df[col_benefit_2].map(score_mapping)
    
    return df, col_salary_1, col_benefit_2

# โหลดข้อมูล
df, col_salary_1, col_benefit_2 = load_data()

# ==========================================
# 2. การสร้างเมนูด้านข้างสำหรับกรองข้อมูล (Sidebar Filters)
# ==========================================
st.sidebar.header("🎯 ตัวกรองข้อมูล (Filters)")

# เลือกเฉพาะ 4 ลักษณะงานหลัก
selected_job_types = st.sidebar.multiselect(
    "ลักษณะงาน:",
    options=df['ลักษณะงาน'].dropna().unique(),
    default=['รับฝาก', 'ส่งต่อ', 'นำจ่าย', 'สนับสนุน']
)

# เลือก Generation
selected_gen = st.sidebar.multiselect(
    "กลุ่มอายุ (Generation):",
    options=df['รุ่น (Generation) '].dropna().unique(),
    default=df['รุ่น (Generation) '].dropna().unique()
)

# เลือกสภาพการจ้าง
selected_employ_type = st.sidebar.multiselect(
    "สภาพการจ้าง:",
    options=df['สภาพการจ้าง'].dropna().unique(),
    default=df['สภาพการจ้าง'].dropna().unique()
)

# กรองข้อมูลตามที่ผู้ใช้เลือก
filtered_df = df[
    (df['ลักษณะงาน'].isin(selected_job_types)) &
    (df['รุ่น (Generation) '].isin(selected_gen)) &
    (df['สภาพการจ้าง'].isin(selected_employ_type))
]

# ==========================================
# 3. ส่วนแสดงผล Dashboard (Main Content)
# ==========================================
st.title("📊 Dashboard วิเคราะห์ความพึงพอใจ: ค่าตอบแทนและสิทธิประโยชน์")
st.markdown("เปรียบเทียบมิติข้อมูลตาม **ลักษณะงาน** (รับฝาก, ส่งต่อ, นำจ่าย, สนับสนุน) เพื่อประกอบการตัดสินใจเชิงยุทธศาสตร์")

# แสดงตัวเลขสรุป (KPIs)
st.subheader("ภาพรวมข้อมูลจากตัวกรองที่เลือก")
col1, col2, col3, col4 = st.columns(4)
col1.metric("ผู้ตอบแบบสอบถามทั้งหมด", f"{len(filtered_df):,} คน")
col2.metric("คะแนนเฉลี่ย: ความเหมาะสมของเงินเดือน", f"{filtered_df['score_salary_1'].mean():.2f} / 5")
col3.metric("คะแนนเฉลี่ย: สวัสดิการช่วยอำนวยความสะดวก", f"{filtered_df['score_benefit_1'].mean():.2f} / 5")
col4.metric("คะแนนเฉลี่ย: สวัสดิการสร้างความมั่นคง", f"{filtered_df['score_benefit_2'].mean():.2f} / 5")

st.divider()

# ==========================================
# กราฟที่ 1: เปรียบเทียบคะแนนเฉลี่ยรายลักษณะงาน
# ==========================================
st.subheader("1. เปรียบเทียบคะแนนเฉลี่ยความพึงพอใจ แยกตามลักษณะงาน")

# คำนวณค่าเฉลี่ยของแต่ละลักษณะงาน
avg_scores = filtered_df.groupby('ลักษณะงาน')[['score_salary_1', 'score_salary_2', 'score_benefit_1', 'score_benefit_2']].mean().reset_index()
avg_scores.columns = ['ลักษณะงาน', 'เงินเดือนเหมาะสมกับหน้าที่', 'เงินเดือนเพียงพอต่อการดำรงชีพ', 'สวัสดิการช่วยอำนวยความสะดวก', 'สวัสดิการสร้างความมั่นคง']
avg_scores_melted = avg_scores.melt(id_vars='ลักษณะงาน', var_name='หัวข้อการประเมิน', value_name='คะแนนเฉลี่ย')

fig1 = px.bar(avg_scores_melted, x='ลักษณะงาน', y='คะแนนเฉลี่ย', color='หัวข้อการประเมิน', barmode='group',
             title="เปรียบเทียบคะแนนความพึงพอใจด้านค่าตอบแทนและสวัสดิการ (เต็ม 5 คะแนน)",
             color_discrete_sequence=px.colors.qualitative.Pastel)
fig1.update_yaxes(range=[0, 5])
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ==========================================
# กราฟที่ 2: สัดส่วนความพึงพอใจรายกลุ่ม (Stacked Bar Chart) 
# ==========================================
st.subheader("2. เจาะลึกสัดส่วนการให้คะแนน (Pain Point Analysis)")

analysis_topic = st.selectbox("เลือกหัวข้อเพื่อดูการกระจายตัวของคะแนน:", 
                             ['เงินเดือนเหมาะสมกับหน้าที่ (1.1)', 'สวัสดิการสร้างความมั่นคง (2.2)'])

# เลือกคอลัมน์ให้ตรงกับที่ผู้ใช้เลือกใน Dropdown
col_name = col_salary_1 if analysis_topic == 'เงินเดือนเหมาะสมกับหน้าที่ (1.1)' else col_benefit_2

# นับจำนวนคนในแต่ละระดับความพึงพอใจ แยกตามลักษณะงาน
satisfaction_dist = filtered_df.groupby(['ลักษณะงาน', col_name]).size().reset_index(name='จำนวนคน')

# เรียงลำดับระดับความพึงพอใจให้ถูกต้อง
order = ['น้อยที่สุด', 'น้อย', 'ปานกลาง', 'มาก', 'มากที่สุด']
satisfaction_dist[col_name] = pd.Categorical(satisfaction_dist[col_name], categories=order, ordered=True)
satisfaction_dist = satisfaction_dist.sort_values(by=[col_name])

fig2 = px.bar(satisfaction_dist, x='ลักษณะงาน', y='จำนวนคน', color=col_name,
             title=f"การกระจายตัวของระดับความพึงพอใจ: {analysis_topic}",
             color_discrete_map={'น้อยที่สุด':'#ff4b4b', 'น้อย':'#ff8b8b', 'ปานกลาง':'#ffd166', 'มาก':'#06d6a0', 'มากที่สุด':'#118ab2'},
             category_orders={col_name: order})

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ==========================================
# กราฟที่ 3: ช่องทางการรับรู้สวัสดิการ
# ==========================================
st.subheader("3. ช่องทางการรับรู้สิทธิสวัสดิการ (Communication Channels)")

channel_col = 'ท่านรับรู้สิทธิสวัสดิการและสิทธิประโยชน์ของตัวท่านเองจากช่องทางใดมากที่สุด '
channel_dist = filtered_df.groupby(['ลักษณะงาน', channel_col]).size().reset_index(name='จำนวนคน')

fig3 = px.sunburst(channel_dist, path=['ลักษณะงาน', channel_col], values='จำนวนคน',
                  title="สัดส่วนช่องทางการรับรู้ข้อมูลสวัสดิการ แยกตามลักษณะงาน",
                  color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig3, use_container_width=True)
