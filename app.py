import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# Cấu hình trang
st.set_page_config(layout="wide", page_title="Dice Probability Master")

# CSS để giao diện mượt mà trên điện thoại
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎲 Dice Probability Master v2.0")

# --- LAYOUT CHÍNH ---
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT TRÁI: THIẾT LẬP ---
with col_left:
    st.header("⚙️ Thiết lập")
    num_dice = st.radio("Chọn số xúc xắc:", [1, 2], horizontal=True)
    
    if num_dice == 1:
        events = {
            "Mặt chẵn": lambda x: x[0] % 2 == 0,
            "Số chấm > 4": lambda x: x[0] > 4,
            "Số nguyên tố": lambda x: x[0] in [2, 3, 5],
        }
    else:
        events = {
            "Tổng bằng 7": lambda x: sum(x) == 7,
            "Tổng là số chẵn": lambda x: sum(x) % 2 == 0,
            "Số kép (1-1, 2-2...)": lambda x: x[0] == x[1],
        }
    
    selected_event = st.selectbox("Biến cố cần dự đoán:", list(events.keys()))
    num_trials = st.select_slider("Số lần gieo:", options=[10, 100, 500, 1000], value=100)

    st.divider()
    st.subheader("🎮 Chế độ Trò chơi")
    user_guess = st.slider("Dự đoán xác suất của bạn (%)", 0, 100, 50)
    
    btn_run = st.button("🔥 BẮT ĐẦU GIEO")

# --- CỘT GIỮA: MÔ PHỎNG & ĐỒ THỊ ---
with col_center:
    st.header("🎰 Thực nghiệm")
    if btn_run:
        # Hiệu ứng chờ đợi gieo xúc xắc
        with st.spinner('Đang gieo xúc xắc...'):
            time.sleep(1)
            results = []
            for _ in range(num_trials):
                d1 = random.randint(1, 6)
                d2 = random.randint(1, 6) if num_dice == 2 else None
                results.append((d1, d2) if d2 else (d1,))
            st.session_state.results = results
            st.session_state.num_dice = num_dice

    if 'results' in st.session_state:
        res = st.session_state.results
        df = pd.DataFrame(res)
        
        # Biểu đồ tần suất
        if st.session_state.num_dice == 1:
            data_counts = df[0].value_counts().sort_index().reset_index()
            data_counts.columns = ['Mặt', 'Số lần']
            fig = px.bar(data_counts, x='Mặt', y='Số lần', color='Số lần', title="Tần suất các mặt")
        else:
            df['Tổng'] = df[0] + df[1]
            data_counts = df['Tổng'].value_counts().sort_index().reset_index()
            fig = px.bar(data_counts, x='index', y='Tổng', color='Tổng', title="Tần suất tổng số chấm")
        
        st.plotly_chart(fig, use_container_width=True)

# --- CỘT PHẢI: KẾT QUẢ & ĐIỂM SỐ ---
with col_right:
    st.header("🏆 Kết quả")
    if 'results' in st.session_state:
        check_fn = events[selected_event]
        success_count = sum(1 for r in st.session_state.results if check_fn(r))
        actual_prob = (success_count / num_trials) * 100
        
        # Tính điểm dựa trên độ lệch giữa dự đoán và thực tế
        error = abs(user_guess - actual_prob)
        score = max(0, 100 - int(error))
        
        st.metric("Xác suất thực nghiệm", f"{actual_prob:.1f}%")
        st.metric("Dự đoán của bạn", f"{user_guess}%")
        
        st.subheader(f"⭐ Điểm chính xác: {score}/100")
        
        if score > 90:
            st.balloons()
            st.success("Tuyệt vời! Bạn là bậc thầy xác suất!")
        elif score > 70:
            st.info("Rất tốt! Dự đoán khá sát thực tế.")
        else:
            st.warning("Cố gắng lên! Hãy thử gieo số lần lớn hơn nhé.")

        with st.expander("Giải thích toán học"):
            st.write(f"Trong {num_trials} lần thực nghiệm, biến cố '{selected_event}' xảy ra {success_count} lần.")
            st.latex(r"P(A) \approx \frac{n(A)}{N}")import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time
import base64

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Dice Master 3D Pro")

# --- DỮ LIỆU ÂM THANH (Base64 encode để không cần file mp3 riêng lẻ) ---
# Đây là tiếng xúc xắc ngắn gọn được mã hóa sẵn để nhúng trực tiếp vào code
dice_sound_b64 = """
T2dnUwACAAAAAAAAAABQZnxAAAAAAABH81cBe0JvorU/N2F1ZGkueGlwaC5vcmcvZmxhYy8w
LjEuMy02NmVmNTFjOWEyZGMxYWM5YmI1NGIyZDk1ODFkZWE5OC9lbi53aWtpcGVkaWEub3Jn
L3dpa2kvQXVkaW9fc2lnbmFsX3Byb2Nlc3NpbmcgKEZMQUMpAAEEZW5jb2Rlci1pZCAgPT0g
djEuMS4wIChsaWJmbGFjIDEuMy4yKSAgLyAgc2VyaWFsLTIgPT0gMTEwNjE0ODg1NzAgIC8g
IHByZWRpY3Rvci1vcmRlciAgPT0gOCAgLyAgbWluLXBhcnRpdGlvbi1vcmRlciAgPT0gMCAg
LyAgbWF4LXBhcnRpdGlvbi1vcmRlciAgPT0gOCAgLyAgc2FtcGxlLXJhdGUgID09IDQ0MTAw
ICAvICBjaGFubmVscyAgPT0gMSAgLyAgYml0cy1wZXItc2FtcGxlICA9PSAxNgAgZGF0YQAA
ABcAAABXAAAAZwAAAFwAAABwAAAAWAAAAHIAAABNAAAAcgAAAEkAAAB8AAAAZAAAAJQAAAB/
AAAAoAAAAIcAAACyAAAAmAAAAMQAAACuAAAA4AAAAMIAAADuAAAA3gAAAPUAAAD1AAAA/wAA Let's pretend this is a full dice sound string for brevity. 
Ghi chú: Đoạn mã này là giả lập cho ngắn gọn. Trong thực tế bạn cần một chuỗi base64 mp3/ogg thực sự.
Để code chạy được ngay, tôi sẽ dùng một thủ thuật khác bên dưới.
"""
# HACK: Để đơn giản hóa việc copy-paste và đảm bảo chạy được ngay mà không cần chuỗi base64 dài dòng, 
# chúng ta sẽ dùng một link âm thanh ngắn có sẵn trên mạng.
sound_url = "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3"

def play_sound():
    """Hàm chèn HTML ẩn để phát âm thanh"""
    sound_html = f"""
        <audio autoplay>
        <source src="{sound_url}" type="audio/mpeg">
        Your browser does not support the audio element.
        </audio>
    """
    # Nhúng vào một container rỗng để không hiện trình phát nhạc
    st.empty().markdown(sound_html, unsafe_allow_html=True)

# --- CSS TÙY CHỈNH (Tạo hiệu ứng 3D và Rung lắc) ---
st.markdown("""
    <style>
    /* Định nghĩa hiệu ứng rung lắc khi gieo */
    @keyframes shake {
      0% { transform: translate(1px, 1px) rotate(0deg); }
      10% { transform: translate(-1px, -2px) rotate(-1deg); }
      20% { transform: translate(-3px, 0px) rotate(1deg); }
      30% { transform: translate(3px, 2px) rotate(0deg); }
      40% { transform: translate(1px, -1px) rotate(1deg); }
      50% { transform: translate(-1px, 2px) rotate(-1deg); }
      60% { transform: translate(-3px, 1px) rotate(0deg); }
      70% { transform: translate(3px, 1px) rotate(-1deg); }
      80% { transform: translate(-1px, -1px) rotate(1deg); }
      90% { transform: translate(1px, 2px) rotate(0deg); }
      100% { transform: translate(1px, -2px) rotate(-1deg); }
    }

    /* Class áp dụng hiệu ứng rung */
    .rolling {
        animation: shake 0.5s;
        animation-iteration-count: infinite;
        opacity: 0.7;
    }

    /* Style cho xúc xắc 3D giả lập */
    .dice-3d {
        font-size: 100px;
        color: #d9534f; /* Màu đỏ của xúc xắc */
        text-shadow: 2px 2px 4px #000000, 4px 4px 0px #8c2b29; /* Tạo bóng đổ nổi khối */
        display: inline-block;
        margin: 10px;
        transition: all 0.3s ease;
    }
    
    .final-result {
        transform: scale(1.1); /* Phóng to nhẹ khi ra kết quả cuối */
    }

    .stButton>button { width: 100%; border-radius: 20px; height: 3em; font-weight: bold; background: linear-gradient(to right, #4e54c8, #8f94fb); color: white; border: none;}
    </style>
    """, unsafe_allow_html=True)

# Dictionary ánh xạ số sang icon Unicode
dice_icons = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

st.title("🎲 Dice Master 3D Pro: Thử tài Xác suất")
st.divider()

# --- LAYOUT CHÍNH ---
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT TRÁI: THIẾT LẬP & DỰ ĐOÁN ---
with col_left:
    st.subheader("🛠 Thiết lập & Dự đoán")
    num_dice = st.radio("Số lượng xúc xắc:", [1, 2], horizontal=True, key="num_dice_select")
    
    if num_dice == 1:
        events = {
            "Mặt chẵn": lambda x: x[0] % 2 == 0,
            "Số chấm > 4": lambda x: x[0] > 4,
            "Số nguyên tố (2,3,5)": lambda x: x[0] in [2, 3, 5],
        }
    else:
        events = {
            "Tổng bằng 7": lambda x: sum(x) == 7,
            "Tổng chẵn": lambda x: sum(x) % 2 == 0,
            "Số kép (Hai mặt giống nhau)": lambda x: x[0] == x[1],
        }
    
    selected_event = st.selectbox("Chọn biến cố:", list(events.keys()))
    num_trials = st.select_slider("Số lần gieo (N):", options=[10, 50, 100, 500, 1000], value=50)

    st.write("---")
    st.write("**🎯 Dự đoán của bạn:**")
    user_guess = st.slider("Bạn nghĩ xác suất là bao nhiêu %?", 0, 100, 50, key="guess_slider")
    
    btn_run = st.button("🎲 GIEO NGAY! (Có âm thanh)")

# --- XỬ LÝ LOGIC GIEO VÀ HIỆU ỨNG ---
if btn_run:
    # 1. Tạo placeholder để chứa hình ảnh xúc xắc
    dice_placeholder = col_center.empty()
    
    # 2. Phát âm thanh
    play_sound()
    
    # 3. Hiệu ứng hình ảnh: Vòng lặp thay đổi mặt liên tục (Giả lập đang gieo)
    for _ in range(12): # Chạy 12 khung hình trong khoảng 1.2 giây
        temp_d1 = random.randint(1, 6)
        if num_dice == 2:
            temp_d2 = random.randint(1, 6)
            # Hiển thị icon với class 'rolling' và 'dice-3d'
            dice_placeholder.markdown(f"""
                <div style='text-align: center;' class='rolling'>
                    <span class='dice-3d'>{dice_icons[temp_d1]}</span>
                    <span class='dice-3d'>{dice_icons[temp_d2]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            dice_placeholder.markdown(f"""
                <div style='text-align: center;' class='rolling'>
                    <span class='dice-3d'>{dice_icons[temp_d1]}</span>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(0.1) # Dừng 0.1s mỗi khung hình

    # 4. Tính toán kết quả thực tế sau khi hiệu ứng kết thúc
    final_results = []
    for _ in range(num_trials):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6) if num_dice == 2 else None
        final_results.append((d1, d2) if d2 else (d1,))
    
    st.session_state.final_results = final_results
    st.session_state.last_roll = final_results[-1]

# --- CỘT GIỮA: KẾT QUẢ CUỐI CÙNG & ĐỒ THỊ ---
with col_center:
    # Nếu không phải đang chạy nút bấm mà đã có kết quả trong session
    if not btn_run and 'last_roll' in st.session_state:
         dice_placeholder = st.empty() # Tạo lại placeholder nếu cần

    if 'last_roll' in st.session_state:
        # Hiển thị kết quả mặt cuối cùng (Dừng lại, không rung nữa, thêm class final-result)
        last = st.session_state.last_roll
        if num_dice == 2:
             dice_placeholder.markdown(f"""
                <div style='text-align: center;'>
                    <span class='dice-3d final-result'>{dice_icons[last[0]]}</span>
                    <span class='dice-3d final-result'>{dice_icons[last[1]]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
             dice_placeholder.markdown(f"""
                <div style='text-align: center;'>
                    <span class='dice-3d final-result'>{dice_icons[last[0]]}</span>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")
    # Biểu đồ tần suất (như cũ)
    if 'final_results' in st.session_state:
        df = pd.DataFrame(st.session_state.final_results)
        if num_dice == 1:
            data_counts = df[0].value_counts().sort_index().reset_index()
            data_counts.columns = ['Mặt', 'Số lần']
            fig = px.bar(data_counts, x='Mặt', y='Số lần', color='Số lần', title=f"Tần suất trong {num_trials} lần gieo")
        else:
            df['Tổng'] = df[0] + df[1]
            data_counts = df['Tổng'].value_counts().sort_index().reset_index()
            fig = px.bar(data_counts, x='index', y='Tổng', color='Tổng', title=f"Tần suất Tổng trong {num_trials} lần gieo")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

# --- CỘT PHẢI: TÍNH ĐIỂM & SO SÁNH ---
with col_right:
    st.subheader("🏆 Kết quả & Điểm số")
    if 'final_results' in st.session_state:
        check_fn = events[selected_event]
        success_count = sum(1 for r in st.session_state.final_results if check_fn(r))
        actual_prob = (success_count / num_trials) * 100
        
        # Tính điểm
        error = abs(user_guess - actual_prob)
        score = max(0, 100 - int(error * 1.5)) # Phạt nặng hơn nếu sai số lớn

        st.metric("Xác suất Thực nghiệm (P')", f"{actual_prob:.1f}%", delta=f"{actual_prob - user_guess:.1f}% so với dự đoán")
        
        st.write("---")
        st.write(f"**Độ chính xác dự đoán:** {score}/100 điểm")
        progress_bar = st.progress(score)

        if score >= 90:
            st.balloons()
            st.success("Wow! Trực giác xác suất tuyệt vời! 🎉")
        elif score >= 70:
            st.info("Rất tốt! Bạn dự đoán khá sát. 👍")
        elif score >= 50:
            st.warning("Tạm ổn. Hãy thử tăng số lần gieo xem sao. 🤔")
        else:
            st.error("Chưa chính xác lắm. Xác suất thực tế khác xa dự đoán! 😅")

    else:
        st.info("👈 Đặt dự đoán ở cột bên trái rồi nhấn nút GIEO NGAY!")