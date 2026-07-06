import streamlit as st
from PIL import Image
import json

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
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #1e293b 100%
    );
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
    color:white;
}

.photo-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.35s ease;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    margin-bottom: 25px;
}

.photo-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 18px 45px rgba(0,0,0,0.55);
}

.photo-card img {
    border-radius: 18px;
    transition: transform .35s ease;
}

.photo-card:hover img {
    transform: scale(1.08);
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

.cover-banner {
    border-radius: 30px;
    overflow: hidden;
    margin-bottom: 25px;
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

# --------------------------------------------------
# FILE UPLOADER
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Upload Photographs",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# --------------------------------------------------
# MAIN APP
# --------------------------------------------------
if uploaded_files:

    file_names = [file.name for file in uploaded_files]

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

    # --------------------------------------------------
    # STATS
    # --------------------------------------------------
    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("📷 Photos", len(uploaded_files))

    with c2:
        st.metric(
            "📝 Descriptions",
            len(
                [
                    x for x in st.session_state.photo_data.values()
                    if x.get("description")
                ]
            )
        )

    with c3:
        st.metric("✅ Gallery", "Ready")

    # --------------------------------------------------
    # REORDER
    # --------------------------------------------------
    st.divider()
    st.subheader("🔄 Reorder Photos")

    for i, name in enumerate(st.session_state.photo_order):

        col1, col2, col3 = st.columns([8,1,1])

        with col1:
            st.markdown(
                f"""
                <div class='reorder-box'>
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
            if i < len(st.session_state.photo_order)-1:
                if st.button("⬇️", key=f"down_{i}"):

                    (
                        st.session_state.photo_order[i],
                        st.session_state.photo_order[i+1]
                    ) = (
                        st.session_state.photo_order[i+1],
                        st.session_state.photo_order[i]
                    )

                    st.rerun()

    # --------------------------------------------------
    # PHOTO INFO
    # --------------------------------------------------
    st.divider()
    st.subheader("✏️ Add Photo Information")

    for idx, uploaded_file in enumerate(uploaded_files):

        if uploaded_file.name not in st.session_state.photo_data:

            st.session_state.photo_data[uploaded_file.name] = {
                "title": uploaded_file.name.rsplit(".",1)[0],
                "description": ""
            }

        metadata = st.session_state.photo_data[uploaded_file.name]

        with st.expander(f"🖼 {uploaded_file.name}"):

            title = st.text_input(
                "Title",
                value=metadata["title"],
                key=f"title_{idx}_{uploaded_file.name}"
            )

            description = st.text_area(
                "Description",
                value=metadata["description"],
                key=f"desc_{idx}_{uploaded_file.name}",
                height=120
            )

            st.session_state.photo_data[uploaded_file.name] = {
                "title": title,
                "description": description
            }

    # --------------------------------------------------
    # COVER IMAGE
    # --------------------------------------------------
    if st.session_state.cover_photo:

        cover_file = next(
            (
                f for f in uploaded_files
                if f.name == st.session_state.cover_photo
            ),
            None
        )

        if cover_file:

            st.divider()

            st.markdown("## 🌟 Cover Photograph")

            st.image(
                cover_file,
                use_container_width=True
            )

    # --------------------------------------------------
    # GALLERY
    # --------------------------------------------------
    st.divider()
    st.subheader("🖼 Portfolio Gallery")

    ordered_files = []

    for fname in st.session_state.photo_order:

        obj = next(
            (
                f for f in uploaded_files
                if f.name == fname
            ),
            None
        )

        if obj:
            ordered_files.append(obj)

    cols = st.columns(4)

    for idx, uploaded_file in enumerate(ordered_files):

        image = Image.open(uploaded_file)

        metadata = st.session_state.photo_data.get(
            uploaded_file.name,
            {}
        )

        if uploaded_file.name not in st.session_state.image_sizes:
            st.session_state.image_sizes[
                uploaded_file.name
            ] = 250

        with cols[idx % 4]:

            st.markdown(
                "<div class='photo-card'>",
                unsafe_allow_html=True
            )

            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    "🌟 Cover",
                    key=f"cover_{uploaded_file.name}"
                ):
                    st.session_state.cover_photo = (
                        uploaded_file.name
                    )
                    st.rerun()

            with b2:

                st.download_button(
                    "⬇ Download",
                    data=uploaded_file.getvalue(),
                    file_name=uploaded_file.name,
                    mime="image/jpeg",
                    key=f"dl_{uploaded_file.name}"
                )

            size = st.slider(
                "Image Size",
                150,
                700,
                st.session_state.image_sizes[
                    uploaded_file.name
                ],
                key=f"size_{uploaded_file.name}"
            )

            st.session_state.image_sizes[
                uploaded_file.name
            ] = size

            st.image(
                image,
                width=size
            )

            if st.button(
                "🔍 Full Screen",
                key=f"preview_{uploaded_file.name}"
            ):
                st.image(
                    image,
                    use_container_width=True
                )

            st.markdown(
                f"""
                <div class='card-title'>
                {metadata.get("title","")}
                </div>

                <div class='card-desc'>
                {metadata.get("description","")}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    # --------------------------------------------------
    # EXPORT JSON
    # --------------------------------------------------
    st.divider()

    json_data = json.dumps(
        st.session_state.photo_data,
        indent=4
    )

    st.download_button(
        "📥 Download Metadata JSON",
        json_data,
        "photo_metadata.json",
        "application/json"
    )

else:

    st.info(
        "👆 Upload one or more photographs to start building your portfolio gallery."
    )