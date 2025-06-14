import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load("model.pkl")

st.set_page_config(page_title="Prediksi Status Mahasiswa", layout="wide")
st.title("🎓 Prediksi Status Mahasiswa")

# Mapping
marital_status_map = {
    "Single": 1, "Married": 2, "Widower": 3, "Divorced": 4,
    "Facto Union": 5, "Legally Separated": 6
}

application_mode_map = {
    "1st phase - general contingent": 1,
    "Ordinance No. 612/93": 2,
    "1st phase - special contingent (Azores)": 5,
    "Holders of other higher courses": 7,
    "Ordinance No. 854-B/99": 10,
    "International student (bachelor)": 15,
    "1st phase - special contingent (Madeira)": 16,
    "2nd phase - general contingent": 17,
    "3rd phase - general contingent": 18,
    "Different Plan (533-A/99 b2)": 26,
    "Other Institution (533-A/99 b3)": 27,
    "Over 23 years old": 39,
    "Transfer": 42,
    "Change of course": 43,
    "Technological diploma holders": 44,
    "Change of institution/course": 51,
    "Short cycle diploma holders": 53,
    "Change institution/course (International)": 57
}

course_map = {
    "Biofuel Production Technologies": 33,
    "Animation and Multimedia Design": 171,
    "Social Service (evening)": 8014,
    "Agronomy": 9003,
    "Communication Design": 9070,
    "Veterinary Nursing": 9085,
    "Informatics Engineering": 9119,
    "Equinculture": 9130,
    "Management": 9147,
    "Social Service": 9238,
    "Tourism": 9254,
    "Nursing": 9500,
    "Oral Hygiene": 9556,
    "Marketing Management": 9670,
    "Journalism": 9773,
    "Basic Education": 9853,
    "Management (evening)": 9991
}

boolean_map = {"No": 0, "Yes": 1}
gender_map = {"Female": 0, "Male": 1}
label_map = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
status_emoji = {"Dropout": "🔴 Dropout", "Enrolled": "🟢 Enrolled", "Graduate": "🎓 Graduate"}

# Form input
with st.form("input_form"):
    col1, col2 = st.columns(2)

    with col1:
        marital_status = st.selectbox("Marital Status", marital_status_map.keys())
        application_mode = st.selectbox("Application Mode", application_mode_map.keys())
        application_order = st.slider("Application Order", 0, 9)
        course = st.selectbox("Course", course_map.keys())
        daytime_evening = st.radio("Class Time", ["Daytime", "Evening"])
        prev_qualification = st.slider("Previous Qualification", 1, 50)
        prev_qualification_grade = st.slider("Previous Qualification Grade", 0.0, 200.0)
        nationality = st.slider("Nationality", 1, 110)
        mother_qual = st.slider("Mother's Qualification", 1, 45)
        father_qual = st.slider("Father's Qualification", 1, 45)
        mother_occ = st.slider("Mother's Occupation", 0, 200)
        father_occ = st.slider("Father's Occupation", 0, 200)
        admission_grade = st.slider("Admission Grade", 0.0, 200.0)
        displaced = st.radio("Displaced", boolean_map.keys())
        special_needs = st.radio("Special Needs", boolean_map.keys())
        debtor = st.radio("Debtor", boolean_map.keys())
        tuition_fees = st.radio("Tuition Fees Up To Date", boolean_map.keys())
        gender = st.radio("Gender", gender_map.keys())
        scholarship_holder = st.radio("Scholarship Holder", boolean_map.keys())
        age_enroll = st.slider("Age at Enrollment", 16, 70)
        international = st.radio("International", boolean_map.keys())

    with col2:
        c1_cred = st.slider("CU 1st Sem - Credited", 0, 20)
        c1_enroll = st.slider("CU 1st Sem - Enrolled", 0, 20)
        c1_eval = st.slider("CU 1st Sem - Evaluated", 0, 20)
        c1_approved = st.slider("CU 1st Sem - Approved", 0, 20)
        c1_grade = st.slider("CU 1st Sem - Grade", 0.0, 20.0)
        c1_wo_eval = st.slider("CU 1st Sem - Without Evaluation", 0, 20)

        c2_cred = st.slider("CU 2nd Sem - Credited", 0, 20)
        c2_enroll = st.slider("CU 2nd Sem - Enrolled", 0, 20)
        c2_eval = st.slider("CU 2nd Sem - Evaluated", 0, 20)
        c2_approved = st.slider("CU 2nd Sem - Approved", 0, 20)
        c2_grade = st.slider("CU 2nd Sem - Grade", 0.0, 20.0)
        c2_wo_eval = st.slider("CU 2nd Sem - Without Evaluation", 0, 20)

        unemployment = st.number_input("Unemployment Rate (%)", 0.0, 100.0, 6.5)
        inflation = st.number_input("Inflation Rate (%)", 0.0, 100.0, 2.0)
        gdp = st.number_input("GDP (x1000)", 0.0, 200000.0, 100000.0)

    submitted = st.form_submit_button("🔍 Prediksi Status")

# Prediction
if submitted:
    input_array = np.array([[
        marital_status_map[marital_status],
        application_mode_map[application_mode],
        application_order,
        course_map[course],
        1 if daytime_evening == "Daytime" else 0,
        prev_qualification,
        prev_qualification_grade,
        nationality,
        mother_qual,
        father_qual,
        mother_occ,
        father_occ,
        admission_grade,
        boolean_map[displaced],
        boolean_map[special_needs],
        boolean_map[debtor],
        boolean_map[tuition_fees],
        gender_map[gender],
        boolean_map[scholarship_holder],
        age_enroll,
        boolean_map[international],
        c1_cred,
        c1_enroll,
        c1_eval,
        c1_approved,
        c1_grade,
        c1_wo_eval,
        c2_cred,
        c2_enroll,
        c2_eval,
        c2_approved,
        c2_grade,
        c2_wo_eval,
        unemployment,
        inflation,
        gdp
    ]])

    prediction = model.predict(input_array)[0]
    prediction_label = label_map[prediction]
    st.success(f"📊 Status Mahasiswa: {status_emoji[prediction_label]}")
