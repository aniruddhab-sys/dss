import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from gtts import gTTS
from io import BytesIO
import pandas as pd
import sys

# ----------------------------------------------------
# 1. DSS QUESTION DATA (All 46 questions)
# ----------------------------------------------------

# Note: All 46 questions are included here for the complete application
dss_questions = [
    {"id": 1, "section_hindi": "I. माता-पिता की चिंता (Parent's Concern)", "question_hindi": "क्या आपको अपने बच्चे के वृद्धि व विकास से संबंधीत चिंता है?", "category": "Parental Concern"},
    {"id": 2, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या आपको गर्भावस्था के समय कोई समस्या हुई? जैसे- उच्च रक्तचाप (बी.पी.), मधुमेह (शुगर), एनीमिया (खून की कमी) खसरा, गलसुवा (गलवा) या रूबेला जैसी बीमारियाँ", "category": "Prenatal/Perinatal Risk"},
    {"id": 3, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या प्रसव के समय आपको कोई समस्या हुई? जैसे- प्रसव के लिए ज्यादा समय लगना, ऑपरेशन से प्रसव, प्रसव के समय बच्चे को चिमटे से निकाला गया हो, समय से पूर्व जन्म होना या जन्म के समय बच्चे का वजन कम होना", "category": "Prenatal/Perinatal Risk"},
    {"id": 4, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे को जन्म के समय या उसके तुरंत बाद कोई समस्या हुई? जैसे- देर से रोना, पीलिया, शरीर नीला दिखना या तेज बुखार होना", "category": "Postnatal Risk"},
    {"id": 5, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे का रंग जन्म के समय आसामान्य था? जैसे- (नीला/ पीला/ बहुत फीका)", "category": "Postnatal Risk"},
    {"id": 6, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या स्तनपान कराते समय बच्चे को दूध पीने में कोई समस्या हुई? जैसे- चूसने में या निगलने/ गुटकने में", "category": "Postnatal Risk"},
    {"id": 7, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या जन्म के बाद बच्चे को कभी दौरे पड़े हैं या कभी बेहोश हुआ है?", "category": "Postnatal Risk"},
    {"id": 8, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे की आँखें अक्सर लाल रहती हैं या उनमें आंसू आते रहता है?", "category": "Physical Health"},
    {"id": 9, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे के कान से अक्सर पानी बहता है या मवाद आता है?", "category": "Physical Health"},
    {"id": 10, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चा अक्सर कान दर्द या सिर दर्द की शिकायत करता है?", "category": "Physical Health"},
    {"id": 11, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या आपको अपने बच्चे के शारीरिक रूप को लेकर कोई चिंता है?", "category": "Physical Appearance"},
    {"id": 12, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या अपने उम्र के बच्चे की तुलना में बच्चा बहुत छोटा या बहुत कमजोर हैं?", "category": "Growth/Strength"},
    {"id": 13, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे के शरीर की हरकतें अजीब हैं या चलने फिरने में लड़खड़ाहट है?", "category": "Motor Skills"},
    {"id": 14, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चा लंगडाकर चलता है? (या, क्या आपको अपने बच्चे के चलने के तरीके को लेकर कोई चिंता है?)", "category": "Motor Skills"},
    {"id": 15, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चा (18 माह की उम्र के बाद) भी चल नहीं पाता या बच्चा अन्य बच्चों की तुलना में देर से चलना शुरू किया?", "category": "Motor Skills"},
    {"id": 16, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे की रीढ़ की हड्डी के ऊपर कोई गठान या उभार है?", "category": "Physical Appearance"},
    {"id": 17, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे की आँखें तिरछी है या भेंगापन है? (या, क्या बच्चे की दोनों आँखों से देखने की दिशा थोड़ी अलग या असामान्य लगती है?)", "category": "Vision"},
    {"id": 18, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे की आँखों की पुतलियाँ स्लेटी / भूरी या सफेद रंग की हैं?", "category": "Vision"},
    {"id": 19, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चा चलते समय अक्सर किसी चीज से टकरा जाता है या बार-बार गिरता हैं? क्या बच्चे को रात के समय देखने में समस्या होती है?", "category": "Vision"},
    {"id": 20, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors)", "question_hindi": "क्या बच्चे के कान में कोई विकृति (ठीक से नहीं बना) है या कान नहीं है?", "category": "Hearing"},
    {"id": 21, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors) - अवलोकन", "question_hindi": "कोई भी खिलौना, पेन आदि लें, उसे बच्चे के आँखों के सामने लगभग 12-20 इंच की दुरी पर रखें और उसे बच्चे की आँखों के दोनों तरफ घुमायें (दांये और बाएं) और देखें कि क्या बच्चा उस वस्तु की दिशा में अपना सिर घुमाता है? (यह एक अवलोकन/जाँच है)", "category": "Vision Observation"},
    {"id": 22, "section_hindi": "II. स्वास्थ्य संबंधी खतरे (Health and Risk Factors) - अवलोकन", "question_hindi": "बच्चे के कान से लगभग 1-3 फिट की दुरी पर कोई आवाज बजने वाली झुनझुना या बर्तन रखें । ध्यान रखें कि बच्चा आपकी ओर देख नहीं रहा हो । अब उसे धीमे से बजाएँ और देखें की बच्चे ने जिस तरफ से आवाज आ रही है क्या उधर अपना सिर घुमाता है? (यह एक अवलोकन/जाँच है)", "category": "Hearing Observation"},
    {"id": 23, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "बात करने पर प्रतिक्रिया देना, जब देखभाल करने वाले बोलते हैं तो उनकी तरफ देखना या सतर्क रहना", "category": "Social/Emotional"},
    {"id": 24, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "लोगों को देखकर मुस्कुराना, खुश होना या उत्साह दिखाना", "category": "Social/Emotional"},
    {"id": 25, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "पेट के बल रहने पर या सीधे रहने पर अपनी गर्दन को सम्हाल लेना", "category": "Gross Motor"},
    {"id": 26, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "पेट से पीठ की तरफ और पीठ से पेट की तरफ पलटना", "category": "Gross Motor"},
    {"id": 27, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "बिना सहारा के बैठना", "category": "Gross Motor"},
    {"id": 28, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "आवाजों, मुस्कराहट और चेहरे के हाव- भाव के प्रति बारी बारी से प्रतिक्रिया देना", "category": "Communication"},
    {"id": 29, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "उँगलियों से छोटी चीजें या खाना पकड़ना/ उठाना", "category": "Fine Motor"},
    {"id": 30, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "सरल/आसान खेल खेलना", "category": "Social/Emotional"},
    {"id": 31, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "बा-बा, मा-मा, दा-दा जैसी आवाजें निकालना", "category": "Communication"},
    {"id": 32, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "अपने नाम पर प्रतिक्रिया देना", "category": "Communication"},
    {"id": 33, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "इशारा करना, हाथ आगे बढ़ाना, हाथ हिलाना", "category": "Communication"},
    {"id": 34, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "कुछ शब्द बोलना, जो चीज चाहिए उसके लिए उँगलियों से इशारा करना", "category": "Communication"},
    {"id": 35, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "बिना सहारे के चलना", "category": "Gross Motor"},
    {"id": 36, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "कहने पर बातों का पालन करना", "category": "Cognitive"},
    {"id": 37, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "स्नेह दिखाना, दूसरों की नकल करना", "category": "Social/Emotional"},
    {"id": 38, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "कुछ शब्द बोलना", "category": "Communication"},
    {"id": 39, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "खेल में दूसरों को शामिल करना", "category": "Social/Emotional"},
    {"id": 40, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "अपना नाम बोल पाना", "category": "Communication"},
    {"id": 41, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "काल्पनिक खेल खेलना", "category": "Social/Emotional/Cognitive"},
    {"id": 42, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "पेशाब / शौच पर नियंत्रण", "category": "Self-Help"},
    {"id": 43, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "खतरों से बचना", "category": "Cognitive"},
    {"id": 44, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "स्वयं से खाना खाना", "category": "Self-Help"},
    {"id": 45, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "स्वयं से कपड़े पहनना", "category": "Self-Help"},
    {"id": 46, "section_hindi": "III. विकासात्मक पड़ाव (Developmental Milestones)", "question_hindi": "साथियों के साथ सहयोग करना, नियमों का पालन करना", "category": "Social/Emotional"}
]

# ----------------------------------------------------
# 2. HELPER FUNCTIONS (TTS, Age Calculation, and FILTERING)
# ----------------------------------------------------

@st.cache_data(show_spinner=False)
def generate_audio(text, lang='hi'):
    """Generates audio bytes for Text-to-Speech (TTS) using gTTS."""
    text_for_tts = text
    if len(text) > 200:
        if '- (' in text:
            text_for_tts = text.split('- (')[0].strip()
        else:
            text_for_tts = text[:200]

    try:
        tts = gTTS(text=text_for_tts, lang=lang)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp.getvalue()
    except Exception as e:
        print(f"TTS Error: {e}", file=sys.stderr)
        return None

def calculate_chronological_age(birth_date, today_date):
    """Calculates the child's chronological age in months (adjusting for >15 days)."""
    if birth_date >= today_date:
        return 0, 0, "जन्म तिथि आज की तारीख से पहले होनी चाहिए।"
    diff = relativedelta(today_date, birth_date)
    total_months = diff.years * 12 + diff.months
    if diff.days >= 16:
        total_months += 1
    return total_months, diff.days, ""

def calculate_corrected_age(chronological_months, gestation_weeks):
    """Calculates the corrected age for premature babies."""
    term_weeks = 40
    if gestation_weeks >= term_weeks:
        return chronological_months, "बच्चा समय पर (Full Term) पैदा हुआ है। सुधार की आवश्यकता नहीं है।"
    week_deficit = term_weeks - gestation_weeks
    month_adjustment = round(week_deficit / 4)
    corrected_age_months = chronological_months - month_adjustment
    if corrected_age_months < 0:
        corrected_age_months = 0 
    adjustment_message = (f"जन्म के समय {gestation_weeks} सप्ताह थे। 40 सप्ताह पूरे होने के लिए {week_deficit} सप्ताह की कमी थी "
                          f"(लगभग {month_adjustment} महीने का सुधार)।")
    return corrected_age_months, adjustment_message


def get_milestone_questions_for_age(age_in_months):
    """
    CORRECTED MAPPING based on standard cumulative milestones (Q23-Q46).
    This function defines which Developmental Milestones (Q23-Q46) are relevant
    for a given age in months. The milestones are cumulative.
    """
    milestone_q_ids = []

    # 0-3 Months (Reacting to people, Neck control)
    if age_in_months >= 0:
        milestone_q_ids.extend([23, 24, 25])
        
    # 4-6 Months (Rolling, Babbling/Communication, Grasping, Sitting with support)
    if age_in_months > 3:
        milestone_q_ids.extend([26, 27, 28, 29, 31])
    
    # 7-12 Months (Sitting alone, Responding to name, Waving/Pointing, Simple games)
    if age_in_months > 6:
        milestone_q_ids.extend([30, 32, 33, 35]) # 35 is walking (often by 12 months)

    # 13-18 Months (Few words, Following commands, Showing affection)
    if age_in_months > 12:
        milestone_q_ids.extend([34, 36, 37, 38]) 

    # 19-24 Months (Naming self, Including others in play, Imagination, Few more words)
    if age_in_months > 18:
        milestone_q_ids.extend([39, 40, 41])
    
    # 25-36 Months (Toilet training, Avoiding danger, Self-feeding)
    if age_in_months > 24:
        milestone_q_ids.extend([42, 43, 44])
        
    # 37-60+ Months (Self-dressing, Cooperating with peers, Following rules)
    if age_in_months > 36:
        milestone_q_ids.extend([45, 46])
        
    # Remove duplicates and return sorted list
    return sorted(list(set(milestone_q_ids)))
    

def get_filtered_questions(age_in_months, all_questions):
    """Filters the full list of DSS questions based on age."""
    
    # 1. Questions 1-22 are always included (Parental Concern, Risk Factors)
    unconditional_q_ids = list(range(1, 23))
    
    # 2. Get the milestone questions (Q23+) relevant to the age
    milestone_q_ids = get_milestone_questions_for_age(age_in_months)
    
    # Combine the IDs
    relevant_q_ids = unconditional_q_ids + milestone_q_ids
    
    # Filter the question list
    filtered_list = [q for q in all_questions if q['id'] in relevant_q_ids]
    
    return filtered_list

# ----------------------------------------------------
# 3. AGE CALCULATION STEP (Screen 1)
# ----------------------------------------------------

def display_age_results(chronological_months, diff_days, gestation_weeks, corrected_months, adjustment_msg):
    """Helper to display age calculation results."""
    st.header("✨ गणना के परिणाम")
    st.subheader("📋 दर्ज किए गए विवरण")
    st.markdown(f"**गाँव:** {st.session_state.village_name} | **बच्चे का नाम:** {st.session_state.child_name} | **लिंग:** {st.session_state.gender}")
    st.markdown(f"**देखभालकर्ता:** {st.session_state.caregiver_name} ({st.session_state.caregiver_relation}) | **मोबाइल:** {st.session_state.mobile_number}")
    st.markdown("---")

    st.subheader("✅ वास्तविक (Chronological) आयु")
    years = chronological_months // 12
    months = chronological_months % 12
    st.metric(label="बच्चे की **वास्तविक आयु**", value=f"{chronological_months} महीने", delta=f"{years} साल और {months} महीने")
    
    if diff_days >= 16:
        st.caption(f"*सूचना: जन्म तिथि के **दिनों का अंतर ({diff_days})** 15 से अधिक था, इसलिए **+1 महीने** का समायोजन किया गया है।*")
    else:
         st.caption(f"*सूचना: जन्म तिथि के दिनों का अंतर ({diff_days}) 15 या उससे कम था, इसलिए कोई अतिरिक्त समायोजन नहीं किया गया है।*")

    if gestation_weeks < 40:
        st.markdown("---")
        st.subheader("🌟 सुधारी हुई (Corrected) आयु")
        corrected_years = corrected_months // 12
        corrected_display_months = corrected_months % 12
        st.metric(label="बच्चे की **सुधारी हुई आयु**", value=f"{corrected_months} महीने", delta=f"{corrected_years} साल और {corrected_display_months} महीने")
        st.caption(f"**समायोजन:** {adjustment_msg}")
    elif gestation_weeks == 40:
        st.markdown("---")
        st.info("बच्चा 40 सप्ताह पर पैदा हुआ। सुधारी हुई आयु वास्तविक आयु के समान है।")

def show_age_calculator_step():
    """Handles the first screen: Personal Details and Age Calculation."""
    st.header("📝 1. व्यक्तिगत विवरण और आयु दर्ज करें")
    
    with st.form(key='age_calc_form'):
        # Reordered inputs for better grouping/flow
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            child_name = st.text_input("1. **बच्चे का नाम**", value=st.session_state.child_name, key='child_name')
            caregiver_name = st.text_input("3. **प्राथमिक देखभालकर्ता का नाम**", value=st.session_state.caregiver_name, key='caregiver_name')
        with col_b:
            gender = st.selectbox("2. **लिंग**", ["चुनें", "लड़का", "लड़की", "अन्य"], index=["चुनें", "लड़का", "लड़की", "अन्य"].index(st.session_state.gender), key='gender')
            caregiver_relation = st.text_input("4. **बच्चे से संबंध**", value=st.session_state.caregiver_relation, key='caregiver_relation')
        with col_c:
            village_name = st.text_input("6. **गाँव का नाम**", value=st.session_state.village_name, key='village_name')
            mobile_number = st.text_input("5. **मोबाइल नंबर**", value=st.session_state.mobile_number, key='mobile_number')
        

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            default_birth_date = date(date.today().year - 2, 3, 10)
            birth_date = st.date_input("बच्चे की **जन्म तिथि**", value=default_birth_date, max_value=date.today(), key='birth_date')
        with col2:
            today_date = st.date_input("आज की **दिनांक**", value=date.today(), key='today_date')

        st.subheader("प्रीमैच्योरिटी विवरण (यदि लागू हो)")
        gestation_weeks = st.slider("जन्म के समय गर्भावधि (Gestational Age) सप्ताह में", min_value=20, max_value=40, value=st.session_state.gestation_weeks, step=1, key='gestation_weeks')

        submitted = st.form_submit_button("📊 आयु की गणना करें और अगले चरण पर जाएँ", type="primary")

    if submitted:
        # 1. Validation
        if not all([village_name, caregiver_name, caregiver_relation, mobile_number, child_name, gender != "चुनें"]):
            st.error("कृपया आयु गणना से पहले सभी व्यक्तिगत विवरण भरें।")
            st.session_state.details_submitted = False
            return
        
        # 2. Calculate Age
        chronological_months, diff_days, error_msg = calculate_chronological_age(birth_date, today_date)

        if error_msg:
            st.error(f"त्रुटि: {error_msg}")
            st.session_state.details_submitted = False
            return

        corrected_months, adjustment_msg = calculate_corrected_age(chronological_months, gestation_weeks)

        # 3. Store results in session state (These keys are safely overwritten)
        st.session_state.chronological_months = chronological_months
        st.session_state.corrected_months = corrected_months
        st.session_state.diff_days = diff_days
        st.session_state.adjustment_msg = adjustment_msg
        st.session_state.details_submitted = True
        
        # 4. Display Results
        display_age_results(chronological_months, diff_days, gestation_weeks, corrected_months, adjustment_msg)
        
        st.success("विवरण दर्ज और आयु गणना पूरी हुई। अब DSS स्क्रीनिंग पेज पर जा रहे हैं...")
        
        # 5. Corrected Navigation: Set state and RERUN to switch page
        st.session_state.page_flow = 'screening'
        st.rerun() 

# ----------------------------------------------------
# 4. DSS QUESTIONNAIRE STEP (Screen 2) - WITH AGE FILTERING
# ----------------------------------------------------

def show_dss_questionnaire():
    """Handles the second screen: The DSS Questionnaire with age filtering."""
    st.title("स्क्रीनिंग प्रश्नावली")
    
    # --- GO BACK BUTTON ADDITION ---
    if st.button("⏪ वापस 'व्यक्तिगत विवरण' पर जाएं"):
        st.session_state.page_flow = 'details'
        st.rerun()
    # -------------------------------

    # Determine the effective age for filtering
    gestation_weeks = st.session_state.get('gestation_weeks', 40)
    if gestation_weeks < 40:
        age_in_months = st.session_state.corrected_months 
        age_source = "सुधारी हुई (Corrected)"
    else:
        age_in_months = st.session_state.chronological_months 
        age_source = "वास्तविक (Chronological)"

    # Filter the questions based on age
    filtered_dss_questions = get_filtered_questions(age_in_months, dss_questions)
    
    st.info(f"💡 प्रश्नावली बच्चे की **{age_source} आयु ({age_in_months} महीने)** के आधार पर फ़िल्टर की गई है।")
    st.markdown("---")
    
    # Display Age and Details Summary at the top
    st.header("👤 बच्चे का सारांश")
    age_display = f"{age_in_months} महीने ({age_source})"
    st.markdown(f"**बच्चे का नाम:** **{st.session_state.child_name}** | **आयु:** {age_display} | **गाँव:** {st.session_state.village_name}")
    st.markdown("---")
    
    
    # --- FORM START ---
    with st.form(key='dss_screening_form'):
        current_section = ""

        for q in filtered_dss_questions:

            if q["section_hindi"] != current_section:
                st.markdown("---")
                st.header(f"➡️ {q['section_hindi']}")
                
                if q['id'] >= 23:
                    st.caption(f"⚠️ इस अनुभाग के प्रश्न **बच्चे की आयु ({age_in_months} महीने)** के लिए प्रासंगिक **विकास के पड़ाव** हैं।")
                    
                current_section = q["section_hindi"]

            q_col, audio_col = st.columns([10, 1])
            question_text = f"**Q{q['id']}.** {q['question_hindi']}"
            answer_key = f"q_{q['id']}_answer"

            with q_col:
                st.markdown(question_text)

            audio_bytes = generate_audio(q['question_hindi'])

            with audio_col:
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.caption("🎧 (ऑडियो विफल)")

            st.radio(
                "उत्तर दें:",
                options=["हाँ (Yes)", "नहीं (No)", "लागू नहीं (N/A)"],
                key=answer_key,
                index=1,
                horizontal=True,
                label_visibility="collapsed"
            )

            st.markdown("---")

        submitted = st.form_submit_button(
            "✅ स्क्रीनिंग सबमिट करें और परिणाम देखें",
            type="primary"
        )
    # --- FORM END ---

    if submitted:
        st.session_state.questions_asked = filtered_dss_questions
        st.session_state.page_flow = 'results'
        st.rerun()

# ----------------------------------------------------
# 5. DECISION AID LOGIC AND CONTENT
# ----------------------------------------------------

def get_decision_aid_content(group):
    """Generates the structured decision aid content for the given group."""
    
    support_action = (
        "(i) देखभालकर्ता के योगदान की सराहना करें और उनके प्रति सहानुभूति दिखाएँ\n"
        "(ii) डीएसएस+ बुकलेट का उपयोग करते हुए बच्चे के विकास में सहयोग करने के लिए व्यक्तिगत सलाह देना \n"
        "    [समूह-1, 2(a), 2(b) (3 वर्ष तक की आयु): पृष्ठ संख्या 11 देखें]\n"
        "    [समूह-3 (5 वर्ष तक की आयु): पृष्ठ संख्या 12 देखें]\n"
        "(iii) हेल्पलाइन नंबर की जानकारी देना: **8448448996**\n"
        "(iv) संबंधित ऑडियो, वीडियो, पोस्टर की जानकारी देना\n"
        "(v) जहाँ रेफरल की आवश्यकता हो वहां प्रोत्साहन देना"
    )
    
    referral_2a_2b = "**सामान्य जाँच रेफरल:** पास के प्राथमिक स्वास्थ्य केंद्र (पी.एच.सी.) या जिला अस्पताल भेजना है।"
    referral_3 = (
        "**सामान्य जाँच रेफरल:** पास के प्राथमिक स्वास्थ्य केंद्र (पी.एच.सी.) या जिला अस्पताल भेजना है।\n\n"
        "**विशेष रेफरल:** पास के जिला शीघ्र हस्तक्षेप केंद्र (डी.ई.आई.सी.), जिला दिव्यांगजन पुनर्वास केंद्र (डी.डी.आर.सी.), राष्ट्रीय मानसिक स्वास्थ्य पुनर्वास संस्थान (एन.आई.एम.एच.आर.) रेफर करना है।"
    )

    aid_data = {
        "समूह- 1": {
            "description": "कोई विकासात्मक देरी या स्वास्थ्य संबंधी खतरे अथवा जोखिम नहीं",
            "home_visits": [
                "गृहभेंट 1: डीएसएस स्क्रीनिंग + सहयोग",
                "गृहभेंट 2: 2-3 माह के बाद पोषण ट्रैकर शेड्यूल अनुसार डीएसएस स्क्रीनिंग + सहयोग",
                "गृहभेंट 3: 3 माह के बाद डीएसएस स्क्रीनिंग + सहयोग"
            ],
            "note": "(नोट: पोषण गृहभेंट करना हैं, बच्चे के लिए जब बच्चे की उम्र 0, 2, 3, 6, 9, 12, 15, 18, 21 एवं 24 माह में)",
            "support": support_action,
            "referral": "**कोई रेफरल आवश्यक नहीं है।**"
        },
        "समूह- 2(a)": {
            "description": "बच्चे को लेकर माता-पिता की चिंता या स्वास्थ्य संबंधी खतरे अथवा जोखिम की वजह से विकासात्मक देरी का खतरा",
            "home_visits": [
                "गृहभेंट 1: डीएसएस स्क्रीनिंग + सहयोग + **रेफरल**",
                "गृहभेंट 2: 2-3 माह के बाद पोषण ट्रैकर शेड्यूल अनुसार डीएसएस स्क्रीनिंग + सहयोग",
                "गृहभेंट 3: 3 माह के बाद डीएसएस स्क्रीनिंग + सहयोग"
            ],
            "note": "",
            "support": support_action,
            "referral": referral_2a_2b
        },
        "समूह- 2(b)": {
            "description": "स्वास्थ्य संबंधी खतरे अथवा जोखिम की वजह से विकासात्मक देरी का खतरा",
            "home_visits": [
                "गृहभेंट 1: डीएसएस स्क्रीनिंग + सहयोग + **रेफरल**",
                "गृहभेंट 2: 2-3 माह के बाद पोषण ट्रैकर शेड्यूल अनुसार डीएसएस स्क्रीनिंग + सहयोग",
                "गृहभेंट 3: 3 माह के बाद डीएसएस स्क्रीनिंग + सहयोग"
            ],
            "note": "",
            "support": support_action,
            "referral": referral_2a_2b
        },
        "समूह- 3": {
            "description": "विकासात्मक देरी",
            "home_visits": [
                "कम से कम माह में 1 बार गृहभेंट करना।",
                "गृहभेंट 1: डीएसएस स्क्रीनिंग + सहयोग + **रेफरल**",
                "गृहभेंट 2: सहयोग",
                "गृहभेंट 3: सहयोग",
                "गृहभेंट 4: डीएसएस स्क्रीनिंग + सहयोग (गृहभेंट में समूह को फिर से तय करना)",
                "गृहभेंट 5: सहयोग",
                "गृहभेंट 6: सहयोग",
                "गृहभेंट 7: डीएसएस स्क्रीनिंग + सहयोग"
            ],
            "note": "",
            "support": support_action,
            "referral": referral_3
        }
    }
    
    return aid_data.get(group, {"description": "अज्ञात समूह", "home_visits": [], "note": "", "support": "", "referral": "**डेटा उपलब्ध नहीं।**"})

# ----------------------------------------------------
# 6. RESULTS STEP (Screen 3)
# ----------------------------------------------------

def show_results_summary():
    """Handles the final screen: Summary and Results, including Decision Aid."""
    st.header("✅ स्क्रीनिंग परिणाम")
    st.success("स्क्रीनिंग सफलतापूर्वक सबमिट हो गई है!")
    
    # --- GO BACK BUTTON ADDITION ---
    if st.button("⏪ वापस 'स्क्रीनिंग' प्रश्नावली पर जाएं"):
        st.session_state.page_flow = 'screening'
        st.rerun()
    # -------------------------------
    
    st.markdown("---")
    
    results = {}
    questions_asked = st.session_state.get('questions_asked', dss_questions)

    for q in questions_asked:
        key = f"q_{q['id']}_answer"
        if key in st.session_state:
            results[q["id"]] = {
                "प्रश्न (Question)": q["question_hindi"],
                "उत्तर (Answer)": st.session_state[key],
                "श्रेणी (Category)": q["category"]
            }

    results_df = pd.DataFrame.from_dict(results, orient="index")
    
    st.subheader("👤 बच्चे का सारांश")
    display_age_results(st.session_state.chronological_months, st.session_state.diff_days, st.session_state.gestation_weeks, st.session_state.corrected_months, st.session_state.adjustment_msg)
    
    st.markdown("---")
    
    # -------------------------------------------------------------
    # DECISION AID LOGIC (निर्णय सहायक तर्क)
    # -------------------------------------------------------------
    
    yes_df = results_df[results_df["उत्तर (Answer)"] == "हाँ (Yes)"]
    no_df = results_df[results_df["उत्तर (Answer)"] == "नहीं (No)"]
    
    group = "समूह- 1" # Default to lowest risk

    # 1. Check for Group 3 trigger (Developmental Delay - Q23-Q46 = "नहीं")
    q_23_to_46_ids = [q['id'] for q in questions_asked if q['id'] >= 23]
    no_q23_to_46 = no_df.index.intersection(q_23_to_46_ids)
    
    if len(no_q23_to_46) > 0:
        group = "समूह- 3" # Highest priority
    else:
        # 2. Check for Group 2(a) triggers (Q1 OR Q2-Q6 = "हाँ")
        is_q1_yes = 1 in yes_df.index
        yes_q2_to_6 = yes_df.index.intersection(range(2, 7))
        
        if is_q1_yes or len(yes_q2_to_6) > 0:
            group = "समूह- 2(a)"
        else:
            # 3. Check for Group 2(b) triggers (Q7-Q22 = "हाँ")
            yes_q7_to_22 = yes_df.index.intersection(range(7, 23))
            
            if len(yes_q7_to_22) > 0:
                group = "समूह- 2(b)"
            # Else remains Group 1

    decision_aid_data = get_decision_aid_content(group)

    # -------------------------------------------------------------
    # DISPLAY DECISION AID (निर्णय सहायक का प्रदर्शन)
    # -------------------------------------------------------------

    st.subheader("💡 निर्णय सहायक (Decision Aid) - आवश्यक कार्यवाही")
    st.markdown(f"बच्चे को **{group}** ({decision_aid_data['description']}) में वर्गीकृत किया गया है।")
    
    st.markdown("---")
    
    # --- गृहभेंट (Home Visits) ---
    st.markdown("##### 🏡 गृहभेंट की अनुसूची")
    for visit in decision_aid_data['home_visits']:
        st.markdown(f"- {visit}")
    if decision_aid_data['note']:
        st.caption(decision_aid_data['note'])
        
    st.markdown("---")

    # --- सहयोग (Support) ---
    st.markdown("##### 🤝 सहयोग (Support) क्रियाएँ")
    st.markdown(decision_aid_data['support'].replace('\n', '\n\n'))

    st.markdown("---")
    
    # --- रेफरल (Referral) ---
    st.markdown("##### 🏥 रेफरल की जानकारी")
    st.markdown(decision_aid_data['referral'])

    st.markdown("---")
    
    # -------------------------------------------------------------
    # SUMMARY DISPLAY (सारांश प्रदर्शन) - kept for completeness
    # -------------------------------------------------------------
    
    st.subheader("📊 DSS प्रश्नोत्तर सारांश (कुल पूछे गए प्रश्न: " + str(len(questions_asked)) + ")")
    st.dataframe(results_df, use_container_width=True)

    yes_df = results_df[results_df["उत्तर (Answer)"] == "हाँ (Yes)"]

    if not yes_df.empty:
        st.warning(f"⚠️ **{len(yes_df)}** प्रश्नों में जोखिम संकेत मिले हैं। इन क्षेत्रों पर ध्यान दें:")
        st.dataframe(yes_df[["प्रश्न (Question)", "श्रेणी (Category)"]], use_container_width=True)
        
        # Display the specific questions that triggered Group 3
        if group == "समूह- 3":
             st.error("🚨 **विकासात्मक देरी (Developmental Delay) ट्रिगर करने वाले प्रश्न:**")
             delay_questions = no_df[no_df.index.isin(q_23_to_46_ids)]
             st.dataframe(delay_questions[["प्रश्न (Question)", "श्रेणी (Category)"]], use_container_width=True)
             
    else:
        st.balloons()
        st.success("🎉 कोई जोखिम संकेत नहीं मिला।")

    st.markdown("---")
    
    # New Screening button with explicit key
    if st.button("⏪ नया बच्चा (New Screening) शुरू करें", key='new_screening_button', type="secondary"):
        st.session_state.clear()
        st.rerun()

# ----------------------------------------------------
# 7. MAIN APPLICATION FLOW 
# ----------------------------------------------------

def main():
    """The main entry point for the Streamlit application."""
    st.set_page_config(page_title="DSS स्क्रीनिंग | एकीकृत", layout="wide")
    
    # --- CRITICAL: INITIALIZE ALL SESSION STATE VARIABLES HERE ---
    if 'page_flow' not in st.session_state:
        st.session_state.page_flow = 'details'

    # 1. Input/Form Data Initialization
    if 'village_name' not in st.session_state: st.session_state.village_name = ""
    if 'caregiver_name' not in st.session_state: st.session_state.caregiver_name = ""
    if 'caregiver_relation' not in st.session_state: st.session_state.caregiver_relation = ""
    if 'mobile_number' not in st.session_state: st.session_state.mobile_number = ""
    if 'child_name' not in st.session_state: st.session_state.child_name = ""
    if 'gender' not in st.session_state: st.session_state.gender = "चुनें"
    if 'gestation_weeks' not in st.session_state: st.session_state.gestation_weeks = 40
    
    # 2. Status and Result Initialization
    if 'details_submitted' not in st.session_state: st.session_state.details_submitted = False
    if 'chronological_months' not in st.session_state: st.session_state.chronological_months = 0
    if 'corrected_months' not in st.session_state: st.session_state.corrected_months = 0
    if 'diff_days' not in st.session_state: st.session_state.diff_days = 0
    if 'adjustment_msg' not in st.session_state: st.session_state.adjustment_msg = ""
    if 'questions_asked' not in st.session_state: st.session_state.questions_asked = [] 
    
    # -----------------------------------------------------------------

    st.title("👶 दिव्यांगता स्क्रीनिंग शेड्यूल (DSS)")
    st.caption("स्क्रीनिंग प्रश्नावली")

    if st.session_state.page_flow == 'details':
        show_age_calculator_step()
    elif st.session_state.page_flow == 'screening':
        if not st.session_state.get('details_submitted', False):
            st.warning("कृपया DSS स्क्रीनिंग शुरू करने से पहले व्यक्तिगत विवरण और आयु दर्ज करें।")
            st.session_state.page_flow = 'details'
            st.rerun()
        show_dss_questionnaire()
    elif st.session_state.page_flow == 'results':
        show_results_summary()


if __name__ == "__main__":
    main()