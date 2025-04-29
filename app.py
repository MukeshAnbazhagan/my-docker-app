import streamlit as st
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Digi Vaidya ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS for better styling
st.markdown("""
<style>
    /* Page-wide styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-weight: 600;
        color: #1E3A8A;
    }
    
    /* History items styling */
    .selected-option {
        background-color: #F8FAFC;
        padding: 18px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .selected-option strong {
        color: #1E40AF;
        font-size: 16px;
    }
    
    .selected-option .question-text {
        color: #334155;
        font-size: 16px;
        margin-bottom: 8px;
        display: block;
    }
    
    .selected-option .answer-text {
        color: #0F766E;
        font-weight: 500;
        display: block;
        margin-top: 6px;
    }
    
    .checkmark {
        color: #10B981;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Results styling */
    .diagnosis-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    
    .diagnosis-header {
        background-color: #059669;
        color: white;
        padding: 15px 20px;
        font-size: 18px;
        font-weight: 600;
    }
    
    .diagnosis-body {
        padding: 20px;
        color: #374151;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .medication-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    
    .medication-header {
        background-color: #DC2626;
        color: white;
        padding: 15px 20px;
        font-size: 18px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .medication-pill-badge {
        background-color: white;
        color: #DC2626;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
    }
    
    .medication-body {
        padding: 20px;
    }
    
    .medication-info {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 10px;
    }
    
    .medication-info-item {
        flex: 1;
        min-width: 140px;
    }
    
    .info-label {
        color: #6B7280;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 5px;
    }
    
    .info-value {
        color: #111827;
        font-size: 16px;
    }
    
    .advice-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    
    .advice-header {
        background-color: #2563EB;
        color: white;
        padding: 15px 20px;
        font-size: 18px;
        font-weight: 600;
    }
    
    .advice-body {
        padding: 20px;
        color: #374151;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .warning-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    
    .warning-header {
        background-color: #E11D48;
        color: white;
        padding: 15px 20px;
        font-size: 18px;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    
    .warning-icon {
        margin-right: 10px;
        font-size: 20px;
    }
    
    .warning-body {
        padding: 20px;
        color: #4B5563;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .test-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .test-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        height: 100%;
    }
    
    .test-header {
        background-color: #8B5CF6;
        color: white;
        padding: 15px;
        font-size: 16px;
        font-weight: 600;
        text-align: center;
    }
    
    .section-header {
        margin: 30px 0 20px 0;
        color: #1F2937;
        font-size: 22px;
        font-weight: 600;
        padding-bottom: 10px;
        border-bottom: 2px solid #E5E7EB;
    }
    
    .section-subheader {
        color: #374151;
        font-size: 18px;
        font-weight: 600;
        margin: 25px 0 15px 0;
    }
    
    .question {
        font-weight: 600;
        font-size: 20px;
        color: #1E3A8A;
        margin: 25px 0 20px 0;
        padding: 15px 20px;
        background-color: #F8FAFC;
        border-radius: 8px;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Button styling */
    div.stButton > button {
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.2s;
        width: 100%;
        margin-bottom: 10px;
    }
    
    div.stButton > button:hover {
        background-color: #E2E8F0;
        color: #1E40AF;
        border-color: #94A3B8;
    }
    
    div.stButton > button:active {
        background-color: #DBEAFE;
        border-color: #3B82F6;
    }
    
    .restart-button button {
        background-color: #1E40AF !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
    }
    
    .restart-button button:hover {
        background-color: #1E3A8A !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Main app layout
st.markdown("""
<h1 style="text-align: center; color: #1E3A8A; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 2px solid #E2E8F0;">
    🏥 Digi Vaidya 
</h1>
""", unsafe_allow_html=True)

# Define the protocols directory
PROTOCOLS_DIR = "protocols"

# Function to load the decision tree from a JSON file
def load_decision_tree(file_path: str) -> Dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return {"root": {}}

# Function to find matching protocol file
def find_protocol_file(protocol_name):
    """Find a JSON file that starts with the given protocol name"""
    protocol_files = []
    
    try:
        # Check if protocols directory exists
        if not os.path.exists(PROTOCOLS_DIR):
            os.makedirs(PROTOCOLS_DIR)
            return None
            
        # Find all JSON files that start with the protocol name
        for file in os.listdir(PROTOCOLS_DIR):
            if file.lower().startswith(protocol_name.lower()) and file.endswith('.json'):
                protocol_files.append(os.path.join(PROTOCOLS_DIR, file))
                
        if protocol_files:
            return protocol_files[0]  # Return the first matching file
        else:
            return None
    except Exception as e:
        st.error(f"Error finding protocol file: {e}")
        return None

# Function to get available protocols
def get_available_protocols(protocols_dir: str) -> List[str]:
    protocols = []
    
    # Create directory if it doesn't exist
    os.makedirs(protocols_dir, exist_ok=True)
    
    try:
        # Get all JSON files in the protocols directory
        json_files = [f for f in os.listdir(protocols_dir) if f.endswith('.json')]
        
        # Extract protocol names (without extension)
        for file in json_files:
            # Get protocol name from filename (before the first underscore or period)
            protocol_name = file.split('_')[0].split('.')[0].capitalize()
            if protocol_name not in protocols:
                protocols.append(protocol_name)
    except Exception as e:
        st.error(f"Error reading protocols directory: {e}")
    
    return protocols

# Initialize session state if not already done
if 'history' not in st.session_state:
    st.session_state.history = []  # To store question and selected option history
if 'current_node' not in st.session_state:
    st.session_state.current_node = None
if 'diagnosis_made' not in st.session_state:
    st.session_state.diagnosis_made = False
if 'decision_tree' not in st.session_state:
    st.session_state.decision_tree = None
if 'protocol_selected' not in st.session_state:
    st.session_state.protocol_selected = False
if 'protocol_name' not in st.session_state:
    st.session_state.protocol_name = None

# Function to handle option selection
def select_option(option: Dict, question: str):
    # Add to history
    st.session_state.history.append({
        'question': question,
        'selected_option': option['opt_value'],
        'option_id': option['option_id']
    })
    
    # Update current node
    st.session_state.current_node = option['next']
    
    # Check if we've reached an action node (diagnosis)
    if 'actions' in option['next']:
        st.session_state.diagnosis_made = True

# Function to parse action text
def parse_action(action_text: str) -> Dict:
    parts = action_text.split(':', 1)
    action_type = parts[0].strip()
    
    details = {}
    if len(parts) > 1:
        details_text = parts[1].strip()
        for item in details_text.split(';'):
            if item.strip():
                key_value = item.split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    details[key] = value
    
    return {
        'action_type': action_type,
        'details': details
    }

# Function to reset the app
def reset_app():
    st.session_state.history = []
    st.session_state.current_node = st.session_state.decision_tree['root'] if st.session_state.decision_tree else None
    st.session_state.diagnosis_made = False

# Function to select a protocol
def select_protocol(protocol_name):
    st.session_state.protocol_name = protocol_name
    st.session_state.protocol_selected = True
    
    # Find matching JSON file
    protocol_file = find_protocol_file(protocol_name)
    
    if not protocol_file:
        st.error(f"No JSON file found for protocol: {protocol_name}")
        st.session_state.protocol_selected = False
        return
    
    # Load the decision tree
    decision_tree = load_decision_tree(protocol_file)
    st.session_state.decision_tree = decision_tree
    st.session_state.current_node = decision_tree['root']
    st.session_state.history = []
    st.session_state.diagnosis_made = False

# Show protocol selection if not already selected
if not st.session_state.protocol_selected:
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; background-color: #F8FAFC; margin-bottom: 30px;">
        <h3 style="margin-top: 0; color: #1E40AF; font-size: 18px;">Select a Diagnosis Protocol</h3>
        <p style="color: #475569; margin-bottom: 15px;">Please select the type of medical condition you want to assess.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get available protocols
    protocols = get_available_protocols(PROTOCOLS_DIR)
    
    # Display available protocols in a grid layout
    st.markdown("### Available Protocols")
    
    # Create a grid layout - 3 columns
    cols = st.columns(3)
    
    # Check if no protocols found
    if not protocols:
        st.warning("""
        No protocol files found in the 'protocols' directory. 
        
        Please add JSON files to the 'protocols' folder named with the format: 'condition_name.json' 
        (e.g., 'cough_adult.json', 'fever_child.json')
        """)
        
        # Option to upload a JSON file instead
        st.markdown("### Upload a Protocol File")
        uploaded_file = st.file_uploader("Upload a JSON protocol file", type=["json"])
        
        if uploaded_file:
            # Save the uploaded file to the protocols directory
            file_path = os.path.join(PROTOCOLS_DIR, uploaded_file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract protocol name from filename
            protocol_name = uploaded_file.name.split('_')[0].split('.')[0].capitalize()
            
            # Select this protocol
            select_protocol(protocol_name)
            st.success(f"Protocol '{protocol_name}' uploaded and selected!")
            st.rerun()
    else:
        # Distribute protocols across columns
        for i, protocol in enumerate(protocols):
            col_idx = i % 3
            with cols[col_idx]:
                # Use a simple button with better styling
                if st.button(protocol, key=f"protocol_{i}", 
                            use_container_width=True,
                            help=f"Select {protocol} protocol"):
                    select_protocol(protocol)
                    st.rerun()
else:
    # Protocol is selected, display the diagnosis process
    if st.session_state.protocol_selected and st.session_state.decision_tree:
        
        # Display protocol info
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 8px; background-color: #EFF6FF; margin-bottom: 20px; 
                    border-left: 6px solid #3B82F6; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="font-size: 16px; color: #1E40AF;">Active Protocol:</strong> 
                <span style="color: #1E3A8A; font-size: 16px;">{st.session_state.protocol_name}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⬅ Change Protocol", key="change_protocol_button"):
            st.session_state.protocol_selected = False
            st.rerun()
        
        # Display history
        if st.session_state.history:
            st.markdown('<div class="section-header">Your Responses</div>', unsafe_allow_html=True)
            for idx, item in enumerate(st.session_state.history):
                st.markdown(f"""
                <div class="selected-option">
                    <strong>Q{idx+1}:</strong> <span class="question-text">{item['question']}</span>
                    <span class="answer-text"><span class="checkmark">✓</span> {item['selected_option']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Display current question if not at diagnosis stage
        if not st.session_state.diagnosis_made and st.session_state.current_node:
            current_node = st.session_state.current_node
            
            st.markdown(f'<div class="question">{current_node["question"]}</div>', 
                        unsafe_allow_html=True)
            
            # Create a column layout for options
            option_cols = st.columns(min(2, len(current_node['options'])))
            for i, option in enumerate(current_node['options']):
                col_idx = i % len(option_cols)
                with option_cols[col_idx]:
                    if st.button(f"{option['opt_value']}", key=f"option_{option['option_id']}"):
                        select_option(option, current_node['question'])
                        st.rerun()
        
        # Display diagnosis and recommendations if reached end
        if st.session_state.diagnosis_made:
            st.markdown('<div class="section-header">Diagnosis & Recommendations</div>', unsafe_allow_html=True)
            
            actions_node = st.session_state.current_node
            
            # Group actions by type for organized display
            action_groups = {
                'diagnosis': [],
                'order_tests': [],
                'recommend_medication': [],
                'provide_advice': [],
                'red_flags': []
            }
            
            for action_text in actions_node['actions']:
                action = parse_action(action_text)
                if action['action_type'] in action_groups:
                    action_groups[action['action_type']].append(action)
            
            # Display diagnoses
            if action_groups['diagnosis']:
                st.markdown('<div class="section-subheader">Diagnosis</div>', unsafe_allow_html=True)
                for action in action_groups['diagnosis']:
                    st.markdown(f"""
                    <div class="diagnosis-card">
                        <div class="diagnosis-header">
                            {action['details'].get('diagnosis.title', '')}
                        </div>
                        <div class="diagnosis-body">
                            {action['details'].get('diagnosis.description', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display ordered tests
            if action_groups['order_tests']:
                st.markdown('<div class="section-subheader">Laboratory Tests</div>', unsafe_allow_html=True)
                st.markdown('<div class="test-grid">', unsafe_allow_html=True)
                for action in action_groups['order_tests']:
                    st.markdown(f"""
                    <div class="test-card">
                        <div class="test-header">
                            {action['details'].get('lab_test.title', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Display medications
            if action_groups['recommend_medication']:
                st.markdown('<div class="section-subheader">Medications</div>', unsafe_allow_html=True)
                for action in action_groups['recommend_medication']:
                    st.markdown(f"""
                    <div class="medication-card">
                        <div class="medication-header">
                            {action['details'].get('otc.Medicine.name', '')}
                            <span class="medication-pill-badge">{action['details'].get('otc.type', '')}</span>
                        </div>
                        <div class="medication-body">
                            <div style="color: #6B7280; font-size: 14px;">{action['details'].get('otc.title', '')}</div>
                            <div class="medication-info">
                                <div class="medication-info-item">
                                    <div class="info-label">Dosage</div>
                                    <div class="info-value">{action['details'].get('otc.dosage_duration', '')}</div>
                                </div>
                                <div class="medication-info-item">
                                    <div class="info-label">Take</div>
                                    <div class="info-value">{action['details'].get('otc.intake_type', '')}</div>
                                </div>
                                <div class="medication-info-item">
                                    <div class="info-label">Schedule</div>
                                    <div class="info-value">{action['details'].get('otc.intake_schedules', '')}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display advice
            if action_groups['provide_advice']:
                st.markdown('<div class="section-subheader">Medical Advice</div>', unsafe_allow_html=True)
                for action in action_groups['provide_advice']:
                    st.markdown(f"""
                    <div class="advice-card">
                        <div class="advice-header">
                            {action['details'].get('advice.title', '')}
                        </div>
                        <div class="advice-body">
                            {action['details'].get('advice.description', '')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Display red flags
            if action_groups['red_flags']:
                st.markdown('<div class="section-subheader">Warning Signs</div>', unsafe_allow_html=True)
                for action in action_groups['red_flags']:
                    st.markdown(f"""
                    <div class="warning-card">
                        <div class="warning-header">
                            <span class="warning-icon">⚠️</span> Important Warning
                        </div>
                        <div class="warning-body">
                            <strong>{action['details'].get('red_flag.description', '')}</strong>
                            <div style="margin-top: 10px;">
                                If you experience this symptom, please seek immediate medical attention.
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add some spacing before the button
            st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.markdown('<div class="restart-button">', unsafe_allow_html=True)
                if st.button("New Diagnosis", use_container_width=True, key="restart_button"):
                    reset_app()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# # Add footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; color: #64748B; font-size: 14px;">
#     © 2025 Medical Diagnosis Assistant | <a href="#" style="color: #3B82F6; text-decoration: none;">Privacy Policy</a> | <a href="#" style="color: #3B82F6; text-decoration: none;">Terms of Use</a>
# </div>
# """, unsafe_allow_html=True)