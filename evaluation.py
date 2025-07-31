import streamlit as st
import pandas as pd
import plotly.express as px
import json
from data_handler import synchronize_drive_results
from config import LOCAL_RESULTS_DIR

def load_all_assessment_data():
    all_assessments = []
    local_files = list(LOCAL_RESULTS_DIR.glob("*.json"))
    if not local_files:
        st.info("No local assessment data found. Click 'Refresh Data from Server' to sync.")
        return pd.DataFrame()

    for i, file_path in enumerate(local_files):
        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
            user_info = data.get('user_info', {})
            for assessment in data.get('assessments', []):
                flat_assessment = assessment.copy()
                flat_assessment.update(user_info)
                responses = flat_assessment.pop('responses', {})
                flat_assessment.update(responses)
                all_assessments.append(flat_assessment)
        except (json.JSONDecodeError, IOError) as e:
            st.warning(f"Could not read or parse {file_path.name}: {e}")
            continue

    if not all_assessments:
        return pd.DataFrame()
        
    df = pd.DataFrame(all_assessments)
    likert_cols = ['confidence', 'features_highlighted', 'localization_correct', 'explanation_like', 'trust_increased', 'time_saving']
    for col in likert_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def render_demographics(df):
    st.header("Participant Demographics")
    if df.empty or 'name' not in df.columns:
        st.info("No demographic data to display.")
        return
    
    unique_users_df = df.drop_duplicates(subset='name')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Medical Specialty")
        specialty_counts = unique_users_df['specialty'].value_counts()
        fig = px.pie(specialty_counts, values=specialty_counts.values, names=specialty_counts.index, title="Distribution of Specialties")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Years of Clinical Experience")
        exp_counts = unique_users_df['years_experience'].value_counts()
        st.bar_chart(exp_counts)
    with col2:
        st.subheader("Experience with OCTA Imaging")
        octa_counts = unique_users_df['octa_experience'].value_counts()
        st.bar_chart(octa_counts)
        st.subheader("Familiarity with AI")
        ai_counts = unique_users_df['ai_familiarity'].value_counts()
        fig = px.pie(ai_counts, values=ai_counts.values, names=ai_counts.index, title="Familiarity with AI in Medical Imaging")
        st.plotly_chart(fig, use_container_width=True)

def render_overall_performance(df):
    st.header("Overall Assessment Performance")
    if df.empty:
        st.info("No data to display.")
        return
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("AI Prediction Correctness")
        correctness_counts = df['prediction_correct'].value_counts()
        fig = px.pie(correctness_counts, values=correctness_counts.values, names=correctness_counts.index, title="Was the AI prediction correct?")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Average Time per Assessment")
        avg_time = df['time_spent_seconds'].mean()
        st.metric("Average Time (seconds)", f"{avg_time:.2f}")
        st.subheader("Time Spent Distribution")
        fig = px.histogram(df, x="time_spent_seconds", nbins=20, title="Distribution of Time Spent per Assessment")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Likert Scale Responses (1=Disagree, 5=Agree)")
    likert_cols = {
        'confidence': "Confidence in AI Assessment",
        'features_highlighted': "Explanation Highlights Important Features",
        'localization_correct': "Explanation Highlights Relevant Areas",
        'explanation_like': "Likability of the Explanation",
        'trust_increased': "Explanation Increased Trust",
        'time_saving': "AI Will Help Save Time"
    }
    for col, title in likert_cols.items():
        if col in df.columns:
            avg_score = df[col].mean()
            st.markdown(f"**{title}** (Average: {avg_score:.2f})")
            counts = df[col].value_counts().sort_index()
            st.bar_chart(counts)
            st.markdown("---")

def render_explanation_comparison(df):
    st.header("Comparison by Explanation Type")
    if df.empty or 'explanation_type' not in df.columns:
        st.info("No data to display.")
        return
    likert_cols = {
        'confidence': "Confidence in AI Assessment",
        'features_highlighted': "Explanation Highlights Important Features",
        'localization_correct': "Explanation Highlights Relevant Areas",
        'explanation_like': "Likability of the Explanation",
        'trust_increased': "Explanation Increased Trust",
        'time_saving': "AI Will Help Save Time"
    }
    st.subheader("Average Likert Scores by Explanation Type")
    avg_scores = df.groupby('explanation_type')[list(likert_cols.keys())].mean().reset_index()
    avg_scores_melted = avg_scores.melt(id_vars='explanation_type', var_name='Metric', value_name='Average Score')
    fig = px.bar(avg_scores_melted, x='Metric', y='Average Score', color='explanation_type', barmode='group',
                 title="Average Agreement Scores by Explanation Type",
                 labels={'Average Score': 'Average Score (1-5)', 'Metric': 'Question'})
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("AI Correctness by Explanation Type")
    correctness_by_type = df.groupby('explanation_type')['prediction_correct'].value_counts(normalize=True).unstack().fillna(0) * 100
    st.dataframe(correctness_by_type.style.format("{:.1f}%"))
    st.subheader("Average Time Spent by Explanation Type")
    time_by_type = df.groupby('explanation_type')['time_spent_seconds'].mean()
    fig = px.bar(time_by_type, y='time_spent_seconds', color=time_by_type.index,
                 title="Average Time per Assessment by Explanation Type",
                 labels={'time_spent_seconds': 'Average Time (seconds)', 'explanation_type': 'Explanation Type'})
    st.plotly_chart(fig, use_container_width=True)

def render_chat_analysis(df):
    st.header("Chat Interaction Analysis")
    chat_df = df[df['explanation_type'] == 'text'].copy()
    if chat_df.empty or 'chat_history' not in chat_df.columns:
        st.info("No chat data available for analysis.")
        return
    chat_df['num_user_questions'] = chat_df['chat_history'].apply(lambda x: sum(1 for msg in x if msg['role'] == 'user'))
    st.subheader("User Question Frequency")
    avg_questions = chat_df['num_user_questions'].mean()
    st.metric("Average User Questions per Session", f"{avg_questions:.2f}")
    fig = px.histogram(chat_df, x='num_user_questions', title="Distribution of User Questions per Chat Session")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Commonly Asked Questions")
    all_questions = []
    for history in chat_df['chat_history']:
        for msg in history:
            if msg['role'] == 'user':
                all_questions.append(msg['content'])
    if all_questions:
        question_counts = pd.Series(all_questions).value_counts().nlargest(10)
        st.dataframe(question_counts)
    else:
        st.info("No user questions were recorded.")

def render_evaluation_page():
    st.title("Assessment Evaluation Dashboard")
    
    if st.button("Refresh Data from Server"):
        with st.spinner("Fetching latest results..."):
            synchronize_drive_results()
    
    df = load_all_assessment_data()
    
    if df.empty:
        st.warning("No assessment data to display.")
        return

    total_assessments = len(df)
    total_participants = df['name'].nunique() if 'name' in df.columns else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Total Assessments Completed", total_assessments)
    col2.metric("Total Unique Participants", total_participants)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Demographics", "Overall Performance", "Explanation Comparison", "Chat Analysis"])
    with tab1:
        render_demographics(df)
    with tab2:
        render_overall_performance(df)
    with tab3:
        render_explanation_comparison(df)
    with tab4:
        render_chat_analysis(df)