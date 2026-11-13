import datetime
import streamlit as st
import os
import uuid
# ==================== 1. Security (Fixed) ====================
KEY_FILE = "license.key"

def get_machine_id():
    return hex(uuid.getnode())

def generate_password(mid):
    # مطابقة تامة لمنطق أداة فك الحماية الثابتة
    digits = ''.join(filter(str.isdigit, mid))
    if not digits: 
        try:
            digits = str(int(mid, 16))
        except:
            return "Error"
    num = int(digits)
    result = round(abs(num / 2 * 3.14))
    return str(result)[:6]

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = os.path.exists(KEY_FILE)

if not st.session_state['authenticated']:
    st.set_page_config(page_title="Security", layout="centered")
    st.title("Security Activation - Ask the programmer for your password")
    st.warning("Send your Machine ID to programmer email : mulham81ahmed@gmail.com ")

    mid = get_machine_id()
    st.info(f"Machine ID: {mid}")
    pwd = st.text_input("Enter Activation Key:", type="password")
    
    if st.button("Activate"):
        if pwd == generate_password(mid):
            with open(KEY_FILE, "w") as f: 
                f.write(pwd)
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid Activation Key.")
            
    st.stop()


# إعداد صفحة ستريمليت
st.set_page_config(
    page_title="مصفوفة القدر والتاروت",
    page_icon="🔮",
    layout="wide",
)

# تنسيق واجهة المستخدم وتصاميم RTL ودعم اللغة العربية
st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Tahoma', sans-serif;
        background-color: #f8f9fa;
    }
    .main-title {
        text-align: center;
        color: #1a5276;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 30px;
    }
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-right: 6px solid #2980b9;
    }
    .domain-header {
        color: #2c3e50;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 8px;
        margin-top: 15px;
        font-size: 18px;
        font-weight: bold;
    }
    .warning-box {
        background-color: #fdedec;
        border-right: 5px solid #e74c3c;
        padding: 12px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .success-box {
        background-color: #e8f8f5;
        border-right: 5px solid #27ae60;
        padding: 12px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# دالة اختزال الأرقام لتتطابق مع الطاقات الـ 22 الكبرى في مصفوفة القدر والتاروت
def reduce_to_22(n):
  if n <= 22:
    return n if n > 0 else 22
  while n > 22:
    n = sum(int(digit) for digit in str(n))
    if n == 0:
      return 22
  return n


# دالة حساب نقاط المصفوفة الأساسية من تاريخ الميلاد
def calculate_destiny_matrix(birth_date):
  day = birth_date.day
  month = birth_date.month
  year = birth_date.year

  p1 = reduce_to_22(day)  # طاقة يوم الميلاد (الشخصية الظاهرة)
  p2 = reduce_to_22(month)  # طاقة شهر الميلاد (الروحانيات والحدس)
  year_sum = sum(int(d) for d in str(year))
  p3 = reduce_to_22(year_sum)  # طاقة سنة الميلاد (القدر والمسار)

  p4 = reduce_to_22(p1 + p2 + p3)  # الأرضية والجذور
  center = reduce_to_22(p1 + p2 + p3 + p4)  # المركز (طاقة الروح الأساسية)

  money_line = reduce_to_22(p1 + p4 + center)
  love_line = reduce_to_22(p2 + p3 + center)
  health_line = reduce_to_22(p1 + p2 + center)

  return {
      "p1": p1,
      "p2": p2,
      "p3": p3,
      "p4": p4,
      "center": center,
      "money_line": money_line,
      "love_line": love_line,
      "health_line": health_line,
  }


# نظام توليد التحليلات المفصلة للـ 5 مجالات بناءً على طاقة الفترة
def generate_domain_predictions(energy):
  # 1. العاطفة (مع التركيز على الطرف الثالث، عودة المنفصلين، الارتباط)
  if energy in [2, 6, 12, 15, 18]:
    love_text = (
        "<b>العاطفة والارتباط:</b> طاقة هذه الفترة تحمل اختبارات عميقة في العلاقات."
        " هناك احتمالية قوية لـ <b>عودة التواصل مع شخص من الماضي (منفصلين)</b>"
        " نتيجة حنين أو تسوية كارمية، ولكنها تحذر بشدة من ظهور <b>طرف ثالث</b>"
        " يتدخل في الاستقرار أو يثير الشكوك. إن كنت مرتبطاً، فهناك حاجة ملحة"
        " للمصارحة وتجاوز الأسرار الخفية. للمنفردين، هناك فرصة لارتباط مفاجئ يحمل"
        " طابعاً قدرياً."
    )
  elif energy in [3, 9, 14, 17, 19]:
    love_text = (
        "<b>العاطفة والارتباط:</b> فترة مزهرة ومستقرة عاطفياً. طاقات الوئام والانسجام"
        " تسود الأجواء. للمنفصلين، الطاقة تدعم المصالحة الهادئة ونضج الطرف الآخر"
        " في الاعتذار. لا توجد مؤشرات سلبية لتدخل طرف ثالث، بل على العكس، تتجه"
        " العلاقة نحو الترسيم، الخطوبة، أو تجديد عهد الارتباط بطريقة دافئة وواضحة."
    )
  else:
    love_text = (
        "<b>العاطفة والارتباط:</b> تشهد هذه الفترة حركة تنقل واختيارات عاطفية"
        " حاسمة. قد يتطلب الأمر وضع حدود صارمة لبعض العلاقات. إذا كان هناك"
        " انفصال سابق، فالكرة في ملعب الطرف الآخر ليبادر، بينما أنت تميل نحو"
        " الاستقلالية وتقييم ما إذا كان الشريك يستحق فرصة جديدة."
    )

  # 2. العمل
  if energy in [1, 4, 7, 11, 19]:
    work_text = (
        "<b>العمل والمهنة:</b> طاقة تصاعدية قوية، قيادة، وإنجاز استثنائي. فرصة"
        " ممتازة للترقي، تولي مسؤوليات جديدة، أو إطلاق مشروع شخصي كنت تأجله."
        " جهودك السابقة تبدأ تؤتي ثمارها بشكل ملحوظ."
    )
  elif energy in [10, 13, 16, 21]:
    work_text = (
        "<b>العمل والمهنة:</b> فترة تحولات جذرية في بيئة العمل؛ قد تشهد إعادة"
        " هيكلة أو تغيير في طبيعة المهام. احذر من الصراعات الجانبية مع الزملاء"
        " أو الإدارة، وكن مرناً في تقبل التغييرات الإجبارية لأنها ستقودك نحو فرصة"
        " أفضل بكثير."
    )
  else:
    work_text = (
        "<b>العمل والمهنة:</b> استقرار نسبي مع ميل للتأني والبحث عن دراسة"
        " الخطوات القادمة بعمق. تجنب التوقيع على عقود مصيرية دون مراجعة تفصيلية"
        " دقيقة واستشارة أهل الخبرة."
    )

  # 3. المال (مع تحديد مواعيد مالية والتحذير من النصب والخسارة)
  if energy in [3, 10, 19, 21]:
    money_text = (
        "<b>المال والوفرة:</b> انفراجة مالية كبرى وموعد محتمل للحصول على أموال"
        " جديدة (أرباح، مستحقات متأخرة، أو عوائد استثمارية) خلال هذه الفترة."
        " الوفرة تدعمك، ولكن احذر من الإسراف غير المبرر.<br>"
        " <div class='success-box'><b>توقيت مالي إيجابي:</b> الطاقة تدعم توقيع"
        " اتفاقيات مالية مربحة أو بدء استثمار واعد.</div>"
    )
  elif energy in [12, 15, 16, 18]:
    money_text = (
        "<b>المال والوفرة:</b> ⚠️ <b>تحذير مالي حاسم:</b> هذه الطاقة تنذر بمخاطر"
        " عالية تتعلق بالتعرض لعمليات <b>نصب، احتيال، أو خسارة مالية</b> غير متوقعة"
        " نتيجة الثقة المفرطة أو الدخول في استثمار غير مدروس. تجنب تماماً إقراض"
        " الأموال أو الدخول في مضاربات مالية عالية المخاطر خلال هذه الفترة.<br>"
        " <div class='warning-box'><b>تنبيه أمان:</b> امتنع عن توقيع عقود مالية"
        " مجهولة المصدر اليوم أو هذا الشهر.</div>"
    )
  else:
    money_text = (
        "<b>المال والوفرة:</b> وضع مالي متوازن يتطلب منك إدارة الحسابات بحكمة"
        " وتقنين المصروفات. الأموال تأتي بجهد وعمل منتظم ولا توجد أرباح فجائية"
        " ضخمة، لذا حافظ على السيولة النقدية لديك."
    )

  # 4. الصحة
  if energy in [4, 7, 11, 19]:
    health_text = (
        "<b>الصحة والحيوية:</b> طاقة جسدية عالية ونشاط ملحوظ. احرص فقط على توجيه"
        " هذه الطاقة نحو الرياضة وتفريغ التوتر لتجنب الإرهاق العضلي الناتج عن ضغط"
        " العمل."
    )
  elif energy in [12, 13, 18, 20]:
    health_text = (
        "<b>الصحة والحيوية:</b> طاقة منخفضة نسبياً قد تصاحبها اضطرابات في النوم،"
        " شعور بالإرهاق النفسي، أو حساسية موسمية. يُنصح بالراحة التامة، الابتعاد"
        " عن مسببات القلق، ومراجعة الطبيب عند أي أعراض غير مطمئنة."
    )
  else:
    health_text = (
        "<b>الصحة والحيوية:</b> استقرار صحي عام. النظام الغذائي المتوازن وشرب"
        " الماء الكافي هما مفتاح الحفاظ على هذا التوازن طوال الفترة."
    )

  # 5. نصائح أوراق التاروت
  tarot_advice = f"<b>نصيحة أوراق التاروت (طاقة الرقم {energy}):</b> استلهم حكمة هذا الرقم؛ تعامل بمرونة ولا تقاوم التيارات الكونية. استمع لحدسك الداخلي (الكاهنة) ولا تتسرع في حسم القرارات المصيرية قبل اكتمال الصورة لديك."

  return love_text, work_text, money_text, health_text, tarot_advice


# دالة لتوليد ملف HTML للطباعة
def get_html_report(
    title, period_name, name, gender, birth_date, energy, l, w, m, h, t
):
  return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{title} - {name}</title>
        <style>
            body {{ font-family: 'Tahoma', sans-serif; background-color: #fff; color: #222; padding: 40px; line-height: 1.8; text-align: right; direction: rtl; }}
            .container {{ max-width: 800px; margin: auto; border: 1px solid #ccc; padding: 40px; border-radius: 10px; }}
            h1 {{ text-align: center; color: #1a5276; border-bottom: 3px solid #3498db; padding-bottom: 15px; }}
            .meta {{ background: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 25px; border-right: 4px solid #2980b9; }}
            .section {{ margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px; }}
            h3 {{ color: #2980b9; margin-bottom: 8px; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #7f8c8d; border-top: 1px solid #eee; padding-top: 15px; }}
            .print-btn {{ background: #2c3e50; color: white; padding: 10px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; display: block; margin: 20px auto; }}
            @media print {{ .print-btn {{ display: none; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <div class="meta">
                <p><b>اسم المستفيد:</b> {name} | <b>الجنس:</b> {gender} | <b>تاريخ الميلاد:</b> {birth_date}</p>
                <p><b>الفترة المختارة:</b> {period_name} | <b>الطاقة المهيمنة (الرقم):</b> {energy}</p>
            </div>
            <div class="section"><h3>❤️ المجال العاطفي</h3><p>{l}</p></div>
            <div class="section"><h3>💼 المجال المهني والعمل</h3><p>{w}</p></div>
            <div class="section"><h3>💰 المجال المالي والوفرة</h3><p>{m}</p></div>
            <div class="section"><h3>🌿 المجال الصحي</h3><p>{h}</p></div>
            <div class="section"><h3>🔮 نصيحة أوراق التاروت</h3><p>{t}</p></div>
            <button class="print-btn" onclick="window.print()">طباعة التقرير مباشرة</button>
            <div class="footer">جميع الحقوق محفوظة - نظام المستشار الفلكي © 2026</div>
        </div>
    </body>
    </html>
    """


# واجهة الإدخال الجانبية
st.sidebar.header("🎛️ بيانات المستفيد الأساسية")
name = st.sidebar.text_input("الاسم الكريم", "الباحث الروحي")
gender = st.sidebar.selectbox("الجنس", ["ذكر", "أنثى"])
birth_date = st.sidebar.date_input(
    "تاريخ الميلاد",
    datetime.date(2005, 1, 1),
    min_value=datetime.date(1960, 1, 1),
)

# حساب المصفوفة الأساسية
matrix = calculate_destiny_matrix(birth_date)

st.markdown(
    '<h1 class="main-title">🔮 التاروت ومصفوفة القدر - تطوير استرو رادار</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='sub-title'>نظام التوقعات الزمنية المتقدم (السنوية، الشهرية،"
    " الأسبوعية، واليومية) المبني على طاقات الأسرار الكبرى الـ 22.</p>",
    unsafe_allow_html=True,
)

# عرض ملخص طاقات المستخدم الأساسية
st.markdown(
    f"""
<div class="card">
    <h3 style="color: #1a5276; margin-top:0;">الملخص الطاقي للمستفيد: {name}</h3>
    <p><b>طاقة المركز (الروح):</b> {matrix['center']} | <b>طاقة خط المال:</b> {matrix['money_line']} | <b>طاقة خط العواطف:</b> {matrix['love_line']}</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# نظام التبويبات الأربعة (سنوي، شهري، أسبوعي، يومي) مع أزرار البحث والتوليد
# ---------------------------------------------------------
tab_annual, tab_monthly, tab_weekly, tab_daily = st.tabs([
    "📅 التوقعات السنوية",
    "🗓️ التوقعات الشهرية",
    "📊 التوقعات الأسبوعية",
    "⏳ التوقعات اليومية",
])

# 1. تبويب التوقعات السنوية
with tab_annual:
  st.markdown("### 📅 بحث وتوليد التوقعات السنوية")
  selected_year = st.selectbox(
      "اختر السنة المطلوبة:",
      list(range(2026, 2036)),
      key="annual_select",
  )

  if st.button(
      "🔍 بحث وعرض توقعات السنة", key="search_annual", type="primary"
  ):
    year_energy = reduce_to_22(
        matrix["center"] + selected_year + birth_date.day
    )
    l, w, m, h, t = generate_domain_predictions(year_energy)

    st.markdown(
        f"""
        <div class="card">
            <h3 style="color: #2980b9;">تحليلات سنة {selected_year} (طاقة الرقم: {year_energy})</h3>
            <div class="domain-header">❤️ المجال العاطفي</div><p>{l}</p>
            <div class="domain-header">💼 المجال المهني والعمل</div><p>{w}</p>
            <div class="domain-header">💰 المجال المالي والوفرة</div><p>{m}</p>
            <div class="domain-header">🌿 المجال الصحي</div><p>{h}</p>
            <div class="domain-header">🔮 نصيحة أوراق التاروت الكبرى</div><p>{t}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    html_code = get_html_report(
        f"تقرير التوقعات السنوية - {selected_year}",
        f"سنة {selected_year}",
        name,
        gender,
        birth_date,
        year_energy,
        l,
        w,
        m,
        h,
        t,
    )
    st.download_button(
        label="📥 تحميل تقرير السنة (HTML جاهز للطباعة)",
        data=html_code,
        file_name=f"Annual_Report_{selected_year}_{name}.html",
        mime="text/html",
        key="dl_annual",
    )

# 2. تبويب التوقعات الشهرية
with tab_monthly:
  st.markdown("### 🗓️ بحث وتوليد التوقعات الشهرية")
  col_y, col_m = st.columns(2)
  with col_y:
    m_year = st.selectbox(
        "السنة:", list(range(2026, 2031)), key="monthly_year"
    )
  with col_m:
    months_list = [
        "يناير",
        "فبراير",
        "مارس",
        "أبريل",
        "مايو",
        "يونيو",
        "يوليو",
        "أغسطس",
        "سبتمبر",
        "أكتوبر",
        "نوفمبر",
        "ديسمبر",
    ]
    m_month = st.selectbox("الشهر:", months_list, key="monthly_name")

  if st.button(
      "🔍 بحث وعرض توقعات الشهر", key="search_monthly", type="primary"
  ):
    month_idx = months_list.index(m_month) + 1
    month_energy = reduce_to_22(
        matrix["love_line"] + m_year + month_idx + birth_date.month
    )
    l, w, m, h, t = generate_domain_predictions(month_energy)

    st.markdown(
        f"""
        <div class="card">
            <h3 style="color: #2980b9;">تحليلات شهر {m_month} {m_year} (طاقة الرقم: {month_energy})</h3>
            <div class="domain-header">❤️ المجال العاطفي</div><p>{l}</p>
            <div class="domain-header">💼 المجال المهني والعمل</div><p>{w}</p>
            <div class="domain-header">💰 المجال المالي والوفرة</div><p>{m}</p>
            <div class="domain-header">🌿 المجال الصحي</div><p>{h}</p>
            <div class="domain-header">🔮 نصيحة أوراق التاروت الكبرى</div><p>{t}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    html_code = get_html_report(
        f"تقرير التوقعات الشهرية - {m_month} {m_year}",
        f"شهر {m_month} {m_year}",
        name,
        gender,
        birth_date,
        month_energy,
        l,
        w,
        m,
        h,
        t,
    )
    st.download_button(
        label="📥 تحميل تقرير الشهر (HTML جاهز للطباعة)",
        data=html_code,
        file_name=f"Monthly_Report_{m_month}_{m_year}_{name}.html",
        mime="text/html",
        key="dl_monthly",
    )

# 3. تبويب التوقعات الأسبوعية
with tab_weekly:
  st.markdown("### 📊 بحث وتوليد التوقعات الأسبوعية")
  weeks_list = [
      "الأسبوع الأول (1-7)",
      "الأسبوع الثاني (8-14)",
      "الأسبوع الثالث (15-21)",
      "الأسبوع الرابع (22-31)",
  ]
  w_num = st.selectbox("اختر الأسبوع في الشهر:", weeks_list, key="weekly_select")

  if st.button(
      "🔍 بحث وعرض توقعات الأسبوع", key="search_weekly", type="primary"
  ):
    week_idx = weeks_list.index(w_num) + 1
    week_energy = reduce_to_22(
        matrix["center"] + week_idx * 3 + birth_date.day % 10
    )
    l, w, m, h, t = generate_domain_predictions(week_energy)

    st.markdown(
        f"""
        <div class="card">
            <h3 style="color: #2980b9;">تحليلات {w_num} (طاقة الرقم: {week_energy})</h3>
            <div class="domain-header">❤️ المجال العاطفي</div><p>{l}</p>
            <div class="domain-header">💼 المجال المهني والعمل</div><p>{w}</p>
            <div class="domain-header">💰 المجال المالي والوفرة</div><p>{m}</p>
            <div class="domain-header">🌿 المجال الصحي</div><p>{h}</p>
            <div class="domain-header">🔮 نصيحة أوراق التاروت الكبرى</div><p>{t}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    html_code = get_html_report(
        f"تقرير التوقعات الأسبوعية - {w_num}",
        w_num,
        name,
        gender,
        birth_date,
        week_energy,
        l,
        w,
        m,
        h,
        t,
    )
    st.download_button(
        label="📥 تحميل تقرير الأسبوع (HTML جاهز للطباعة)",
        data=html_code,
        file_name=f"Weekly_Report_{week_idx}_{name}.html",
        mime="text/html",
        key="dl_weekly",
    )

# 4. تبويب التوقعات اليومية
with tab_daily:
  st.markdown("### ⏳ بحث وتوليد التوقعات اليومية")
  selected_day_date = st.date_input(
      "اختر التاريخ اليومي:", datetime.date.today(), key="daily_date"
  )

  if st.button("🔍 بحث وعرض توقعات اليوم", key="search_daily", type="primary"):
    day_energy = reduce_to_22(
        matrix["center"]
        + selected_day_date.day
        + selected_day_date.month
        + (selected_day_date.year % 100)
    )
    l, w, m, h, t = generate_domain_predictions(day_energy)

    st.markdown(
        f"""
        <div class="card">
            <h3 style="color: #2980b9;">تحليلات يوم {selected_day_date} (طاقة الرقم: {day_energy})</h3>
            <div class="domain-header">❤️ المجال العاطفي</div><p>{l}</p>
            <div class="domain-header">💼 المجال المهني والعمل</div><p>{w}</p>
            <div class="domain-header">💰 المجال المالي والوفرة</div><p>{m}</p>
            <div class="domain-header">🌿 المجال الصحي</div><p>{h}</p>
            <div class="domain-header">🔮 نصيحة أوراق التاروت الكبرى</div><p>{t}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    html_code = get_html_report(
        f"تقرير التوقعات اليومية - {selected_day_date}",
        str(selected_day_date),
        name,
        gender,
        birth_date,
        day_energy,
        l,
        w,
        m,
        h,
        t,
    )
    st.download_button(
        label="📥 تحميل تقرير اليوم (HTML جاهز للطباعة)",
        data=html_code,
        file_name=f"Daily_Report_{selected_day_date}_{name}.html",
        mime="text/html",
        key="dl_daily",
    )
