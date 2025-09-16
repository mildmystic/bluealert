import streamlit as st
from streamlit import session_state as ss
import random

st.title("📚 Health Education & Awareness")
st.markdown("### Learn about water safety, disease prevention, and healthy practices")

# Initialize quiz session state
if 'quiz_score' not in ss:
    ss.quiz_score = 0
if 'quiz_total' not in ss:
    ss.quiz_total = 0
if 'current_question' not in ss:
    ss.current_question = 0

# Water Safety Guidelines
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 💧 Water Safety Guidelines")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔥 Water Purification Methods")
    
    purification_methods = [
        {
            "method": "Boiling",
            "icon": "🔥",
            "description": "Boil water for 5+ minutes to kill bacteria and viruses",
            "effectiveness": "99.9%",
            "time": "5-10 minutes"
        },
        {
            "method": "UV Purification",
            "icon": "☀️",
            "description": "UV light destroys harmful microorganisms",
            "effectiveness": "99.99%",
            "time": "Instant"
        },
        {
            "method": "Water Purification Tablets",
            "icon": "💊",
            "description": "Chemical tablets for portable water treatment",
            "effectiveness": "99%",
            "time": "30 minutes"
        },
        {
            "method": "Reverse Osmosis",
            "icon": "🌀",
            "description": "Filters out dissolved solids and contaminants",
            "effectiveness": "95-99%",
            "time": "Continuous"
        }
    ]
    
    for method in purification_methods:
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.08);
            padding: 16px;
            border-radius: 8px;
            margin: 12px 0;
            border-left: 4px solid #3498db;
        ">
            <h4 style="margin: 0 0 8px 0; color: #3498db;">
                {method['icon']} {method['method']}
            </h4>
            <p style="margin: 0 0 8px 0; opacity: 0.9;">{method['description']}</p>
            <div style="display: flex; justify-content: space-between; font-size: 12px; opacity: 0.8;">
                <span>⚡ Effectiveness: {method['effectiveness']}</span>
                <span>⏱️ Time: {method['time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("#### 🚰 Safe Water Storage")
    
    storage_tips = [
        "Use clean, covered containers with tight-fitting lids",
        "Store treated water in cool, dark places",
        "Clean storage containers with soap weekly",
        "Use narrow-mouth containers to prevent contamination",
        "Label containers with treatment date",
        "Consume stored water within 3 days",
        "Never mix treated and untreated water",
        "Use a clean ladle or pour carefully to avoid contamination"
    ]
    
    for i, tip in enumerate(storage_tips, 1):
        st.markdown(f"**{i}.** {tip}")
    
    st.markdown("---")
    
    st.markdown("#### ⚠️ Water Safety Red Flags")
    warning_signs = [
        "🟤 Brownish or cloudy appearance",
        "🦠 Strange taste or odor",
        "🧪 Visible particles or sediment",
        "🌊 Source near sewage or waste",
        "🚫 No recent quality testing"
    ]
    
    for sign in warning_signs:
        st.markdown(f"- {sign}")

st.markdown('</div>', unsafe_allow_html=True)

# Disease Prevention
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🦠 Disease Prevention Guide")

# Disease information tabs
disease_tabs = st.tabs(["💧 Cholera", "🤒 Typhoid", "🤢 Diarrhea", "🟡 Hepatitis A"])

with disease_tabs[0]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🦠 About Cholera**
        - Acute diarrheal infection
        - Caused by Vibrio cholerae bacteria
        - Spreads through contaminated water/food
        - Can cause severe dehydration
        
        **🚨 Symptoms**
        - Profuse watery diarrhea
        - Vomiting
        - Rapid dehydration
        - Muscle cramps
        """)
    
    with col2:
        st.markdown("""
        **🛡️ Prevention**
        - Drink only boiled/bottled water
        - Eat hot, freshly cooked food
        - Avoid raw vegetables and fruits
        - Practice good hand hygiene
        
        **🏥 Treatment**
        - Oral rehydration solution (ORS)
        - Medical attention for severe cases
        - Antibiotics if prescribed
        """)

with disease_tabs[1]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🦠 About Typhoid**
        - Bacterial infection by Salmonella Typhi
        - Transmitted via contaminated food/water
        - Can be life-threatening if untreated
        - Vaccination available
        
        **🚨 Symptoms**
        - High fever (104°F/40°C)
        - Headache and weakness
        - Abdominal pain
        - Rose-colored chest rash
        """)
    
    with col2:
        st.markdown("""
        **🛡️ Prevention**
        - Get vaccinated before travel
        - Avoid street food and tap water
        - Wash hands frequently
        - Peel fruits yourself
        
        **🏥 Treatment**
        - Antibiotics as prescribed
        - Complete the full course
        - Plenty of fluids and rest
        """)

with disease_tabs[2]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🦠 About Diarrhea**
        - Loose, watery stools 3+ times/day
        - Usually caused by infections
        - Most common waterborne illness
        - Leading cause of child mortality
        
        **🚨 Symptoms**
        - Frequent loose stools
        - Abdominal cramps
        - Nausea and vomiting
        - Dehydration
        """)
    
    with col2:
        st.markdown("""
        **🛡️ Prevention**
        - Safe water and food practices
        - Hand washing after toilet use
        - Breastfeeding for infants
        - Proper sanitation
        
        **🏥 Treatment**
        - ORS for rehydration
        - Zinc supplements for children
        - Continue feeding
        - Seek help if severe
        """)

with disease_tabs[3]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🦠 About Hepatitis A**
        - Viral liver infection
        - Spreads through contaminated food/water
        - Highly contagious
        - Vaccine available
        
        **🚨 Symptoms**
        - Fatigue and weakness
        - Nausea and vomiting
        - Abdominal pain
        - Jaundice (yellow skin/eyes)
        """)
    
    with col2:
        st.markdown("""
        **🛡️ Prevention**
        - Hepatitis A vaccination
        - Good hand hygiene
        - Safe food and water
        - Avoid close contact with infected
        
        **🏥 Treatment**
        - Rest and supportive care
        - No specific medication
        - Recovery takes weeks to months
        - Avoid alcohol
        """)

st.markdown('</div>', unsafe_allow_html=True)

# Hygiene Best Practices
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🧼 Hygiene Best Practices")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 👐 Hand Hygiene")
    
    handwashing_steps = [
        "Wet hands with clean water",
        "Apply soap and lather well",
        "Scrub for at least 20 seconds",
        "Rinse thoroughly with clean water",
        "Dry with clean towel or air dry"
    ]
    
    for i, step in enumerate(handwashing_steps, 1):
        st.markdown(f"**{i}.** {step}")
    
    st.markdown("**🕐 When to wash:**")
    wash_times = [
        "Before eating or cooking",
        "After using the toilet",
        "After handling garbage",
        "After touching animals",
        "When hands are visibly dirty"
    ]
    
    for time in wash_times:
        st.markdown(f"• {time}")

with col2:
    st.markdown("#### 🍽️ Food Safety")
    
    food_safety_tips = [
        "**Cook thoroughly**: Heat food to 70°C/158°F",
        "**Eat promptly**: Consume hot food while hot",
        "**Store safely**: Refrigerate leftovers quickly",
        "**Reheat properly**: Heat leftovers to steaming",
        "**Keep clean**: Wash utensils and surfaces",
        "**Avoid cross-contamination**: Separate raw and cooked",
        "**Check expiry dates**: Don't eat expired food",
        "**Be cautious**: Avoid street food when unsure"
    ]
    
    for tip in food_safety_tips:
        st.markdown(f"• {tip}")

with col3:
    st.markdown("#### 🏠 Environmental Hygiene")
    
    env_hygiene = [
        "**Waste disposal**: Use covered bins",
        "**Water storage**: Clean containers regularly",
        "**Toilet maintenance**: Keep toilets clean",
        "**Pest control**: Eliminate breeding sites",
        "**Surface cleaning**: Disinfect regularly",
        "**Ventilation**: Ensure good air circulation",
        "**Drainage**: Prevent water stagnation",
        "**Community spaces**: Maintain cleanliness"
    ]
    
    for hygiene in env_hygiene:
        st.markdown(f"• {hygiene}")

st.markdown('</div>', unsafe_allow_html=True)

# Interactive Health Quiz
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🧠 Test Your Knowledge")

# Quiz questions
quiz_questions = [
    {
        "question": "How long should you boil water to make it safe for drinking?",
        "options": ["1 minute", "3 minutes", "5 minutes", "10 minutes"],
        "correct": 2,
        "explanation": "Boiling water for at least 5 minutes kills most harmful bacteria, viruses, and parasites."
    },
    {
        "question": "Which of these is NOT a symptom of cholera?",
        "options": ["Profuse watery diarrhea", "Skin rash", "Vomiting", "Dehydration"],
        "correct": 1,
        "explanation": "Cholera typically causes watery diarrhea, vomiting, and dehydration, but not skin rash."
    },
    {
        "question": "When should you wash your hands?",
        "options": ["Only when visibly dirty", "Before eating only", "Before eating and after toilet", "Multiple times daily"],
        "correct": 3,
        "explanation": "Hands should be washed frequently throughout the day, especially before eating, after toilet use, and when dirty."
    },
    {
        "question": "What is the safe pH range for drinking water?",
        "options": ["5.0-6.0", "6.5-8.5", "8.0-10.0", "Any pH is fine"],
        "correct": 1,
        "explanation": "Safe drinking water should have a pH between 6.5 and 8.5."
    },
    {
        "question": "Which water purification method is most effective?",
        "options": ["Boiling", "UV treatment", "Chlorination", "All are equally effective"],
        "correct": 3,
        "explanation": "All three methods (boiling, UV, chlorination) are highly effective when used properly."
    }
]

st.markdown(f"**Question {ss.current_question + 1} of {len(quiz_questions)}**")

if ss.current_question < len(quiz_questions):
    current_q = quiz_questions[ss.current_question]
    
    st.markdown(f"### {current_q['question']}")
    
    user_answer = st.radio(
        "Choose your answer:",
        current_q['options'],
        key=f"q_{ss.current_question}"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Submit Answer", type="primary"):
            selected_index = current_q['options'].index(user_answer)
            ss.quiz_total += 1
            
            if selected_index == current_q['correct']:
                ss.quiz_score += 1
                st.success(f"✅ Correct! {current_q['explanation']}")
            else:
                correct_answer = current_q['options'][current_q['correct']]
                st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")
                st.info(f"💡 {current_q['explanation']}")
            
            ss.current_question += 1
            
            if ss.current_question < len(quiz_questions):
                time.sleep(2)
                st.rerun()
    
    with col2:
        if st.button("Skip Question"):
            ss.current_question += 1
            if ss.current_question < len(quiz_questions):
                st.rerun()
    
    with col3:
        if st.button("Reset Quiz"):
            ss.quiz_score = 0
            ss.quiz_total = 0
            ss.current_question = 0
            st.rerun()

else:
    # Quiz completed
    if ss.quiz_total > 0:
        percentage = (ss.quiz_score / ss.quiz_total) * 100
        
        st.markdown(f"""
        ### 🎉 Quiz Complete!
        
        **Your Score: {ss.quiz_score}/{ss.quiz_total} ({percentage:.1f}%)**
        """)
        
        if percentage >= 80:
            st.success("🌟 Excellent! You have great knowledge about water safety and health!")
        elif percentage >= 60:
            st.info("👍 Good job! You have solid understanding with room for improvement.")
        else:
            st.warning("📚 Keep learning! Review the educational materials to improve your knowledge.")
        
        if st.button("Take Quiz Again"):
            ss.quiz_score = 0
            ss.quiz_total = 0
            ss.current_question = 0
            st.rerun()

# Current score display
if ss.quiz_total > 0:
    st.sidebar.markdown("### 🧠 Quiz Progress")
    st.sidebar.markdown(f"**Score: {ss.quiz_score}/{ss.quiz_total}**")
    st.sidebar.progress(ss.quiz_score / max(ss.quiz_total, 1))

st.markdown('</div>', unsafe_allow_html=True)

# Emergency Preparedness
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🆘 Emergency Preparedness")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎒 Emergency Water Kit")
    
    emergency_items = [
        "💧 1 gallon per person per day (3-day supply)",
        "💊 Water purification tablets",
        "🔥 Portable water filter or boiling equipment",
        "🥤 Bottled water (backup supply)",
        "🧪 Water testing strips",
        "🧼 Hand sanitizer and soap",
        "💊 Oral rehydration salts (ORS)",
        "📋 Emergency contact numbers"
    ]
    
    st.markdown("**Essential items to keep ready:**")
    for item in emergency_items:
        st.markdown(f"• {item}")

with col2:
    st.markdown("#### 🚨 When to Seek Medical Help")
    
    medical_signs = [
        "🤒 High fever (>101°F/38.5°C)",
        "💧 Signs of severe dehydration",
        "🩸 Blood in stool or vomit",
        "🤢 Persistent vomiting",
        "😵 Dizziness or confusion",
        "👶 Symptoms in infants or elderly",
        "⏰ Symptoms lasting >2 days",
        "🟡 Jaundice (yellow skin/eyes)"
    ]
    
    st.markdown("**Seek immediate medical attention if:**")
    for sign in medical_signs:
        st.markdown(f"• {sign}")
    
    st.markdown("---")
    st.markdown("#### 📞 Emergency Numbers")
    st.markdown("""
    - **Health Emergency:** 102
    - **General Emergency:** 112  
    - **Local Health Office:** Contact your district health office
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Additional Resources
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📖 Additional Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🌐 Online Resources")
    resources = [
        "[WHO Water Safety](https://who.int/water)",
        "[CDC Water Treatment](https://cdc.gov/water)",
        "[UNICEF Water & Sanitation](https://unicef.org/wash)",
        "[Ministry of Health Guidelines](https://mohfw.gov.in)"
    ]
    
    for resource in resources:
        st.markdown(f"• {resource}")

with col2:
    st.markdown("#### 📱 Mobile Apps")
    apps = [
        "Water Quality India",
        "Safe Water Network",
        "WHO Water Safety",
        "Emergency Response Guide"
    ]
    
    for app in apps:
        st.markdown(f"• {app}")

with col3:
    st.markdown("#### 📚 Downloads")
    
    downloads = [
        "Water Safety Poster",
        "Disease Prevention Guide", 
        "Emergency Preparedness Checklist",
        "Hygiene Practice Cards"
    ]
    
    for download in downloads:
        if st.button(f"📥 {download}", key=f"download_{download}"):
            st.success(f"Downloaded: {download}")

st.markdown('</div>', unsafe_allow_html=True)