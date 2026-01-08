# app.py
import hashlib
import json
from datetime import datetime, timezone
from io import BytesIO

import streamlit as st
from PIL import Image
import imagehash

import db


# ---------------------------
# Styling
# ---------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
          /* Layout width + overall typography */
          .block-container { padding-top: 1.25rem; padding-bottom: 3rem; max-width: 1100px; }
          html, body, [class*="css"]  { font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji"; }

          /* Hide Streamlit default menu/footer */
          #MainMenu { visibility: hidden; }
          footer { visibility: hidden; }
          header { visibility: hidden; }

          /* Hero section */
          .hero {
            padding: 28px 26px;
            border-radius: 18px;
            background: radial-gradient(1200px circle at 0% 0%, rgba(99,102,241,0.18), transparent 45%),
                        radial-gradient(1200px circle at 100% 0%, rgba(34,197,94,0.16), transparent 45%),
                        linear-gradient(135deg, rgba(15,23,42,0.98), rgba(30,41,59,0.98));
            border: 1px solid rgba(148,163,184,0.18);
          }
          .hero h1 {
            color: #F8FAFC;
            font-size: 2.0rem;
            line-height: 1.15;
            margin: 0 0 10px 0;
            font-weight: 800;
            letter-spacing: -0.02em;
          }
          .hero p {
            color: rgba(248,250,252,0.85);
            margin: 0;
            font-size: 1.02rem;
            line-height: 1.55;
          }
          .pillrow { margin-top: 14px; display: flex; gap: 8px; flex-wrap: wrap; }
          .pill {
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 0.85rem;
            color: rgba(248,250,252,0.9);
            border: 1px solid rgba(148,163,184,0.22);
            background: rgba(2,6,23,0.25);
          }

          /* Card */
          .card {
            padding: 18px 16px;
            border-radius: 16px;
            border: 1px solid rgba(148,163,184,0.22);
            background: rgba(2,6,23,0.02);
          }
          .card h3 { margin: 0 0 6px 0; font-size: 1.05rem; }
          .muted { color: rgba(15,23,42,0.70); font-size: 0.95rem; line-height: 1.5; }

          /* Make buttons look more “product” */
          div.stButton > button {
            border-radius: 12px !important;
            padding: 0.65rem 1.0rem !important;
            font-weight: 700 !important;
            border: 1px solid rgba(99,102,241,0.35) !important;
          }
          div.stButton > button:hover { transform: translateY(-1px); transition: 0.12s ease; }

          /* Primary button accent */
          button[kind="primary"] {
            background: linear-gradient(135deg, #6366F1, #22C55E) !important;
            border: 0 !important;
          }

          /* Sidebar polish */
          section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(2,6,23,0.95), rgba(15,23,42,0.95));
            border-right: 1px solid rgba(148,163,184,0.15);
          }
          section[data-testid="stSidebar"] * {
            color: rgba(248,250,252,0.92) !important;
          }
          .sidebar-title {
            font-weight: 900;
            letter-spacing: -0.02em;
            font-size: 1.1rem;
            margin-bottom: 0.25rem;
          }
          .sidebar-sub { color: rgba(248,250,252,0.70) !important; font-size: 0.9rem; margin-bottom: 0.75rem; }

          /* Footer */
          .app-footer {
            margin-top: 2.2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(148,163,184,0.25);
            color: rgba(15,23,42,0.65);
            font-size: 0.9rem;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------
# Hashing
# ---------------------------
def sha256_of_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def compute_phash(img: Image.Image) -> str:
    ph = imagehash.phash(img)  # 64-bit default
    return str(ph)


# ---------------------------
# Navigation helpers
# ---------------------------
PAGES = ["🏠 Home", "⚡ Generate Hash", "🗄️ Hash Vault", "ℹ️ About"]

def go(page_label: str) -> None:
    st.session_state["page"] = page_label
    st.rerun()


# ---------------------------
# Pages
# ---------------------------
def page_home() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>SafeHash — Fingerprint Images Without Storing Them</h1>
          <p>
            A privacy-first prototype that generates image fingerprints (hashes) to help detect re-uploads of the same content.
            The long-term vision is enabling <b>hash-sharing</b> with platforms so harmful, non-consensual content can be flagged and removed faster.
          </p>
          <div class="pillrow">
            <div class="pill">🔒 Hashes only (no images stored)</div>
            <div class="pill">⚡ Fast duplicate detection</div>
            <div class="pill">🧪 Built for evaluation + scaling</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns(3)

    # Public-facing impact stats (summarized; sources in About)
    with c1:
        st.markdown(
            """
            <div class="card">
              <h3>📈 Sextortion is rising</h3>
              <div class="muted">NCMEC reported nearly <b>100 financial sextortion reports/day</b> in 2024 (US).</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
              <h3>🧒 Kids are targeted heavily</h3>
              <div class="muted">NCMEC logged <b>546,000 online enticement reports</b> in 2024 (includes sextortion).</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="card">
              <h3>🛡️ Removal can work</h3>
              <div class="muted">Australia’s eSafety scheme reports high success rates for takedown requests.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader("What this demo does")
    left, right = st.columns([1.2, 1.0])

    with left:
        st.markdown(
            """
            **SafeHash** lets someone:
            1. Upload an image (locally / in the app)
            2. Generate two fingerprints:
               - **SHA-256** (exact duplicate detection)
               - **pHash** (perceptual fingerprint, future near-duplicate detection)
            3. Store only the hashes in a database  
            4. If the same image is uploaded again, the app flags **“already exists”**
            """
        )

        st.info("This is a prototype for awareness + engineering demonstration. It does **not** share data with any platform.")
        if st.button("Generate Hash Now →", type="primary"):
            go("⚡ Generate Hash")

    with right:
        total = db.count_images()
        st.markdown(
            f"""
            <div class="card">
              <h3>📦 Your Demo Database</h3>
              <div class="muted">Hashes stored so far:</div>
              <h2 style="margin: 10px 0 0 0;">{total}</h2>
              <div class="muted" style="margin-top:8px;">Tip: upload an image twice to see duplicate detection.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="app-footer">
          <b>Privacy note:</b> This app stores <b>hashes only</b> (no raw images). If you deploy it publicly later, treat uploads as sensitive data.
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_generate() -> None:
    st.subheader("⚡ Generate Hash")

    st.write("Upload an image → generate hashes → store in database → detect duplicates (exact same image).")

    uploaded = st.file_uploader("Upload an image (PNG/JPG/WebP)", type=["png", "jpg", "jpeg", "webp"])

    if uploaded is None:
        st.info("Upload an image to begin.")
        return

    file_bytes = uploaded.getvalue()

    try:
        img = Image.open(BytesIO(file_bytes)).convert("RGB")
    except Exception as e:
        st.error(f"Could not read image: {e}")
        return

    st.image(img, caption=f"Preview: {uploaded.name}", use_container_width=True)

    colA, colB = st.columns([1, 1])
    with colA:
        action = st.button("Create hashes & store", type="primary")
    with colB:
        st.caption("Stores **hashes only** (no image bytes).")

    if action:
        sha256_hex = sha256_of_bytes(file_bytes)
        phash_hex = compute_phash(img)
        now_iso = datetime.now(timezone.utc).isoformat()

        existing = db.find_by_sha256(sha256_hex)
        if existing:
            st.warning("⚠️ Image already uploaded (exact duplicate).")
            st.toast("Duplicate detected.", icon="⚠️")
            with st.expander("View existing record", expanded=True):
                st.json(existing)
            return

        try:
            new_id = db.insert_image(
                filename=uploaded.name,
                uploaded_at_iso=now_iso,
                sha256_hex=sha256_hex,
                phash_hex=phash_hex,
            )
        except Exception as e:
            st.error(f"DB insert failed: {e}")
            return

        st.success("✅ Stored new image fingerprint!")
        st.toast("Hashes saved successfully.", icon="✅")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**SHA-256 (exact):**")
            st.code(sha256_hex)
        with c2:
            st.markdown("**pHash (perceptual):**")
            st.code(phash_hex)

        st.caption(f"Record ID: {new_id}")


def page_vault() -> None:
    st.subheader("🗄️ Hash Vault")
    st.write("Browse stored hashes. Select a record to view details and export.")

    limit = st.slider("Max rows to display", min_value=10, max_value=1000, value=200, step=10)

    rows = db.get_all_images(limit=limit)
    if not rows:
        st.info("Database is empty. Go to Generate Hash and add an image.")
        return

    # Search filter
    q = st.text_input("Search (filename / sha256 / phash)", placeholder="e.g. .png  |  sha  |  db1924...")
    if q.strip():
        qq = q.strip().lower()
        rows = [
            r for r in rows
            if qq in r["filename"].lower()
            or qq in r["sha256"].lower()
            or qq in r["phash"].lower()
        ]

    total_shown = len(rows)
    st.caption(f"Showing {total_shown} record(s), latest first.")

    # Table data (shortened sha for readability)
    table_data = [{
        "id": r["id"],
        "filename": r["filename"],
        "uploaded_at": r["uploaded_at"],
        "sha256": r["sha256"][:12] + "…",
        "phash": r["phash"],
    } for r in rows]

    # Click-select row (with fallback selectbox)
    selected_id = None
    try:
        event = st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        if event and hasattr(event, "selection") and event.selection and event.selection.get("rows"):
            idx = event.selection["rows"][0]
            selected_id = table_data[idx]["id"]
    except TypeError:
        st.dataframe(table_data, use_container_width=True, hide_index=True)

    ids = [r["id"] for r in rows]
    picked = st.selectbox("Select a record to view details", ids, index=0)
    if selected_id is None:
        selected_id = picked

    record = db.get_image_by_id(int(selected_id))
    if not record:
        st.warning("Could not load selected record.")
        return

    st.divider()
    st.markdown("### Record Details")
    st.json(record)

    # Export single record
    record_json = json.dumps(record, indent=2)
    st.download_button(
        "Download record (JSON)",
        data=record_json.encode("utf-8"),
        file_name=f"safehash_record_{record['id']}.json",
        mime="application/json",
    )

    # Export all shown hashes (CSV)
    csv_lines = ["id,filename,uploaded_at,sha256,phash"]
    for r in rows:
        # Basic CSV escaping for commas/quotes
        fn = r["filename"].replace('"', '""')
        csv_lines.append(f'{r["id"]},"{fn}",{r["uploaded_at"]},{r["sha256"]},{r["phash"]}')
    csv_data = "\n".join(csv_lines)

    st.download_button(
        "Export shown hashes (CSV)",
        data=csv_data.encode("utf-8"),
        file_name="safehash_hashes.csv",
        mime="text/csv",
    )


def page_about() -> None:
    st.subheader("ℹ️ About SafeHash")

    st.markdown(
        """
        **What this is:**  
        A demo application that generates and stores **image fingerprints (hashes)** so duplicates can be detected without storing the images themselves.

        **Why it matters (conceptually):**  
        Hash-sharing systems (in principle) can allow platforms to block known harmful content by matching fingerprints, not the raw media.

        **Future work (not implemented):**
        - Platform integration via an API to share hash lists (opt-in, with safety controls)
        - Near-duplicate matching using pHash distance thresholds
        - Abuse-prevention workflows (reporting, verification, audit logs)
        - Stronger privacy model + encryption-at-rest for stored identifiers
        """
    )

    with st.expander("Sources (public reporting)", expanded=True):
        st.markdown(
            """
            - NCMEC “2024 in Numbers” (financial sextortion ~100 reports/day; suicide-linked cases mentioned): https://www.missingkids.org/blog/2025/ncmec-releases-new-data-2024-in-numbers  
            - NCMEC sextortion data (26,718 reports in 2023): https://www.missingkids.org/blog/2024/ncmec-releases-new-sextortion-data  
            - NCMEC CyberTipline Data (546,000 online enticement reports in 2024; 192% increase): https://www.missingkids.org/cybertiplinedata  
            - eSafety (Australia) insights from image-based abuse reporting/removal scheme (reports, extortion share, removal outcomes): https://www.esafety.gov.au/research/insights-from-esafetys-image-based-abuse-reporting-and-removal-scheme
            """
        )

    st.markdown(
        """
        **Disclaimer:** This is a student prototype for learning and demonstration. If deployed publicly, handle uploads as sensitive data and follow legal/ethical guidance.
        """
    )


# ---------------------------
# Main
# ---------------------------
def main() -> None:
    st.set_page_config(page_title="SafeHash", page_icon="🧩", layout="wide", initial_sidebar_state="expanded")
    inject_css()
    db.init_db()

    if "page" not in st.session_state:
        st.session_state["page"] = "🏠 Home"

    with st.sidebar:
        st.markdown('<div class="sidebar-title">🧩 SafeHash</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">Privacy-first image fingerprinting demo</div>', unsafe_allow_html=True)

        chosen = st.radio("Navigate", PAGES, index=PAGES.index(st.session_state["page"]))
        st.session_state["page"] = chosen

        st.markdown("---")
        st.caption("Built with Streamlit • SQLite • SHA-256 • pHash")

    # Page router
    page = st.session_state["page"]
    if page == "🏠 Home":
        page_home()
    elif page == "⚡ Generate Hash":
        page_generate()
    elif page == "🗄️ Hash Vault":
        page_vault()
    else:
        page_about()


if __name__ == "__main__":
    main()
