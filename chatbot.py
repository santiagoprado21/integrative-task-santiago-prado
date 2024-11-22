from rules import TroubleshootingExpert
from bayesian_model import BayesianNetwork, VehicleDiagnosis
from experta import Fact
from rules import pass_evidence_to_engine

class DiagnosticChatbot:
    """Chatbot de diagnóstico con múltiples preguntas y análisis probabilístico."""

    def __init__(self):
        self.rule_engine = TroubleshootingExpert() 
        self.bayesian_handler = BayesianNetwork() 
        self.evidence = {}  
        self.bayesian_handler = VehicleDiagnosis()

    def ask_question(self, question, valid_responses=None):
        """Pregunta al usuario asegurando respuestas válidas."""
        if valid_responses is None:
            valid_responses = ["yes", "no"]
        while True:
            response = input(f"{question} ({'/'.join(valid_responses)}): ").strip().lower()
            if response in valid_responses:
                return response
            print(f"Por favor, responde con una de las siguientes opciones: {', '.join(valid_responses)}.")

    def collect_bayesian_evidence(self):
        """Recolecta evidencia detallada para el modelo bayesiano."""
        print("\nRespondamos algunas preguntas relacionadas con los síntomas.")
        
        self.evidence['difficulty_starting'] = 1 if self.ask_question("¿Tu vehículo tiene dificultad para arrancar?", ["si", "no"]) == "si" else 0
        
        if self.evidence['difficulty_starting']:
            self.evidence['battery_ok'] = 1 if self.ask_question("¿La batería parece estar cargada?", ["si", "no"]) == "si" else 0
            self.evidence['starter_sound'] = 1 if self.ask_question("¿Escuchas el sonido del motor de arranque?", ["si", "no"]) == "si" else 0
            self.evidence['fuel_smell'] = 1 if self.ask_question("¿Notas olor a combustible?", ["si", "no"]) == "si" else 0

        self.evidence['brake_issue'] = 1 if self.ask_question("¿Los frenos suenan raro al utilizarlos?", ["si", "no"]) == "si" else 0

        if self.evidence['brake_issue']:
            self.evidence['brake_problem_frequency'] = 1 if self.ask_question("¿El problema con los frenos ocurre frecuentemente?", ["si", "no"]) == "si" else 0
            self.evidence['noise_type'] = 1 if self.ask_question("¿Los frenos funcionan con normalidad?", ["si", "no"]) == "si" else 0
            
        
        self.evidence['overheating'] = 1 if self.ask_question("¿Tu vehículo se sobrecalienta?", ["si", "no"]) == "si" else 0
        if self.evidence['overheating']:
            self.evidence['coolant_level'] = 1 if self.ask_question("¿El nivel de refrigerante está bajo?", ["si", "no"]) == "si" else 0
            self.evidence['fan_function'] = 1 if self.ask_question("¿El ventilador del radiador está funcionando?", ["si", "no"]) == "si" else 0
            self.evidence['leak_presence'] = 1 if self.ask_question("¿Ves signos de fuga de refrigerante?", ["si", "no"]) == "si" else 0
        
        self.evidence['vibrations'] = 1 if self.ask_question("¿Sientes vibraciones mientras conduces?", ["si", "no"]) == "si" else 0
        if self.evidence['vibrations']:
            self.evidence['speed_dependency'] = 1 if self.ask_question("¿Las vibraciones aumentan con la velocidad?", ["si", "no"]) == "si" else 0
            self.evidence['tire_wear'] = 1 if self.ask_question("¿Notas desgaste en las llantas?", ["si", "no"]) == "si" else 0
            self.evidence['steering_vibrates'] = 1 if self.ask_question("¿El volante vibra mientras conduces?", ["si", "no"]) == "si" else 0

    def diagnose(self):
        """Realiza el diagnóstico basado en las reglas y el análisis bayesiano."""
        print("\nIniciando el diagnóstico...")

        print("\nEvaluando con el modelo bayesiano...")
        bayesian_diagnosis = self.bayesian_handler.infer(self.evidence)
        sorted_diagnosis = sorted(bayesian_diagnosis.items(), key=lambda x: x[1], reverse=True)
        top_three = sorted_diagnosis[:3]

        print("\nEvaluando con el motor de reglas...")
        rule_based_diagnosis = pass_evidence_to_engine(self.evidence,bayesian_diagnosis)

        print("\nResultados del diagnóstico:")
        print(f"- Diagnóstico basado en reglas: {rule_based_diagnosis}")
        print(f"- Diagnóstico basado en modelo bayesiano: ")
        for diagnosis, probability in top_three:
            print(f"- {diagnosis}: {probability:.2f}")
        return {
            "Esperamos te haya servido nuestro Chatbot :)"
        }


    def run(self):
        """Ejecuta el chatbot."""
        print("Bienvenido al Chatbot de Diagnóstico de Vehículos.")
        self.collect_bayesian_evidence() 
        diagnosis_results = self.diagnose()  
        


chatbot = DiagnosticChatbot()
chatbot.run()



