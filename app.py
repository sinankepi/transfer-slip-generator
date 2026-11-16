import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Transfer Slip Generator", layout="centered")
st.title("📝 Transfer Record Generator")
st.write("Type your details below to generate and download your custom transfer receipt.")

# Interactive Form
with st.form("slip_form"):
    amount = st.text_input("Amount", value="10,000.00")
    date = st.text_input("Date", value="16 NOV 2026")
    beneficiary = st.text_input("Beneficiary Name", value="RUKHSANA MOHAMMAD WAHAJUDDIN CHAUDH")
    account_number = st.text_input("Account Number", value="0023100100005189")
    ifsc = st.text_input("IFSC Code", value="PUNB0002310")
    utr = st.text_input("UTR / Transaction ID", value="632018010320")
    submit = st.form_submit_button("Generate Slip")

if submit:
    WIDTH, HEIGHT, BAR_WIDTH = 817, 459, 55
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    # Fonts setup - falls back to system defaults cleanly if specific fonts aren't present
    try:
        regular = ImageFont.truetype("DejaVuSans.ttf", 15)
        bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
        heading = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
        amount_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 43)
    except OSError:
        regular = bold = heading = amount_font = ImageFont.load_default()

    BLUE, DARK, GREY, LINE = "#2057AE", "#172A45", "#687589", "#DCE1E8"

    # LEFT SIDEBAR
    draw.rectangle((0, 0, BAR_WIDTH, HEIGHT), fill=BLUE)
    text_str = "TRANSFER RECORD"
    temp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text_str, font=bold)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    side = Image.new("RGBA", (text_w, text_h + 10), (0, 0, 0, 0))
    side_draw = ImageDraw.Draw(side)
    side_draw.text((0, 0), text_str, font=bold, fill="white")
    side = side.rotate(90, expand=True)
    rotated_w, rotated_h = side.size
    img.paste(side, (int((BAR_WIDTH - rotated_w) / 2), int((HEIGHT - rotated_h) / 2)), side)

    # HEADER
    left, right = 103, 766
    draw.text((left, 45), "AMOUNT TRANSFERRED", font=heading, fill=GREY)
    draw.text((left-3, 70), amount, font=amount_font, fill=BLUE)

    # DETAILS
    draw.line((105, 155, right, 155), fill=BLUE, width=2)
    details = [
        ("Date", date),
        ("Beneficiary name", beneficiary),
        ("Account number", account_number),
        ("IFSC", ifsc),
        ("UTR", utr)
    ]
    y = 180
    for label, val in details:
        draw.text((left, y), label, font=regular, fill=GREY)
        bbox = draw.textbbox((0, 0), val, font=bold)
        text_width = bbox[2] - bbox[0]
        draw.text((right - text_width, y), val, font=bold, fill=DARK)
        y += 55
        draw.line((105, y-17, right, y-17), fill=LINE, width=1)

    # Preview Image inside Web Page
    st.image(img, caption="Preview", use_container_width=True)

    # Provide instant download
    png_buffer = io.BytesIO()
    img.save(png_buffer, format="PNG")
    st.download_button(
        label="📥 Download Receipt Image",
        data=png_buffer.getvalue(),
        file_name=f"{beneficiary.replace(' ', '_')}.png",
        mime="image/png"
    )
