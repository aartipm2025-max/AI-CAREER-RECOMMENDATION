import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.orchestrator import CareerAdvisorOrchestrator
from agents.input_agent import ValidationError

# Page Configuration
st.set_page_config(
    page_title="AI Career Market Value Advisor",
    page_icon="🎓",
    layout="wide"
)

# Domain to Icon mapping
DOMAIN_ICONS = {
    "Data Science & AI": "🧠",
    "Healthcare": "🏥",
    "Biotechnology": "🧬",
    "Finance & Accounting": "💰",
    "Business": "💼",
    "Management": "📈",
    "Economics": "📊",
    "Psychology": "🎭",
    "Law": "⚖️",
    "Design": "🎨",
    "Technology": "💻",
    "Corporate Governance": "🏢",
    "Media & Communication": "📢",
    "Science & Research": "🔬",
    "Life Sciences": "🌿",
    "Humanities": "📚",
    "Hospitality": "🏨",
    "Public Service": "🏛️",
    "Creative": "🖼️"
}

# Custom CSS for Premium Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        display: none;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main {
        background: #FFE6EB; /* Solid Baby Pink */
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 4rem 1rem 3rem 1rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #1e293b;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .hero-support {
        font-size: 1rem;
        color: #94a3b8;
    }

    /* Input Card */
    .input-card {
        background-color: white;
        padding: 3rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        max-width: 700px;
        margin: 2rem auto 4rem auto;
        text-align: center;
        border: 1px solid #f1f5f9;
    }
    .input-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .input-helper {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.8em;
        background: linear-gradient(90deg, #3A86FF 0%, #8338EC 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s ease;
        margin-top: 1.5rem;
        box-shadow: 0 4px 15px rgba(58, 134, 255, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(58, 134, 255, 0.4);
        filter: brightness(1.1);
        color: white;
        border: none;
    }

    /* Result Card Styling */
    .result-card {
        background-color: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        margin-bottom: 2.5rem;
        border: 1px solid #f1f5f9;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
    }
    .result-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
    }
    
    /* Rank Badges */
    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 1.25rem;
        margin-right: 1.5rem;
    }
    .rank-1 { background: linear-gradient(135deg, #FFD700, #FFA500); color: #78350f; }
    .rank-2 { background: linear-gradient(135deg, #C0C0C0, #808080); color: #334155; }
    .rank-3 { background: linear-gradient(135deg, #CD7F32, #8B4513); color: #fff; }
    .rank-other { background: #3A86FF; color: white; }
    
    .degree-header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
    }
    .degree-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .metric-pill {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #f1f5f9;
        display: flex;
        flex-direction: column;
    }
    .metric-pill-label { font-size: 0.8rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; margin-bottom: 0.25rem;}
    .metric-pill-val { font-size: 1.25rem; font-weight: 700; color: #1e293b; }
    .metric-pill-val.salary { color: #059669; }

    /* Career Intelligence Sub-sections */
    .intel-section {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid #f1f5f9;
    }
    .intel-header {
        font-size: 1rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .tag {
        background: #eff6ff;
        color: #3b82f6;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .tag-skill {
        background: #fdf2f8;
        color: #db2777;
    }
    
    .career-path-stepper {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .step-circle {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #3A86FF;
        flex-shrink: 0;
    }
    .step-text { font-size: 0.95rem; color: #475569; font-weight: 500;}

    /* Chatbot Section */
    .chatbot-card {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        border: 1px solid #f1f5f9;
        padding: 2rem;
        margin-top: 4rem;
    }
    .chat-history {
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
    }
    .chat-msg {
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        max-width: 80%;
    }
    .msg-user { background: #3A86FF; color: white; margin-left: auto; }
    .msg-bot { background: white; color: #1e293b; border: 1px solid #e2e8f0; }

    /* Animation */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    </style>
""", unsafe_allow_html=True)

# Application Logic
def main():
    # Hero Section
    st.markdown('<div class="hero-container"><h1 class="hero-title">🎓 AI Career Market Value Advisor</h1><p class="hero-subtitle">Discover the best degrees based on real labour-market demand.</p><p class="hero-support">For students exploring their future careers.</p></div>', unsafe_allow_html=True)


    # Initialize Orchestrator
    if 'orchestrator' not in st.session_state:
        try:
            st.session_state.orchestrator = CareerAdvisorOrchestrator()
        except Exception as e:
            st.error(f"Failed to initialize system: {e}")
            return

    # Main Layout
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown('<div class="input-card"><div class="input-title">Choose Your Academic Stream</div><div class="input-helper">Select your stream to discover the highest value degree options.</div></div>', unsafe_allow_html=True)
        
        stream_choice = st.selectbox(
            "Stream Selector",
            ["Science", "Commerce", "Arts"],
            label_visibility="collapsed"
        )
        
        st.markdown('<div style="display: flex; justify-content: center; width: 100%;">', unsafe_allow_html=True)
        show_btn = st.button("Show Best Degree Options")
        st.markdown('</div>', unsafe_allow_html=True)

    # Results Section
    if show_btn or 'results' in st.session_state:
        if show_btn:
            with st.spinner(f"🔍 Analyzing the best {stream_choice} degree options..."):
                try:
                    results = st.session_state.orchestrator.run_pipeline(stream_choice, top_n=10)
                    # Diagnostic
                    print(f"DEBUG: Pipeline returned DataFrame with columns: {list(results.columns)}")
                    st.session_state.results = results
                    st.session_state.current_stream = stream_choice
                except ValidationError as e:
                    st.warning(str(e))
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    return

        if 'results' in st.session_state:
            res_df = st.session_state.results
            
            # Critical check for stale data in session state
            if "Domain" not in res_df.columns and "domain" not in res_df.columns:
                print("DEBUG: Stale data detected in session state (missing 'Domain'). Clearing.")
                del st.session_state.results
                st.rerun()

            st.markdown(f"<h2 style='text-align: center; margin-bottom: 3rem;'>Top Ranked Degrees for {st.session_state.current_stream}</h2>", unsafe_allow_html=True)

            col_left, col_mid, col_right = st.columns([1, 5, 1])
            with col_mid:
                all_cards_html = ""
                for idx, row in res_df.iterrows():
                    # Safe extraction with defaults
                    rank = row.get('Rank', row.get('rank', idx + 1))
                    degree = row.get('Degree', row.get('degree', 'Unknown Degree'))
                    salary = row.get('Median Salary', row.get('median_salary_lpa', 'N/A'))
                    growth = row.get('Demand Growth', row.get('demand_growth_percent', 'N/A'))
                    reason = row.get('Reason', row.get('reason', ''))
                    source = row.get('Source', row.get('primary_source', 'Unknown'))
                    domain_val = row.get('Domain', row.get('domain', 'General'))
                    
                    rank_class = f"rank-{rank}" if str(rank).isdigit() and int(rank) <= 3 else "rank-other"
                    domain_icon = DOMAIN_ICONS.get(domain_val, "🎓")
                    
                    # Career Intel
                    job_roles = row.get('Job Roles', row.get('job_roles', []))
                    skills = row.get('Skills', row.get('skills', []))
                    career_path = row.get('Career Path', row.get('career_path', []))
                    
                    roles_html = "".join([f'<span class="tag">{r}</span>' for r in job_roles])
                    skills_html = "".join([f'<span class="tag tag-skill">{s}</span>' for s in skills])
                    path_html = "".join([f'<div class="step"><div class="step-circle"></div><div class="step-text">{p}</div></div>' for p in career_path])

                    # Condensed HTML with Flex Header for Rank + Title
                    card_html = f'<div class="result-card fade-in" style="animation-delay: {idx * 0.1}s;"><div class="degree-header"><div class="rank-badge {rank_class}">#{rank}</div><div class="degree-title">{domain_icon} {degree}</div></div><div class="metrics-grid"><div class="metric-pill"><div class="metric-pill-label">💰 Median Salary</div><div class="metric-pill-val salary">{salary}</div></div><div class="metric-pill"><div class="metric-pill-label">📈 Demand Growth</div><div class="metric-pill-val">{growth}</div></div></div><p style="color: #475569; line-height: 1.6; margin-bottom: 2rem;">{reason}</p><div class="intel-section"><div class="intel-header">💼 Top Career Roles</div><div class="tag-container">{roles_html}</div><div class="intel-header">🛠️ Required Skills</div><div class="tag-container">{skills_html}</div><div class="intel-header">🚀 Career Progression</div><div class="career-path-stepper">{path_html}</div></div><div style="margin-top: 2rem; color: #94a3b8; font-size: 0.85rem; border-top: 1px solid #f1f5f9; padding-top: 1rem;">📄 Source: {source}</div></div>'
                    all_cards_html += card_html
                
                st.markdown(all_cards_html, unsafe_allow_html=True)
                



    # Footer
    st.markdown('<div style="text-align: center; margin-top: 8rem; padding-bottom: 4rem;"><p style="color: #94a3b8; font-size: 0.9rem;">© 2026 AI Career Market Value Advisor. Designed for students aged 15–18.</p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
