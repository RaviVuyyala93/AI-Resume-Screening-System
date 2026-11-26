import streamlit as st
import pandas as pd

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from matcher import calculate_similarity


# Page Configuration

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


# Main Heading

st.title("🤖 AI Resume Screening System")

st.write(
    "An application to analyze resumes "
    "and match candidates with job descriptions."
)


st.divider()


# Job Description Section

st.header("📝 Job Description")

job_description = st.text_area(
    "Enter the job description",
    height=200,
    placeholder="Enter required skills and job responsibilities..."
)


st.divider()


# Resume Upload Section

st.header("📄 Upload Candidate Resumes")

uploaded_files = st.file_uploader(
    "Upload PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)


# Process Resumes

if st.button("Analyze Resumes"):

    if not job_description.strip():

        st.error("Please enter a job description.")

    elif not uploaded_files:

        st.error("Please upload at least one PDF resume.")

    else:

        results = []

        for uploaded_file in uploaded_files:

            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text.strip():

                st.warning(
                    f"Could not extract text from {uploaded_file.name}"
                )

                continue

            # Extract skills

            resume_skills = extract_skills(resume_text)

            required_skills = extract_skills(job_description)

            # Calculate similarity

            similarity_score = calculate_similarity(
                resume_text,
                job_description
            )

            # Skill matching

            matched_skills = [
                skill for skill in required_skills
                if skill in resume_skills
            ]

            missing_skills = [
                skill for skill in required_skills
                if skill not in resume_skills
            ]

            if required_skills:

                skill_score = (
                    len(matched_skills) / len(required_skills)
                ) * 100

            else:

                skill_score = 0

            # Final score

            final_score = (
                0.60 * similarity_score
                + 0.40 * skill_score
            )

            results.append({

                "Candidate": uploaded_file.name,

                "Text Similarity": round(similarity_score, 2),

                "Skill Match": round(skill_score, 2),

                "Final Score": round(final_score, 2),

                "Matched Skills": ", ".join(matched_skills),

                "Missing Skills": ", ".join(missing_skills)

            })


        # Display Results

        if results:

            results_df = pd.DataFrame(results)

            results_df = results_df.sort_values(
                by="Final Score",
                ascending=False
            )

            st.success("Resume analysis completed!")

            st.header("🏆 Candidate Ranking")

            st.dataframe(
                results_df,
                use_container_width=True
            )

            # Best Candidate

            best_candidate = results_df.iloc[0]

            st.subheader("🥇 Highest Scoring Resume")

            st.write(best_candidate["Candidate"])

            st.metric(
                "Final Match Score",
                f'{best_candidate["Final Score"]}%'
            )

            # Download Results

            csv_data = results_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download Results as CSV",
                data=csv_data,
                file_name="resume_screening_results.csv",
                mime="text/csv"
            )

        else:

            st.warning(
                "No readable resumes were found."
            )


st.divider()

st.caption(
    "AI Resume Screening System | Python | NLP | Machine Learning"
)