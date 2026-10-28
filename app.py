import streamlit as st
import requests
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="PTMU Booking System", page_icon="📅", layout="centered")

# ลิงก์ Google Apps Script ของคุณ
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyK0rw7dtoG9hR9WDfFzBrP_uYjXvURAK31cBPBFu4PbYae5CpKAQEIVRfU6F0i--ak5A/exec"

# สร้างรายชื่อนักศึกษา 80 คน (รหัส 6810001 - 6810080)
students = [f"68100{i:02d} - นศ.กายภาพบำบัดคนที่ {i}" for i in range(1, 81)]

# จัดการ Login ด้วย session_state
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("🏥 เข้าสู่ระบบจองซ้อม PTMU")
    st.write("เลือกรายชื่อนักศึกษา (80 คน) เพื่อเข้าใช้งานระบบจองเตียงและอุปกรณ์")
    
    selected_student = st.selectbox("รายชื่อนักศึกษา", ["-- กรุณาเลือกรายชื่อของคุณ --"] + students)
    
    if st.button("เข้าสู่ระบบ", type="primary", use_container_width=True):
        if selected_student != "-- กรุณาเลือกรายชื่อของคุณ --":
            st.session_state.user = selected_student
            st.rerun()
        else:
            st.warning("กรุณาเลือกรายชื่อก่อนเข้าสู่ระบบ")
else:
    # Header & Logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"👤 ผู้ใช้งาน: **{st.session_state.user}**")
    with col2:
        if st.button("ออกจากระบบ", use_container_width=True):
            st.session_state.user = None
            st.rerun()
            
    st.divider()
    
    # ดึงข้อมูลจาก Google Apps Script
    @st.cache_data(ttl=2)
    def fetch_data():
        try:
            res = requests.get(GOOGLE_SCRIPT_URL + "?action=getData")
            return res.json()
        except:
            return {
                "rooms": ["เตียงซ้อมที่ 1", "เตียงซ้อมที่ 2", "ห้องปฏิบัติการย่อย A"],
                "equipments": ["Humerus Model", "Goniometer", "Reflex Hammer"],
                "bookings": []
            }

    data = fetch_data()
    rooms = data.get("rooms", ["เตียงซ้อมที่ 1", "เตียงซ้อมที่ 2"])
    equipments = data.get("equipments", ["Humerus Model", "Goniometer"])
    bookings = data.get("bookings", [])

    # ================= PAGE: หน้าหลัก & Dashboard =================
    st.subheader("🏠 หน้าหลักระบบซ้อมปฏิบัติการ")
    
    # 1. แสดง วัน-เวลา ปัจจุบันแบบเรียลไทม์ และห้องที่มีให้ซ้อม
    st.info(f"🕒 **เวลาปัจจุบัน:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    st.markdown("### 🛏️ ห้อง/เตียงฝึกซ้อมที่มีให้บริการ")
    if rooms:
        cols = st.columns(min(len(rooms), 3))
        for idx, room in enumerate(rooms):
            with cols[idx % len(cols)]:
                st.markdown(f"<div style='padding:10px; border:1px solid #cbd5e1; border-radius:8px; text-align:center; background:#f8fafc;'><b>{room}</b><br><span style='color:green; font-size:12px;'>🟢 พร้อมใช้งาน</span></div>", unsafe_allow_html=True)
    else:
        st.warning("ยังไม่มีห้องในระบบ")

    st.divider()

    # 2. ปฏิทิน / วันที่มีคนจอง (จำลองจุดเขียวบอกวันที่มีการจอง)
    st.markdown("### 📅 ตรวจสอบวันที่มีการจอง")
    selected_calendar_date = st.date_input("เลือกดูวันที่ต้องการเช็คคิวจอง")
    
    booked_dates = [b.get('date') for b in bookings]
    matched_bookings = [b for b in bookings if b.get('date') == str(selected_calendar_date)]
    
    if str(selected_calendar_date) in booked_dates:
        st.success(f"🟢 วันที่ {selected_calendar_date} มีการจองแล้ว ({len(matched_bookings)} รายการ)")
    else:
        st.caption(f"⚪ วันที่ {selected_calendar_date} ยังไม่มีการจอง")

    st.divider()

    # 3. สถานะอุปกรณ์ส่วนกลาง คิว และเวลาคงเหลือ
    st.markdown("### 🔬 สถานะอุปกรณ์ส่วนกลางและคิวใช้งาน")
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
                    c3.markdown("🟢 **สถานะ:** ว่าง (พร้อมหยิบใช้)")
                
                st.caption(f"🕒 เวลารวมการใช้งานต่อรอบ: 60 นาที | คิวล่าสุด: {eq_bookings[-1]['user'] if queue_count > 0 else 'ไม่มี'}")
    else:
        st.info("ยังไม่มีอุปกรณ์ส่วนกลางในระบบ")

    st.divider()

    # ================= TABS เมนูการใช้งาน =================
    tab1, tab2, tab3 = st.tabs(["📅 ทำรายการจอง", "📋 ตารางการจองทั้งหมด", "⚙️ จัดการห้อง/อุปกรณ์"])
    
    with tab1:
        st.subheader("ทำรายการจองเตียง/อุปกรณ์")
        with st.form("booking_form"):
            book_date = st.date_input("เลือกวันที่ต้องการจอง")
            book_time = st.selectbox("เลือกรอบเวลา", ["09:00 - 12:00", "13:00 - 16:00", "16:00 - 19:00"])
            book_room = st.selectbox("เลือกห้อง / เตียงฝึกซ้อม", rooms if rooms else ["-- ไม่มีห้องในระบบ --"])
            
            st.write("เลือกอุปกรณ์ส่วนกลางเพิ่มเติม (ถ้ามี):")
            selected_eqs = []
            for eq in equipments:
                if st.checkbox(eq, key=f"eq_{eq}"):
                    selected_eqs.append(eq)
                    
            submitted = st.form_submit_button("ยืนยันการจอง", type="primary", use_container_width=True)
            if submitted:
                if not book_room or book_room.startswith("--"):
                    st.warning("กรุณาเลือกห้อง/เตียงซ้อม")
                else:
                    payload = {
                        "action": "book",
                        "user": st.session_state.user,
                        "date": str(book_date),
                        "time": book_time,
                        "room": book_room,
                        "equipments": ", ".join(selected_eqs)
                    }
                    try:
                        requests.post(GOOGLE_SCRIPT_URL, json=payload)
                        st.success("จองสำเร็จเรียบร้อย!")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")

    with tab2:
        st.subheader("ตารางการจองทั้งหมด")
        if not bookings:
            st.info("ยังไม่มีรายการจองในขณะนี้")
        else:
            for b in bookings:
                with st.container(border=True):
                    st.markdown(f"**📍 ห้อง/เตียง:** {b.get('room')} | **📅 วันที่:** {b.get('date')} ({b.get('time')})")
                    st.text(f"ผู้จอง: {b.get('user')}")
                    st.caption(f"อุปกรณ์เสริม: {b.get('equipments') or '-'}")

    with tab3:
        st.subheader("จัดการห้องและอุปกรณ์ส่วนกลาง (ทุกคนกดเพิ่ม/ลบได้)")
        col_r, col_e = st.columns(2)
        
        with col_r:
            st.markdown("### เพิ่มห้องใหม่")
            new_room = st.text_input("ชื่อห้อง/เตียงซ้อม", key="new_room_input")
            if st.button("เพิ่มห้อง", use_container_width=True):
                if new_room.strip():
                    requests.post(GOOGLE_SCRIPT_URL, json={"action": "addRoom", "name": new_room.strip()})
                    st.success(f"เพิ่ม {new_room} สำเร็จ!")
                    st.cache_data.clear()
                    st.rerun()
            
            st.markdown("#### รายการห้องปัจจุบัน")
            for r in rooms:
                c1, c2 = st.columns([3, 1])
                c1.text(r)
                if c2.button("ลบ", key=f"del_r_{r}"):
                    requests.post(GOOGLE_SCRIPT_URL, json={"action": "deleteRoom", "name": r})
                    st.cache_data.clear()
                    st.rerun()

        with col_e:
            st.markdown("### เพิ่มอุปกรณ์ใหม่")
            new_eq = st.text_input("ชื่ออุปกรณ์ส่วนกลาง", key="new_eq_input")
            if st.button("เพิ่มอุปกรณ์", use_container_width=True):
                if new_eq.strip():
                    requests.post(GOOGLE_SCRIPT_URL, json={"action": "addEquipment", "name": new_eq.strip()})
                    st.success(f"เพิ่ม {new_eq} สำเร็จ!")
                    st.cache_data.clear()
                    st.rerun()
                    
            st.markdown("#### รายการอุปกรณ์ปัจจุบัน")
            for eq in equipments:
                c1, c2 = st.columns([3, 1])
                c1.text(eq)
                if c2.button("ลบ", key=f"del_eq_{eq}"):
                    requests.post(GOOGLE_SCRIPT_URL, json={"action": "deleteEquipment", "name": eq})
                    st.cache_data.clear()
                    st.rerun()
