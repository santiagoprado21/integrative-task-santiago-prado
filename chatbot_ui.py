import streamlit as st
from rules import TroubleshootingExpert
from bayesian_model import BayesianNetwork, VehicleDiagnosis
from rules import pass_evidence_to_engine
import matplotlib.pyplot as plt


class DiagnosticChatbot:
    """Chatbot de diagnóstico con flujo condicional basado en evidencia."""

    def __init__(self):
        self.rule_engine = TroubleshootingExpert()
        self.evidence = {}
        self.bayesian_handler = VehicleDiagnosis()
        self.questions = [
            {
                "key": "difficulty_starting",
                "text": "¿Tu vehículo tiene dificultad para arrancar?",
                "options": ["Sí", "No"],
                "follow_up": [
                    {
                        "key": "battery_ok",
                        "text": "¿La batería parece estar cargada?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("difficulty_starting") == 1
                    },
                    {
                        "key": "starter_sound",
                        "text": "¿Escuchas el sonido del motor de arranque?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("difficulty_starting") == 1
                    },
                    {
                        "key": "fuel_smell",
                        "text": "¿Notas olor a combustible?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("difficulty_starting") == 1
                    }
                ]
            },
            {
                "key": "brake_issue",
                "text": "¿Los frenos suenan raro al utilizarlos?",
                "options": ["Sí", "No"],
                "follow_up": [
                    {
                        "key": "brake_problem_frequency",
                        "text": "¿El problema con los frenos ocurre frecuentemente?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("brake_issue") == 1
                    },
                    {
                        "key": "noise_type",
                        "text": "¿Los frenos funcionan con normalidad?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("brake_issue") == 1
                    }
                ]
            },
            {
                "key": "overheating",
                "text": "¿Tu vehículo se sobrecalienta?",
                "options": ["Sí", "No"],
                "follow_up": [
                    {
                        "key": "coolant_level",
                        "text": "¿El nivel de refrigerante está bajo?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("overheating") == 1
                    },
                    {
                        "key": "fan_function",
                        "text": "¿El ventilador del radiador está funcionando?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("overheating") == 1
                    },
                    {
                        "key": "leak_presence",
                        "text": "¿Ves signos de fuga de refrigerante?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("overheating") == 1
                    }
                ]
            },
            {
                "key": "vibrations",
                "text": "¿Sientes vibraciones mientras conduces?",
                "options": ["Sí", "No"],
                "follow_up": [
                    {
                        "key": "speed_dependency",
                        "text": "¿Las vibraciones aumentan con la velocidad?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("vibrations") == 1
                    },
                    {
                        "key": "tire_wear",
                        "text": "¿Notas desgaste en las llantas?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("vibrations") == 1
                    },
                    {
                        "key": "steering_vibrates",
                        "text": "¿El volante vibra mientras conduces?",
                        "options": ["Sí", "No"],
                        "condition": lambda e: e.get("vibrations") == 1
                    }
                ]
            }
        ]

    def update_evidence(self, key, value):
        self.evidence[key] = value
        print("Evidencia actualizada:", self.evidence)

    def diagnose(self, evidence=None):
        """Realiza el diagnóstico basado en las reglas y el análisis bayesiano."""
        self.evidence = st.session_state.evidence if evidence is None else evidence

        print("Evidencia antes de diagnóstico:", self.evidence)

        if not self.evidence:
            print("Error: No hay evidencia para diagnosticar.")
            return {"rule_based": {}, "bayesian": {}}

        bayesian_diagnosis = self.bayesian_handler.infer(self.evidence)
        print("Diagnóstico bayesiano intermedio:", bayesian_diagnosis)

        print("Evidencia enviada al motor de reglas:", self.evidence)
        rule_based_diagnosis = pass_evidence_to_engine(self.evidence, bayesian_diagnosis)
        print("Diagnóstico basado en reglas intermedio:", rule_based_diagnosis)

        if isinstance(rule_based_diagnosis, list):
            sorted_rule_based = rule_based_diagnosis[:3]  
        elif isinstance(rule_based_diagnosis, dict):
            sorted_rule_based = sorted(rule_based_diagnosis.items(), key=lambda x: x[1], reverse=True)[:3]
        else:
            sorted_rule_based = ["Diagnóstico basado en reglas no disponible"]

        if not bayesian_diagnosis:
            sorted_bayesian = ["Diagnóstico bayesiano no disponible"]
        else:
            sorted_bayesian = sorted(bayesian_diagnosis.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "rule_based": sorted_rule_based,
            "bayesian": sorted_bayesian
        }


    def get_next_question(self, evidence):
        """Obtiene la siguiente pregunta en el flujo."""
        for question in self.questions:
            if question["key"] not in evidence:
                return question
            for follow_up in question.get("follow_up", []):
                if follow_up["key"] not in evidence and follow_up["condition"](evidence):
                    return follow_up
        return None



st.title("Chatbot de Diagnóstico de Vehículos 🚗")

if "evidence" not in st.session_state:
    st.session_state.evidence = {}
if "chat_progress" not in st.session_state:
    st.session_state.chat_progress = []

chatbot = DiagnosticChatbot()

progress = len(st.session_state.evidence) / len(chatbot.questions)
progress = min(1.0, progress)
st.progress(progress)

for entry in st.session_state.chat_progress:
    if entry['role'] == "Usuario":
        st.markdown(f"<div style='background-color:#e0f7fa;padding:10px;border-radius:5px;margin-bottom:10px;'><strong>Usuario:</strong> {entry['text']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:#f9f9f9;padding:10px;border-radius:5px;margin-bottom:10px;'><strong>Chatbot:</strong> {entry['text']}</div>", unsafe_allow_html=True)



next_question = chatbot.get_next_question(st.session_state.evidence)
if next_question:
    with st.form(key=next_question["key"]):
        st.write(next_question["text"])
        response = st.radio("Selecciona una opción:", next_question["options"], key=f"response_{next_question['key']}")
        submitted = st.form_submit_button("Responder")

        if submitted:
            
            st.session_state.evidence[next_question["key"]] = 1 if response == "Sí" else 0
            chatbot.evidence = st.session_state.evidence

            print("Evidencia actualizada:", st.session_state.evidence)

            st.session_state.chat_progress.append({"role": "Chatbot", "text": next_question["text"]})
            st.session_state.chat_progress.append({"role": "Usuario", "text": response})
            

            st.session_state.evidence = chatbot.evidence
            st.rerun()

else:
    st.write("## **Diagnóstico final**")

# Establecer la evidencia para diagnóstico
    chatbot.evidence = st.session_state.evidence
    results = chatbot.diagnose()

    # Mostrar diagnóstico basado en reglas con formato
    st.write("### **Diagnóstico basado en reglas**:")
    results["rule_based"]

    # Separador visual
    st.markdown("---")

    # Mostrar diagnóstico basado en modelo bayesiano con formato
    st.write("### **Diagnóstico basado en modelo bayesiano**:")
    if results["bayesian"]:
        for diagnosis, probability in results["bayesian"]:
            try:
                # Intentar convertir la probabilidad a float y mostrarla
                formatted_probability = float(probability)
                st.markdown(f"- **{diagnosis}** - _Probabilidad_: {formatted_probability:.2f}")
            except ValueError:
                # Si la probabilidad no es un número, se muestra tal cual
                st.markdown(f"- **{diagnosis}** - _Probabilidad_: {probability}")
    else:
        st.markdown("No se ha encontrado diagnóstico basado en el modelo bayesiano :warning:")

    st.markdown("#### Diagnóstico basado en modelo bayesiano:")
    probs = [prob for _, prob in results["bayesian"]]
    labels = [diag for diag, _ in results["bayesian"]]


    if probs:

        fig, ax = plt.subplots()
        ax.barh(labels, probs, color="skyblue")
        ax.set_xlabel("Probabilidad")
        ax.set_title("Diagnóstico Bayesiano")
        st.pyplot(fig)
    else:
        st.write("No hay diagnósticos bayesianos disponibles.")


    st.markdown("---")
    st.write("👨‍🔧 **¡Recuerda que este diagnóstico es solo informativo! Para un diagnóstico preciso, te recomendamos visitar un mecánico especializado.**")

    st.markdown(
        """
        <div style="background-color: #f2f2f2; padding: 10px; border-radius: 5px;">
            <h4 style="color: #333333;">Consejo:</h4>
            <p style="color: #666666;">Si tu vehículo muestra síntomas graves, considera llevarlo a un especialista cuanto antes. 🚗⚠️</p>
        </div>
        """, unsafe_allow_html=True
    )





