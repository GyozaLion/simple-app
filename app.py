import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="Logic Gate Signal Visualizer", layout="wide")

st.title("Logic Gate Signal Visualizer")
st.markdown("### Interactive Three-Input Logic Gate Behavior Analysis")
st.markdown("Explore how different logic gates behave with customizable signal inputs.")

st.divider()

with st.sidebar:
    st.header("⚙️ Signal Configuration")
    
    st.subheader("Time Settings")
    duration = st.slider("Signal Duration (seconds)", min_value=5, max_value=20, value=10, step=1)
    
    st.subheader("Signal A Settings")
    signal_a_freq = st.slider("Signal A Frequency (Hz)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)
    signal_a_pattern = st.selectbox("Signal A Pattern", ["Clock Pulse", "Half Duration High", "Constant High", "Constant Low"])
    
    st.subheader("Signal C Settings")
    signal_c_pattern = st.selectbox("Signal C Pattern", ["Half Duration High", "Clock Pulse", "Constant High", "Constant Low"])
    signal_c_freq = st.slider("Signal C Frequency (Hz)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)
    
    st.subheader("Logic Gate Type")
    gate_type = st.selectbox("Select Logic Gate", ["AND", "OR", "NAND", "NOR", "XOR"])

def generate_signal(t, pattern, frequency=1.0):
    if pattern == "Clock Pulse":
        return (np.sin(t * np.pi * frequency) > 0).astype(float)
    elif pattern == "Constant High":
        return np.ones_like(t)
    elif pattern == "Constant Low":
        return np.zeros_like(t)
    elif pattern == "Half Duration High":
        signal = np.zeros_like(t)
        signal[t < duration/2] = 1
        return signal
    return np.zeros_like(t)

def apply_logic_gate(a, b, c, gate_type):
    if gate_type == "AND":
        return np.logical_and(np.logical_and(a, b), c).astype(float)
    elif gate_type == "OR":
        return np.logical_or(np.logical_or(a, b), c).astype(float)
    elif gate_type == "NAND":
        return np.logical_not(np.logical_and(np.logical_and(a, b), c)).astype(float)
    elif gate_type == "NOR":
        return np.logical_not(np.logical_or(np.logical_or(a, b), c)).astype(float)
    elif gate_type == "XOR":
        return np.logical_xor(np.logical_xor(a, b), c).astype(float)
    return np.zeros_like(a)

def save_fig_to_bytes(fig, format='png'):
    buf = io.BytesIO()
    fig.savefig(buf, format=format, bbox_inches='tight', dpi=300)
    buf.seek(0)
    return buf.read()

def get_truth_table(gate_type):
    inputs_a = [0, 0, 0, 0, 1, 1, 1, 1]
    inputs_b = [0, 0, 1, 1, 0, 0, 1, 1]
    inputs_c = [0, 1, 0, 1, 0, 1, 0, 1]
    
    outputs = []
    for a, b, c in zip(inputs_a, inputs_b, inputs_c):
        result = apply_logic_gate(np.array([a]), np.array([b]), np.array([c]), gate_type)
        outputs.append(int(result[0]))
    
    return {
        "A": inputs_a,
        "B": inputs_b,
        "C": inputs_c,
        "X (Output)": outputs
    }

t = np.linspace(0, duration, 1000)

signal_A_original = generate_signal(t, signal_a_pattern, signal_a_freq)
signal_C_original = generate_signal(t, signal_c_pattern, signal_c_freq)

signal_A_case_a = np.zeros_like(t)
signal_X_case_a = apply_logic_gate(signal_A_case_a, np.ones_like(t), signal_C_original, gate_type)

signal_X_case_b = apply_logic_gate(signal_A_original, np.ones_like(t), signal_C_original, gate_type)

signal_B_case_c = np.zeros_like(t)
signal_C_case_c = np.zeros_like(t)
signal_X_case_c = apply_logic_gate(signal_A_original, signal_B_case_c, signal_C_case_c, gate_type)

plt.close('all')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14))
plt.subplots_adjust(hspace=0.6)

ax1.set_title(f"a. Output When Input A = LOW ({gate_type} Gate)", fontsize=14, loc='left', fontweight='bold')
ax1.plot(t, signal_A_case_a, color='red', linestyle='--', label='Input A (Forced LOW)', linewidth=2)
ax1.plot(t, signal_X_case_a, color='green', linewidth=3, label='OUTPUT X (Result)')
ax1.set_ylim(-0.5, 1.5)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(['LOW (0)', 'HIGH (1)'])
ax1.grid(True, which='both', axis='x', linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')
ax1.set_xlabel('Time (seconds)')

ax2.set_title(f"b. Output When Input B = HIGH ({gate_type} Gate)", fontsize=14, loc='left', fontweight='bold')
ax2.plot(t, signal_A_original, color='blue', linestyle=':', alpha=0.7, linewidth=2, label='Input A (Original)')
ax2.plot(t, signal_C_original, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Input C (Original)')
ax2.step(t, signal_X_case_b, where='post', color='green', linewidth=3, label='OUTPUT X (Result)')
ax2.fill_between(t, signal_X_case_b, step="post", alpha=0.2, color='green')
ax2.set_ylim(-0.5, 1.5)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['LOW (0)', 'HIGH (1)'])
ax2.grid(True, which='both', axis='x', linestyle=':', alpha=0.6)
ax2.legend(loc='upper right')
ax2.set_xlabel('Time (seconds)')

ax3.set_title(f"c. Output When Input B & C = LOW ({gate_type} Gate)", fontsize=14, loc='left', fontweight='bold')
ax3.plot(t, np.zeros_like(t), color='purple', linestyle='--', linewidth=2, label='Input B & C (Forced LOW)')
ax3.plot(t, signal_A_original, color='blue', linestyle=':', alpha=0.5, linewidth=1.5, label='Input A (Original)')
ax3.plot(t, signal_X_case_c, color='green', linewidth=3, label='OUTPUT X (Result)')
ax3.set_ylim(-0.5, 1.5)
ax3.set_yticks([0, 1])
ax3.set_yticklabels(['LOW (0)', 'HIGH (1)'])
ax3.grid(True, which='both', axis='x', linestyle=':', alpha=0.6)
ax3.legend(loc='upper right')
ax3.set_xlabel('Time (seconds)')

st.pyplot(fig)

col1, col2 = st.columns([1, 1])

with col1:
    st.download_button(
        label="📥 Download Chart as PNG",
        data=save_fig_to_bytes(fig, 'png'),
        file_name=f"logic_gate_{gate_type.lower()}_visualization.png",
        mime="image/png"
    )

with col2:
    st.download_button(
        label="📥 Download Chart as PDF",
        data=save_fig_to_bytes(fig, 'pdf'),
        file_name=f"logic_gate_{gate_type.lower()}_visualization.pdf",
        mime="application/pdf"
    )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Case A: Input A = LOW")
    if gate_type in ["OR", "NOR"]:
        st.info(f"With {gate_type} gate and A=LOW, the output depends on inputs B and C.")
    else:
        st.info(f"With {gate_type} gate and A=LOW, observe how the output behaves based on the gate logic.")

with col2:
    st.markdown("#### Case B: Input B = HIGH")
    st.success(f"With {gate_type} gate and B=HIGH, the output is determined by the logic combination of A and C.")

with col3:
    st.markdown("#### Case C: Input B & C = LOW")
    st.warning(f"With {gate_type} gate when both B and C are LOW, the output follows the gate's specific logic rules.")

st.divider()

st.markdown(f"### {gate_type} Gate Truth Table")
st.markdown(f"Truth table for three-input {gate_type} gate (X = A {gate_type} B {gate_type} C):")

truth_table_data = get_truth_table(gate_type)
st.table(truth_table_data)

gate_descriptions = {
    "AND": "Output is HIGH (1) only when ALL three inputs are HIGH (1).",
    "OR": "Output is HIGH (1) when AT LEAST ONE input is HIGH (1).",
    "NAND": "Output is LOW (0) only when ALL three inputs are HIGH (1). Inverse of AND.",
    "NOR": "Output is HIGH (1) only when ALL three inputs are LOW (0). Inverse of OR.",
    "XOR": "Output is HIGH (1) when an ODD number of inputs are HIGH (1)."
}

st.markdown(f"**Note:** {gate_descriptions.get(gate_type, '')}")
