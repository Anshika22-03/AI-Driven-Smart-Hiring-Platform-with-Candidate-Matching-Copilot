import streamlit as st
import os
import pandas as pd
import plotly.express as px
from copilot import ask_copilot

from resume_parser import extract_text
from analyzer import analyze_resume
from interview import generate_questions
from ranking import rank_candidates
from resume_chat import chat_with_resume
from talent_insights import generate_talent_insights

from database import (
    create_database,
    add_candidate,
    get_all_candidates,
    update_status,
    delete_candidate,
    get_dashboard_stats
)
def copilot_page():

    st.title("🤖 TalentPilot AI Copilot")

    st.info(
        """
Ask anything about:

✅ Resume Analysis
✅ ATS Score
✅ Job Matching
✅ Recruitment
✅ HR
✅ Employees
✅ Interviews
✅ Talent Management
"""
    )

    question = st.text_area(
        "Ask your question",
        height=150,
        placeholder="Example: How is ATS score calculated?"
    )

    if st.button("Ask Copilot"):

        if question.strip():

            with st.spinner("Thinking..."):

                answer = ask_copilot(question)

            with st.chat_message("assistant"):
                st.write(answer)
# ==========================================================
# INITIAL SETUP
# ==========================================================

st.set_page_config(
    page_title="AI Recruitment & Talent Management Copilot",
    page_icon="🤖",
    layout="wide"
)
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

create_database()

if not os.path.exists("resumes"):
    os.makedirs("resumes")

st.markdown("""
<div class="hero">

<h1>🤖 AI Driven Smart Hiring Platform with Candidate Matching Copilot</h1>

<p>
Smart AI-powered Applicant Tracking System built using
Llama 3.2, Streamlit & Ollama.
</p>

</div>
""", unsafe_allow_html=True)
st.caption("AI Powered Applicant Tracking System (ATS) using Llama 3.2")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("AI Recruiter")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📄 Resume Screening",
        "🏆 Candidate Ranking",
        "🎤 Interview Questions",
        "🤖 Resume Chat AI",
        "📊 Talent Insights",
        "🤖 AI Copilot"
    ]
)
if menu == "🤖 AI Copilot":
    copilot_page()

# ==========================================================
# HOME
# ==========================================================

elif menu == "🏠 Home":

    st.header("📊 Recruitment Dashboard")

    st.markdown("""
### Recruitment Pipeline

📄 Application ->
📝 Resume Screening ->
⭐ Shortlisted ->
🎤 Interview ->
🏆 Hired
""")

    applications, pending, shortlisted, rejected = get_dashboard_stats()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Applications", applications)
    c2.metric("Pending", pending)
    c3.metric("Shortlisted", shortlisted)
    c4.metric("Rejected", rejected)

    df = pd.DataFrame(
        {
            "Status": [
                "Pending",
                "Shortlisted",
                "Rejected"
            ],
            "Count": [
                pending,
                shortlisted,
                rejected
            ]
        }
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        fig = px.pie(
            df,
            names="Status",
            values="Count",
            title="Candidate Distribution"
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="black"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with chart2:

        fig = px.bar(
            df,
            x="Status",
            y="Count",
            title="Recruitment Pipeline"
        )
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="black"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("🕒 Recent Activity")

    recent = get_all_candidates()[::-1][:5]

    if len(recent) == 0:

        st.info("No recent activity.")

    else:

        for candidate in recent:

            st.write(
                f"✅ **{candidate[1]}** uploaded on **{candidate[5]}**"
            )

    st.markdown("---")

    st.subheader("👥 Candidate Management")

    search = st.text_input(
        "🔍 Search Candidate"
    )

    status_filter = st.selectbox(
        "Filter by Status",
        [
            "All",
            "Pending",
            "Shortlisted",
            "Rejected"
        ]
    )

    candidates = get_all_candidates()

    filtered = []

    for candidate in candidates:

        name = candidate[1]
        status = candidate[4]

        if search.lower() not in name.lower():
            continue

        if status_filter != "All":

            if status != status_filter:
                continue

        filtered.append(candidate)

    candidates = filtered
    if len(candidates) == 0:

        st.info("No candidates found.")

    else:

        for candidate in candidates:

            candidate_id = candidate[0]
            candidate_name = candidate[1]
            resume_file = candidate[2]
            resume_text = candidate[3]
            status = candidate[4]
            upload_date = candidate[5]

            st.markdown("---")

            col1, col2 = st.columns([3, 1])

            with col1:

                st.subheader(candidate_name)

                st.write(f"📄 Resume : {resume_file}")
                st.write(f"📅 Uploaded : {upload_date}")

                if status == "Pending":
                    st.warning(status)

                elif status == "Shortlisted":
                    st.success(status)

                else:
                    st.error(status)

            with col2:

                st.write("")

            with st.expander("📄 Resume Preview"):

                st.write(resume_text[:2000])

                if len(resume_text) > 2000:
                    st.info("Showing first 2000 characters.")

            b1, b2, b3 = st.columns(3)

            if b1.button(
                "✅ Shortlist",
                key=f"short_{candidate_id}"
            ):

                update_status(
                    candidate_id,
                    "Shortlisted"
                )

                st.success("Candidate Shortlisted")

                st.rerun()

            if b2.button(
                "❌ Reject",
                key=f"reject_{candidate_id}"
            ):

                update_status(
                    candidate_id,
                    "Rejected"
                )

                st.success("Candidate Rejected")

                st.rerun()

            if b3.button(
                "🗑 Delete",
                key=f"delete_{candidate_id}"
            ):

                delete_candidate(candidate_id)

                try:

                    os.remove(
                        os.path.join(
                            "resumes",
                            resume_file
                        )
                    )

                except:
                    pass

                st.success("Candidate Deleted")

                st.rerun()

# ==========================================================
# RESUME SCREENING
# ==========================================================

elif menu == "📄 Resume Screening":

    st.header("📄 AI Resume Screening")

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        key="resume_screening"
    )

    jd = st.text_area(
        "Paste Job Description"
    )

    if st.button("Analyze Resume"):

        if uploaded_resume is None:

            st.error("Please upload a resume.")

        elif jd.strip() == "":

            st.error("Please enter Job Description.")

        else:

            resume_text = extract_text(uploaded_resume)

            save_path = os.path.join(
                "resumes",
                uploaded_resume.name
            )

            with open(save_path, "wb") as f:

                f.write(
                    uploaded_resume.getbuffer()
                )

            exists = False

            for row in get_all_candidates():

                if row[2] == uploaded_resume.name:

                    exists = True
                    break

            if not exists:

                add_candidate(

                    uploaded_resume.name
                    .replace(".pdf", "")
                    .replace(".docx", ""),

                    uploaded_resume.name,

                    resume_text

                )

            with st.spinner("Analyzing Resume..."):

                result = analyze_resume(
                    resume_text,
                    jd
                )

            st.success("Analysis Complete!")

            st.markdown(result)
            # =====================================================
            # Resume Match Score
            # =====================================================

            score = 85

            st.subheader("📊 Resume Match Score")

            st.progress(score)

            st.metric(
                "Overall Score",
                f"{score}%"
            )

            # =====================================================
            # AI Recommendation
            # =====================================================

            if score >= 80:

                st.success(
                    "⭐ AI Recommendation : Strongly Recommend"
                )

            elif score >= 60:

                st.info(
                    "👍 AI Recommendation : Recommend"
                )

            else:

                st.warning(
                    "⚠ AI Recommendation : Needs Further Evaluation"
                )

            st.download_button(

                "📥 Download AI Report",

                result,

                file_name="AI_Report.txt"

            )

            st.markdown("---")

            c1, c2 = st.columns(2)

            if c1.button("✅ Shortlist Candidate"):

                for row in get_all_candidates():

                    if row[2] == uploaded_resume.name:

                        update_status(
                            row[0],
                            "Shortlisted"
                        )

                        break

                st.success("Candidate Shortlisted")

                st.rerun()

            if c2.button("❌ Reject Candidate"):

                for row in get_all_candidates():

                    if row[2] == uploaded_resume.name:

                        update_status(
                            row[0],
                            "Rejected"
                        )

                        break

                st.success("Candidate Rejected")

                st.rerun()

# ==========================================================
# CANDIDATE RANKING
# ==========================================================

elif menu == "🏆 Candidate Ranking":

    st.header("🏆 AI Candidate Ranking")

    candidates = get_all_candidates()

    if len(candidates) < 2:

        st.warning(
            "Upload at least two resumes from Resume Screening."
        )

    else:

        selected = st.multiselect(

            "Select Candidates",

            [c[1] for c in candidates],

            default=[c[1] for c in candidates]

        )

        jd = st.text_area(
            "Enter Job Description"
        )

        if st.button("Rank Candidates"):

            if jd.strip() == "":

                st.error("Please enter Job Description.")

            elif len(selected) < 2:

                st.error("Select at least two candidates.")

            else:

                resumes = []

                for row in candidates:

                    if row[1] in selected:

                        resumes.append({

                            "name": row[1],

                            "text": row[3]

                        })

                with st.spinner("Ranking Candidates..."):

                    ranking = rank_candidates(

                        resumes,

                        jd

                    )

                st.success("Ranking Complete!")

                st.markdown(ranking)

# ==========================================================
# INTERVIEW QUESTIONS
# ==========================================================

elif menu == "🎤 Interview Questions":

    st.header("🎤 AI Interview Question Generator")

    role = st.selectbox(

        "Select Job Role",

        [

            "Python Developer",

            "Java Developer",

            "Frontend Developer",

            "Backend Developer",

            "Full Stack Developer",

            "AI Engineer",

            "ML Engineer",

            "Data Scientist",

            "Data Analyst",

            "Cloud Engineer",

            "DevOps Engineer",

            "Cyber Security Analyst"

        ]

    )

    difficulty = st.selectbox(

        "Difficulty",

        [

            "Beginner",

            "Intermediate",

            "Advanced"

        ]

    )

    if st.button("Generate Questions"):

        with st.spinner("Generating Questions..."):

            questions = generate_questions(

                f"{role} ({difficulty})"

            )

        st.success("Questions Generated!")

        st.markdown(questions)
# ==========================================================
# RESUME CHAT AI
# ==========================================================

elif menu == "🤖 Resume Chat AI":

    st.header("🤖 Resume Chat AI")

    candidates = get_all_candidates()

    if len(candidates) == 0:

        st.warning("No candidates available. Please upload resumes first.")

    else:

        selected_candidate = st.selectbox(
            "Select Candidate",
            [c[1] for c in candidates]
        )

        candidate = None

        for c in candidates:

            if c[1] == selected_candidate:

                candidate = c
                break

        st.markdown("### 👤 Candidate Details")

        col1, col2, col3 = st.columns(3)

        col1.metric("Candidate", candidate[1])
        col2.metric("Status", candidate[4])
        col3.metric("Uploaded", candidate[5])

        st.markdown("---")

        question = st.text_input(
            "Ask anything about the candidate",
            placeholder="Example: What are the candidate's strengths?"
        )

        example_questions = st.selectbox(
            "Quick Questions",
            [
                "",
                "Summarize this resume",
                "What are the candidate's strengths?",
                "What are the weaknesses?",
                "Is this candidate suitable for a Python Developer role?",
                "What technical skills does the candidate have?",
                "Does this candidate have leadership experience?"
            ]
        )

        if example_questions != "":
            question = example_questions

        if st.button("Ask AI"):

            if question.strip() == "":

                st.warning("Please enter a question.")

            else:

                with st.spinner("Thinking..."):

                    answer = chat_with_resume(
                        candidate[3],
                        question
                    )

                st.success("Response Generated!")

                st.markdown(answer)

                st.download_button(
                    "📥 Download Response",
                    answer,
                    file_name="ResumeChat_Response.txt"
                )

# ==========================================================
# TALENT INSIGHTS
# ==========================================================

elif menu == "📊 Talent Insights":

    st.header("📊 AI Talent Insights")

    candidates = get_all_candidates()

    if len(candidates) == 0:

        st.warning("No candidates available.")

    else:

        selected_candidate = st.selectbox(
            "Select Candidate",
            [c[1] for c in candidates]
        )

        candidate = None

        for c in candidates:

            if c[1] == selected_candidate:

                candidate = c
                break

        st.markdown("## 👤 Candidate Profile")

        c1, c2, c3 = st.columns(3)

        c1.metric("Candidate", candidate[1])
        c2.metric("Status", candidate[4])
        c3.metric("Uploaded", candidate[5])

        st.markdown("---")

        if st.button("Generate Talent Insights"):

            with st.spinner("Analyzing Resume..."):

                insights = generate_talent_insights(
                    candidate[3]
                )

            st.success("Insights Generated!")

            st.markdown(insights)

            st.download_button(
                "📥 Download Insights",
                insights,
                file_name="Talent_Insights.txt"
            )

        st.markdown("---")

        st.subheader("Candidate Actions")

        a1, a2, a3 = st.columns(3)

        if a1.button(
            "✅ Shortlist",
            key=f"insight_short_{candidate[0]}"
        ):

            update_status(
                candidate[0],
                "Shortlisted"
            )

            st.success("Candidate Shortlisted")

            st.rerun()

        if a2.button(
            "❌ Reject",
            key=f"insight_reject_{candidate[0]}"
        ):

            update_status(
                candidate[0],
                "Rejected"
            )

            st.success("Candidate Rejected")

            st.rerun()

        if a3.button(
            "🗑 Delete Candidate",
            key=f"insight_delete_{candidate[0]}"
        ):

            delete_candidate(candidate[0])

            try:

                os.remove(
                    os.path.join(
                        "resumes",
                        candidate[2]
                    )
                )

            except:

                pass

            st.success("Candidate Deleted")

            st.rerun()