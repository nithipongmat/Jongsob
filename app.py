import streamlit as st
import requests
from datetime import datetime, date
import calendar

# ตั้งค่าหน้าเว็บให้เต็มตาและสวยงาม
st.set_page_config(page_title="ระบบจองซ้อมปฏิบัติงาน", page_icon="🏥", layout="centered")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyK0rw7dtoG9hR9WDfFzBrP_uYjXvURAK31cBPBFu4PbYae5CpKAQEIVRfU6F0i--ak5A/exec"

# รายชื่อนักศึกษา 80 กว่าคน
students = [
    "6810001 กชพร คชวงษ์", "6810002 กัญภัท ภัทร์ธาดาโชค", "6810003 กัณฐกะ ปัทมศรีรัตนา",
    "6810004 คุณพงศ์ กังวาลสกุล", "6810005 ชนิภา สุวรรณทา", "6810006 ณัฐกฤตา ห้วยเรไร",
    "6810008 ธนสร วงศ์รัศมีธรรม", "6810009 นพณัฐ หลวงพล", "6810010 นิชาภัทร เนตรสุวรรณ",
    "6810011 นิธิพงษ์ มาทิพย์", "6810012 ปภัชญา ศิรกรวิไล", "6810014 พิมพ์นารา มูลสระดู่",
    "6810015 วรชญา คู่เรืองตระกูล", "6810016 ศิรภัสสร ธิรักษพันธ์", "6810017 ศุภกฤต ศรีเมฆ",
    "6810018 สุทิสสา สุขแสวง", "6810019 สรยุทธ์ พรหมชูแก้ว", "6810020 อิทธิกร กาญจนมุสิก",
    "6810021 กวีกร กสิวิทย์", "6810023 ชญานิศา เทียนแก้ว", "6810024 ชนัญชิดา พุทธประเสริฐ",
    "6810025 ชัญทร กาญจนกิจ", "6810026 ญาณิศา พิกุลทอง", "6810027 ญาณิศา ลาภาอุตม์",
    "6810028 ณัฏฐนันท์ ทรัพย์คงดี", "6810029 ดลฤทัย นันทจันทร์", "6810030 ธนภร สิงห์ภู่",
    "6810031 ธนารักษ์ จตุรงค์พลาธิปัต", "6810032 ธวัลรัตน์ สุภาษี", "6810033 ธิติกาญจน์ ปานทุ่ง",
    "6810034 ปฏิญญา สุทธราพงษ์", "6810035 ปณิธิ สุคันธี", "6810036 ปภังกร ประดิษฐ์วรกุล",
    "6810038 ปานตะวัน ดวงชิน", "6810039 พงค์จักรภัทรติ์ ปานต๊ะรังษี", "6810040 พัทธนันท์ เรืองสิริวุฒิ",
    "6810041 พิชชาพร เจริญศิริ", "6810042 ภัคจิรา ปิยะพันธ์", "6810043 ภาสวิชญ์ ชะเอมไทย",
    "6810044 ภูริทัต โชติทอง", "6810045 ระพีพัชร สายขุน", "6810047 ลลิล ผลศิริ",
    "6810048 วณิชญาณ์ กวางเฉลียว", "6810049 วรธนา กันตอนันตพร", "6810050 หาญชัย สิงหกมล",
    "6810051 อทิติยา ยาตรา", "6810053 ตระการ ดอกบัว", "6810056 กฤตพร วงค์สะทำ",
    "6810057 กฤตยชญ์ ปรัศนียาภรณ์", "6810058 กัลยา อินทร์ติยะ", "6810059 ชญาดา ปิติเจริญพร",
    "6810060 ณภัทร สิทธิพันธุรักษ์", "6810062 ณัฐชนน ศรีอุดร", "6810063 ณัฐณิชา หล้าประพันธ์กุล",
    "6810064 ติณณภพ ณ น่าน", "6810065 ธนภูมิ บัวทิพย์", "6810066 ธัญมน จงฤกษ์งาม",
    "6810067 ธันยพัฒน์ เกรียงพิทักษ์", "6810068 บุณญาพร ศิริศิลป์", "6810069 บุณยาภัค ลอมาเละ",
    "6810070 เบญญาภา ชูทอง", "6810071 ปูริดา อุดมวงศ์", "6810072 พรภาณี มัธยมพงศ์",
    "6810073 พศิน สายวงศ์", "6810074 พองาม พงศทันธรรม", "6810075 พิมพ์มาดา เสถียรพันธฤทธิ์",
    "6810076 ภาสุพล ยอดสุข", "6810077 ภูมิชรินทร์ สารสินพิทักษ์", "6810078วัลลภา ยกเจริญ",
    "6810079 วีณารัตน์ บุญสิริฉาย", "6810080 วุฒินันต์ เลิศศิริวรกุล", "6810081 ศรัญญูย์ หลังพันธุ์",
    "6810082 ศุภณัฐ ปัญจมาสกุล", "6810083 ศุภาพิชญ์ รอดภัย", "6810084 ศุภิสรา ปิ่นชัยมูล",
    "6810085 สมัชญ์ ตีระพิพัฒนกุล", "6810086 สุวรินทร์ คุ้มครองเลิศสิน", "6810087 อภิชญา ศรีชัย",
    "6810088 อันดา มณเฑียรรัตน์", "6810089 ฮาซีซะห์ มะแซ"
]

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- หน้า Login (มีช่องพิมพ์ค้นหาแบบในเรฟ) ----------------
if not st.session_state.user:
    st.markdown("""
        <div style='text-align: center; padding: 30px;'>
            <h2 style='color: #1e1b4b;'>🏥 เข้าสู่ระบบนักศึกษา</h2>
            <p style='color: #64748b; font-size: 14px;'>พิมพ์รหัสนักศึกษา (เช่น 6810011) หรือชื่อ แล้วเลือกจากรายการ</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        search_query = st.text_input("ค้นหารหัสนักศึกษา / ชื่อ-นามสกุล", placeholder="🔍 พิมพ์รหัส 6810... หรือชื่อ...")
        
        if search_query.strip():
            filtered_students = [s for s in students if search_query.lower() in s.lower()]
        else:
            filtered_students = students
        
        selected_student = st.selectbox("เลือกรายชื่อจากผลการค้นหา", ["-- กรุณาเลือกรายชื่อ --"] + filtered_students)
        
        if st.button("เข้าสู่ระบบ", type="primary", use_container_width=True):
            if selected_student != "-- กรุณาเลือกรายชื่อ --":
                st.session_state.user = selected_student
                st.rerun()
            else:
                st.warning("กรุณาเลือกรายชื่อก่อนเข้าสู่ระบบ")
else:
    # ---------------- Header ด้านบนสุด ----------------
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("### 🏥 ระบบจองซ้อมปฏิบัติงาน")
        st.caption("Practical Skill & Equipment Booking System")
    with col_h2:
        st.markdown(f"<div style='background:#312e81; color:white; padding:8px; border-radius:8px; text-align:center; font-size:13px;'><b>{st.session_state.user}</b></div>", unsafe_allow_html=True)
        if st.button("ออกจากระบบ", use_container_width=True):
            st.session_state.user = None
            st.rerun()
            
    st.divider()
    
    @st.cache_data(ttl=2)
    def fetch_data():
        try:
            res = requests.get(GOOGLE_SCRIPT_URL + "?action=getData")
            return res.json()
        except:
            return {
                "rooms": [{"name": "ห้องปฏิบัติการกายภาพบำบัด 1", "date": "2026-10-28", "time": "09:00 - 16:00"}],
                "equipments": [{"name": "Humerus Model", "count": 2, "time": 30}],
                "bookings": []
            }

    data = fetch_data()
    rooms = data.get("rooms", [])
    equipments = data.get("equipments", [])
    bookings = data.get("bookings", [])

    # 4 แท็บหลักด้านบน (ฟีลเด๊ะตามเรฟ)
    tab_home, tab_book, tab_allbooking, tab_mybooking, tab_manage = st.tabs([
        "🏠 หน้าหลัก", 
        "📅 จองซ้อมปฏิบัติ", 
        "📋 การจองทั้งหมด", 
        "👥 คิวของฉัน", 
        "⚙️ จัดการระบบ (Admin)"
    ])

    # ---------------- 1. หน้าหลัก ----------------
    with tab_home:
        # กล่องเวลาเรียลไทม์
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #312e81 0%, #4338ca 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px;'>
                <p style='margin:0; font-size: 13px; opacity: 0.9;'>🕒 เวลาปัจจุบัน</p>
                <h1 style='margin:5px 0 0 0; font-size: 36px;'>{datetime.now().strftime('%H:%M:%S')}</h1>
                <p style='margin:5px 0 0 0; font-size: 14px;'>วัน{datetime.now().strftime('%Aที่ %d %B %Y')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # ปฏิทินรายเดือน
        st.markdown("### 📅 ปฏิทินจองซ้อม")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            cal_year = st.selectbox("ปี", [2026, 2027], index=0)
        with col_m2:
            cal_month = st.selectbox("เดือน", list(range(1, 13)), format_func=lambda x: calendar.month_name[x], index=datetime.now().month - 1)
        
        cal_matrix = calendar.monthcalendar(cal_year, cal_month)
        booked_dates = [b.get('date') for b in bookings]
        
        html_cal = "<table style='width:100%; text-align:center; border-collapse:collapse; background:white; border-radius:8px;'><tr style='background:#f8fafc;'><th style='padding:10px;'>อา</th><th>จ</th><th>อ</th><th>พ</th><th>พฤ</th><th>ศ</th><th>ส</th></tr>"
        for week in cal_matrix:
            html_cal += "<tr>"
            for day in week:
                if day == 0:
                    html_cal += "<td style='padding:12px; color:#cbd5e1;'>-</td>"
                else:
                    d_str = f"{cal_year}-{cal_month:02d}-{day:02d}"
                    has_booking = d_str in booked_dates
                    bg_color = "#d1fae5" if has_booking else "transparent"
                    text_color = "#065f46" if has_booking else "inherit"
                    dot = " 🟢" if has_booking else ""
                    html_cal += f"<td style='padding:12px; background:{bg_color}; color:{text_color}; border:1px solid #f1f5f9;'>{day}{dot}</td>"
            html_cal += "</tr>"
        html_cal += "</table>"
        st.markdown(html_cal, unsafe_allow_html=True)
        st.caption("🟢 มีการเปิดซ้อม/จอง")

        st.divider()
        st.markdown("### 🛏️ ห้องปฏิบัติการที่เปิดซ้อมประจำวัน")
        if rooms:
            for r in rooms:
                st.info(f"📍 ห้อง: {r.get('name')} | เวลา: {r.get('time')}")
        else:
            st.warning("ไม่มีห้องปฏิบัติการเปิดให้บริการในวันที่เลือก")

    # ---------------- 2. จองซ้อมปฏิบัติ ----------------
    with tab_book:
        st.subheader("📅 จองคิวซ้อมปฏิบัติงาน")
        st.caption("เลือกวันที่ คู่ซ้อม และอุปกรณ์ที่ต้องการฝึกซ้อมปฏิบัติ")
        
        with st.form("booking_form", clear_on_submit=True):
            book_date = st.date_input("วันที่ต้องการเข้าซ้อม")
            
            room_names = [r.get('name') for r in rooms] if rooms else ["-- ไม่มีห้องเปิดในวันเลือก --"]
            book_room = st.selectbox("เลือกห้องปฏิบัติการ", room_names)
            
            st.text_input("ผู้จองคนที 1 (ตัวคุณ - ล็อกออโต้)", value=st.session_state.user, disabled=True)
            
            partner_options = ["-- เลือกคู่ซ้อมจากรายชื่อนักศึกษา --"] + [s for s in students if s != st.session_state.user]
            partner_select = st.selectbox("ผู้จองคนที 2 (คู่ซ้อมปฏิบัติ)", partner_options)
            
            eq_names = [eq.get('name') for eq in equipments] if equipments else ["-- ยังไม่มีอุปกรณ์ในระบบ --"]
            chosen_eq = st.selectbox("เลือกอุปกรณ์ซ้อมปฏิบัติ", eq_names)
            
            submitted = st.form_submit_button("ยืนยันการจองคิวซ้อม", type="primary", use_container_width=True)
            if submitted:
                if partner_select == "-- เลือกคู่ซ้อมจากรายชื่อนักศึกษา --":
                    st.warning("กรุณาเลือกคู่ซ้อมปฏิบัติ")
                else:
                    payload = {
                        "action": "book",
                        "user": st.session_state.user,
                        "partner": partner_select,
                        "date": str(book_date),
                        "room": book_room,
                        "equipments": chosen_eq
                    }
                    try:
                        requests.post(GOOGLE_SCRIPT_URL, json=payload)
                        st.success("จองคิวสำเร็จเรียบร้อย!")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")

    # ---------------- 3. การจองทั้งหมด ----------------
    with tab_allbooking:
        st.subheader("📋 ตารางการจองและคู่ที่กำลังซ้อมทั้งหมด")
        if not bookings:
            st.info("ไม่มีรายการจองซ้อมในขณะนี้")
        else:
            for b in bookings:
                with st.container(border=True):
                    st.markdown(f"**📦 อุปกรณ์:** {b.get('equipments')} | **📍 ห้อง:** {b.get('room')}")
                    st.text(f"คู่ซ้อม: {b.get('user')} & {b.get('partner')}")
                    st.caption(f"วันที่: {b.get('date')}")

    # ---------------- 4. คิวของฉัน ----------------
    with tab_mybooking:
        st.subheader("👥 รายการจองซ้อมของฉันและคู่ซ้อม")
        my_bookings = [b for b in bookings if st.session_state.user in b.get('user', '') or st.session_state.user in b.get('partner', '')]
        
        if not my_bookings:
            st.info("คุณยังไม่มีรายการจองซ้อมในระบบ")
        else:
            for b in my_bookings:
                with st.container(border=True):
                    st.markdown(f"**📍 ห้อง:** {b.get('room')} | **📅 วันที่:** {b.get('date')}")
                    st.text(f"ผู้จองหลัก: {b.get('user')} | คู่ซ้อม: {b.get('partner')}")
                    st.caption(f"อุปกรณ์: {b.get('equipments')}")
                    st.markdown("🟢 **สถานะ:** รอดำเนินการ / พร้อมใช้งาน")

    # ---------------- 5. จัดการระบบ (Admin) ----------------
    with tab_manage:
        st.warning("⚠️ โหมดผู้ดูแลระบบ (เปิดสิทธิ์ให้ทุกคน): สมาชิกสามารถเพิ่ม แก้ไข หรือลบข้อมูลห้องและอุปกรณ์ได้ทันที Real-time")
        
        col_mg1, col_mg2 = st.columns(2)
        
        with col_mg1:
            st.markdown("### 🛏️ จัดการเปิดห้องปฏิบัติการ")
            with st.form("room_form", clear_on_submit=True):
                r_name = st.text_input("ชื่อห้องซ้อม", placeholder="เช่น ห้องปฏิบัติการกายภาพ 1")
                r_date = st.date_input("วันที่เปิดซ้อม")
                r_c1, r_c2 = st.columns(2)
                r_start = r_c1.time_input("เวลาเริ่มเปิด", value=datetime.strptime("09:00", "%H:%M").time())
                r_end = r_c2.time_input("เวลาปิด", value=datetime.strptime("16:00", "%H:%M").time())
                
                r_sub = st.form_submit_button("＋ เพิ่มห้องเปิดซ้อม", type="primary", use_container_width=True)
                if r_sub and r_name.strip():
                    payload = {
                        "action": "addRoomDetail",
                        "name": r_name.strip(),
                        "date": str(r_date),
                        "time": f"{r_start.strftime('%H:%M')} - {r_end.strftime('%H:%M')}"
                    }
                    requests.post(GOOGLE_SCRIPT_URL, json=payload)
                    st.success("เพิ่มห้องสำเร็จ!")
                    st.cache_data.clear()
                    st.rerun()

        with col_mg2:
            st.markdown("### 📦 จัดการรายการอุปกรณ์ซ้อม")
            with st.form("eq_form", clear_on_submit=True):
                eq_name = st.text_input("ชื่ออุปกรณ์", placeholder="เช่น ชุดฝึกฉีดยาเข้ากล้ามเนื้อ")
                eq_count = st.number_input("จำนวนที่มี (ชุด/เครื่อง)", min_value=1, value=2)
                eq_time = st.number_input("เวลาซ้อมต่อรอบ (นาที)", min_value=5, value=30)
                
                eq_sub = st.form_submit_button("＋ เพิ่มอุปกรณ์", type="primary", use_container_width=True)
                if eq_sub and eq_name.strip():
                    payload = {
                        "action": "addEquipmentDetail",
                        "name": eq_name.strip(),
                        "count": eq_count,
                        "time": eq_time
                    }
                    requests.post(GOOGLE_SCRIPT_URL, json=payload)
                    st.success("เพิ่มอุปกรณ์สำเร็จ!")
                    st.cache_data.clear()
                    st.rerun()

