import streamlit as st
import requests
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="PTMU Booking System", page_icon="📅", layout="centered")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyK0rw7dtoG9hR9WDfFzBrP_uYjXvURAK31cBPBFu4PbYae5CpKAQEIVRfU6F0i--ak5A/exec"

# รายชื่อนักศึกษาตัวจริงตามที่ระบุ
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
    "6810076 ภาสุพล ยอดสุข", "6810077 ภูมิชรินทร์ สารสินพิทักษ์", "6810078 วัลลภา ยกเจริญ",
    "6810079 วีณารัตน์ บุญสิริฉาย", "6810080 วุฒินันต์ เลิศศิริวรกุล", "6810081 ศรัญญูย์ หลังพันธุ์",
    "6810082 ศุภณัฐ ปัญจมาสกุล", "6810083 ศุภาพิชญ์ รอดภัย", "6810084 ศุภิสรา ปิ่นชัยมูล",
    "6810085 สมัชญ์ ตีระพิพัฒนกุล", "6810086 สุวรินทร์ คุ้มครองเลิศสิน", "6810087 อภิชญา ศรีชัย",
    "6810088 อันดา มณเฑียรรัตน์", "6810089 ฮาซีซะห์ มะแซ"
]

if "user" not in st.session_state:
    st.session_state.user = None

# หน้า Login เลือกรายชื่อ
if not st.session_state.user:
    st.title("🏥 เข้าสู่ระบบจองซ้อม PTMU")
    st.write("เลือกรายชื่อนักศึกษาเพื่อเข้าใช้งานระบบและเชื่อมโยงข้อมูลการจองคู่ของคุณ")
    
    selected_student = st.selectbox("รายชื่อนักศึกษา", ["-- กรุณาเลือกรายชื่อของคุณ --"] + students)
    
    if st.button("เข้าสู่ระบบ", type="primary", use_container_width=True):
        if selected_student != "-- กรุณาเลือกรายชื่อของคุณ --":
            st.session_state.user = selected_student
            st.rerun()
        else:
            st.warning("กรุณาเลือกรายชื่อก่อนเข้าสู่ระบบ")
else:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"👤 ผู้ใช้งาน: **{st.session_state.user}**")
    with col2:
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
                "rooms": ["ห้องปฏิบัติการกายภาพบำบัดหลัก (ตายตัว)"],
                "equipments": ["Humerus Model", "Goniometer", "Reflex Hammer"],
                "bookings": []
            }

    data = fetch_data()
    rooms = data.get("rooms", ["ห้องปฏิบัติการกายภาพบำบัดหลัก (ตายตัว)"])
    equipments = data.get("equipments", ["Humerus Model", "Goniometer"])
    bookings = data.get("bookings", [])

    # 4 แท็บหลักตามบรีฟ
    tab_home, tab_book, tab_mybooking, tab_manage = st.tabs([
        "🏠 หน้าหลัก", 
        "📅 หน้าการจอง", 
        "📋 จัดการการจองของฉัน", 
        "⚙️ จัดการระบบ"
    ])

    # ---------------- 1. หน้าหลัก ----------------
    with tab_home:
        st.subheader("🏠 หน้าหลักระบบซ้อมปฏิบัติการ")
        
        # วันเวลาเรียลไทม์ และห้องที่มีให้ซ้อม
        now_date_str = datetime.now().strftime("%d/%m/%Y")
        now_time_str = datetime.now().strftime("%H:%M:%S")
        st.info(f"📅 **วันที่:** {now_date_str} | 🕒 **เวลาปัจจุบัน:** {now_time_str}")
        
        st.markdown(f"### 🛏️ ห้องฝึกซ้อมวันนี้")
        st.markdown(f"<div style='padding:12px; border:1px solid #cbd5e1; border-radius:8px; background:#f8fafc;'><b>📍 {rooms[0]}</b><br><span style='color:green;'>🟢 เปิดให้บริการช่วงเวลาปกติ</span></div>", unsafe_allow_html=True)

        st.divider()

        # ปฏิทินเช็ควันจอง
        st.markdown("### 📅 ปฏิทินเช็ควันจองซ้อม")
        selected_calendar_date = st.date_input("เลือกดูวันที่ต้องการเช็คคิวจอง")
        
        booked_dates = [b.get('date') for b in bookings]
        matched_bookings = [b for b in bookings if b.get('date') == str(selected_calendar_date)]
        
        if str(selected_calendar_date) in booked_dates:
            st.success(f"🟢 วันที่ {selected_calendar_date} มีการจองแล้ว ({len(matched_bookings)} รายการ)")
            for mb in matched_bookings:
                st.caption(f"- ห้อง: {mb.get('room')} | เวลา: {mb.get('time')} | ผู้จอง: {mb.get('user')} (คู่: {mb.get('partner', '-')})")
        else:
            st.caption(f"⚪ วันที่ {selected_calendar_date} ยังไม่มีการจอง")

        st.divider()

        # สรุปอุปกรณ์ ว่างกี่ชิ้น คิวรอ และเวลาเหลือ
        st.markdown("### 🔬 สถานะอุปกรณ์ส่วนกลาง")
        if equipments:
            for eq in equipments:
                eq_bookings = [b for b in bookings if eq in b.get('equipments', '')]
                queue_count = len(eq_bookings)
                
                with st.container(border=True):
                    c1, c2, c3 = st.columns(3)
                    c1.markdown(f"**📦 อุปกรณ์:** {eq}")
                    c2.markdown(f"👥 **คิวที่รอ:** {queue_count} คิว")
                    
                    if queue_count > 0:
                        remaining_mins = max(0, 60 - (datetime.now().minute % 60))
                        c3.markdown(f"⏱️ **เหลือเวลาอีก:** {remaining_mins} นาที")
                    else:
                        c3.markdown("🟢 **สถานะ:** ว่าง")
                    
                    current_user_using = eq_bookings[0]['user'] if queue_count > 0 else 'ไม่มี'
                    st.caption(f"🕒 กำลังใช้งานโดย: {current_user_using} | เวลารวมต่อรอบ: ตามกำหนด")
        else:
            st.info("ยังไม่มีอุปกรณ์ในระบบ")

    # ---------------- 2. หน้าการจอง ----------------
    with tab_book:
        st.subheader("📅 ทำรายการจองอุปกรณ์และห้องซ้อม")
        with st.form("booking_form"):
            book_date = st.date_input("เลือกวันที่ต้องการจอง")
            book_time = st.text_input("ระบุช่วงเวลา (เช่น 09:00 - 11:30)")
            
            # เลือกคู่ซ้อมจากรายชื่อ 80 คน
            partner_options = ["-- ไม่มีคู่ซ้อม (เดี่ยว) --"] + [s for s in students if s != st.session_state.user]
            partner_select = st.selectbox("เลือกรายชื่อคู่ซ้อม (ถ้ามี)", partner_options)
            
            st.write("เลือกอุปกรณ์ส่วนกลางที่ต้องการใช้งาน:")
            selected_eqs = []
            for eq in equipments:
                if st.checkbox(eq, key=f"eq_{eq}"):
                    selected_eqs.append(eq)
                    
            submitted = st.form_submit_button("ยืนยันการจอง", type="primary", use_container_width=True)
            if submitted:
                if not book_time.strip():
                    st.warning("กรุณาระบุช่วงเวลาที่ต้องการจอง")
                else:
                    payload = {
                        "action": "book",
                        "user": st.session_state.user,
                        "partner": partner_select if partner_select != "-- ไม่มีคู่ซ้อม (เดี่ยว) --" else "-",
                        "date": str(book_date),
                        "time": book_time,
                        "room": rooms[0],
                        "equipments": ", ".join(selected_eqs)
                    }
                    try:
                        requests.post(GOOGLE_SCRIPT_URL, json=payload)
                        st.success("จองสำเร็จเรียบร้อย!")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")

    # ---------------- 3. หน้าจัดการการจองของฉัน ----------------
    with tab_mybooking:
        st.subheader("📋 จัดการการจองของฉัน / รายการที่เกี่ยวข้อง")
        my_bookings = [b for b in bookings if st.session_state.user in b.get('user', '') or st.session_state.user in b.get('partner', '')]
        
        if not my_bookings:
            st.info("คุณยังไม่มีประวัติการจองหรือยังไม่ได้เป็นคู่ซ้อมในขณะนี้")
        else:
            for b in my_bookings:
                with st.container(border=True):
                    st.markdown(f"**📍 ห้อง:** {b.get('room')} | **📅 วันที่:** {b.get('date')} (เวลา: {b.get('time')})")
                    st.text(f"ผู้จองหลัก: {b.get('user')} | คู่ซ้อม: {b.get('partner', '-')}")
                    st.caption(f"อุปกรณ์ที่จอง: {b.get('equipments') or '-'}")
                    st.markdown("🟢 **สถานะ:** กำลังดำเนินการ / รอใช้งาน")

    # ---------------- 4. หน้าจัดการระบบ ----------------
    with tab_manage:
        st.subheader("⚙️ หน้าจัดการระบบ (เพิ่ม/ลดอุปกรณ์ และตั้งค่า)")
        
        new_eq = st.text_input("ชื่ออุปกรณ์ส่วนกลางใหม่", key="new_eq_input")
        if st.button("เพิ่มอุปกรณ์", use_container_width=True):
            if new_eq.strip():
                requests.post(GOOGLE_SCRIPT_URL, json={"action": "addEquipment", "name": new_eq.strip()})
                st.success(f"เพิ่ม {new_eq} สำเร็จ!")
                st.cache_data.clear()
                st.rerun()
                
        st.markdown("#### รายการอุปกรณ์ปัจจุบันในระบบ")
        if equipments:
            for eq in equipments:
                c1, c2 = st.columns([3, 1])
                c1.text(eq)
                if c2.button("ลบ", key=f"del_eq_{eq}"):
                    requests.post(GOOGLE_SCRIPT_URL, json={"action": "deleteEquipment", "name": eq})
                    st.cache_data.clear()
                    st.rerun()
        else:
            st.info("ยังไม่มีอุปกรณ์ในระบบ")
