import streamlit as st
from PIL import Image
import json
import base64


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Photo Portfolio Gallery",
    page_icon="📸",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

def set_background(image_bytes):

    encoded = base64.b64encode(image_bytes).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background:
                linear-gradient(
                    rgba(0,0,0,0.45),
                    rgba(0,0,0,0.45)
                ),
                url("data:image/jpeg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .main .block-container {{
            background: rgba(0,0,0,0.15);
            backdrop-filter: blur(8px);
            border-radius: 20px;
            padding-top: 1rem;
        }}

        .preview-container {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )



st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #1e293b 100%
    );
    color: white;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero {
    text-align: center;
    padding: 1rem 0 2rem 0;
}

.hero h1 {
    color: white;
    font-size: 3.5rem;
    font-weight: 800;
}

.hero p {
    color: #cbd5e1;
    font-size: 1.1rem;
}

.reorder-box {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.07);
}

.photo-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    padding: 18px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.15);
    transition: all 0.35s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    margin-bottom: 25px;
}

.photo-card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 25px 60px rgba(0,0,0,0.6);
}

.photo-card img {
    border-radius: 18px;
}

.card-title {
    color: white;
    font-size: 20px;
    font-weight: 700;
    margin-top: 12px;
}

.card-desc {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.6;
}

.stButton button {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class='hero'>
    <h1>📸 My Portfolio Gallery</h1>
    <p>Create beautiful visual stories from your photographs</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "photo_data" not in st.session_state:
    st.session_state.photo_data = {}

if "photo_order" not in st.session_state:
    st.session_state.photo_order = []

if "cover_photo" not in st.session_state:
    st.session_state.cover_photo = None

if "image_sizes" not in st.session_state:
    st.session_state.image_sizes = {}

# NEW: Full-screen background image
if "active_background" not in st.session_state:
    st.session_state.active_background = None

# --------------------------------------------------
# FILE UPLOADER
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Upload Photographs",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if st.session_state.active_background:
    set_background(
        st.session_state.active_background
    )

    c1, c2, c3 = st.columns([4,2,4])

    with c2:

        if st.button(
            "🔍 Full Screen",
            key=f"preview_{uploaded_file.name}"
        ):

            st.session_state.active_background = (
                uploaded_file.getvalue()
            )

            st.rerun()


# --------------------------------------------------
# MAIN APP
# --------------------------------------------------
if uploaded_files:

    file_names = [file.name for file in uploaded_files]

    # Update ordering
    if not st.session_state.photo_order:
        st.session_state.photo_order = file_names

    for name in file_names:
        if name not in st.session_state.photo_order:
            st.session_state.photo_order.append(name)

    st.session_state.photo_order = [
        name
        for name in st.session_state.photo_order
        if name in file_names
    ]

    # ----------------------------------------------
    # GALLERY STATS
    # ----------------------------------------------
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📷 Photos", len(uploaded_files))

    with col2:
        st.metric(
            "📝 Descriptions",
            len([
                item for item in st.session_state.photo_data.values()
                if item.get("description")
            ])
        )

    with col3:
        st.metric("✅ Status", "Ready")

    # ----------------------------------------------
    # PHOTO ORDERING
    # ----------------------------------------------
    st.divider()
    st.subheader("🔄 Reorder Photos")

    for i, name in enumerate(st.session_state.photo_order):

        col1, col2, col3 = st.columns([8, 1, 1])

        with col1:
            st.markdown(
                    f"""
                    <div class="reorder-box">
                    📷 {name}
                    </div>
                    """,
                unsafe_allow_html=True
            )

        with col2:
            if i > 0:
                if st.button("⬆️", key=f"up_{i}"):

                    (
                        st.session_state.photo_order[i],
                        st.session_state.photo_order[i-1]
                    ) = (
                        st.session_state.photo_order[i-1],
                        st.session_state.photo_order[i]
                    )

                    st.rerun()

        with col3:
            if i < len(st.session_state.photo_order) - 1:
                if st.button("⬇️", key=f"down_{i}"):

                    (
                        st.session_state.photo_order[i],
                        st.session_state.photo_order[i+1]
                    ) = (
                        st.session_state.photo_order[i+1],
                        st.session_state.photo_order[i]
                    )

                    st.rerun()

    # ----------------------------------------------
    # PHOTO DETAILS
    # ----------------------------------------------
    st.divider()
    st.subheader("✏️ Add Photo Information")

    for index, uploaded_file in enumerate(uploaded_files):

        if uploaded_file.name not in st.session_state.photo_data:
            st.session_state.photo_data[uploaded_file.name] = {
                "title": uploaded_file.name.rsplit(".", 1)[0],
                "description": ""
            }

        metadata = st.session_state.photo_data[uploaded_file.name]

        with st.expander(
            f"🖼 {uploaded_file.name}",
            expanded=False
        ):

            title = st.text_input(
                "Title",
                value=metadata["title"],
                key=f"title_{index}_{hash(uploaded_file.name)}"
            )

            description = st.text_area(
                "Description",
                value=metadata["description"],
                height=120,
                key=f"desc_{index}_{hash(uploaded_file.name)}"
            )

            st.session_state.photo_data[uploaded_file.name] = {
                "title": title,
                "description": description
            }

    # ----------------------------------------------
    # COLLAGE PREVIEW
    # ----------------------------------------------
    st.divider()

    if st.session_state.active_background:

    st.markdown(
        "<div class='preview-container'>",
        unsafe_allow_html=True
    )

    st.image(
        st.session_state.active_background,
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.subheader("🖼 Portfolio Gallery")

    ordered_files = []

    for filename in st.session_state.photo_order:

        file_match = next(
            (
                f
                for f in uploaded_files
                if f.name == filename
            ),
            None
        )

        if file_match:
            ordered_files.append(file_match)

    cols = st.columns(4)

    for idx, uploaded_file in enumerate(ordered_files):

        image = Image.open(uploaded_file)

        metadata = st.session_state.photo_data.get(
            uploaded_file.name,
            {}
        )

        with cols[idx % 4]:

            st.markdown(
                "<div class='photo-card'>",
                unsafe_allow_html=True
            )

            st.image(
                image,
                use_container_width=True
            )

            st.markdown(
                f"""
                <div class='card-title'>
                {metadata.get("title", uploaded_file.name)}
                </div>

                <div class='card-desc'>
                {metadata.get("description", "")}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    # ----------------------------------------------
    # EXPORT JSON
    # ----------------------------------------------
    st.divider()
    st.subheader("📥 Export Metadata")

    json_data = json.dumps(
        st.session_state.photo_data,
        indent=4
    )

    st.download_button(
        label="📥 Download Metadata JSON",
        data=json_data,
        file_name="photo_metadata.json",
        mime="application/json"
    )

else:

    st.info(
        "👆 Upload one or more photographs to create your professional photo portfolio."
    )