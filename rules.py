from experta import KnowledgeEngine, Rule, Fact

class TroubleshootingExpert(KnowledgeEngine):
    """Motor de reglas extendido con múltiples preguntas por síntoma y diagnóstico bayesiano."""

    @Rule(Fact(difficulty_starting=1))
    def set_symptom_difficulty_starting(self):
        self.declare(Fact(symptom="difficulty_starting"))

    @Rule(Fact(brake_issue=1))
    def set_symptom_brake_issue(self):
        self.declare(Fact(symptom="brake_issue"))

    @Rule(Fact(overheating=1))
    def set_symptom_overheating(self):
        self.declare(Fact(symptom="overheating"))

    @Rule(Fact(vibrations=1))
    def set_symptom_overheating(self):
        self.declare(Fact(symptom="vibrations"))

    @Rule(Fact(symptom="difficulty_starting"), Fact(battery_ok=1), Fact(starter_sound=0), Fact(fuel_smell=0))
    def diagnose_ignition(self):
        self.declare(Fact(diagnosis="Problema en el sistema de encendido (bujías, cables)"))

    @Rule(Fact(symptom="difficulty_starting"), Fact(battery_ok=0), Fact(starter_sound=0), Fact(fuel_smell=0))
    def diagnose_battery(self):
        self.declare(Fact(diagnosis="La batería está descargada o desconectada"))

    @Rule(Fact(symptom="brake_issue"), Fact(brake_problem_frequency=1), Fact(noise_type=1))
    def diagnose_brakes(self):
        print("Regla de frenos activada")
        self.declare(Fact(diagnosis="Revisar pastillas y liquido de frenos"))

    @Rule(Fact(symptom="brake_issue"), Fact(brake_problem_frequency=1), Fact(noise_type=0))
    def diagnose_brakes2(self):
        self.declare(Fact(diagnosis="Acudir al mecanico para diagnosticar problema en los frenos"))

    @Rule(Fact(symptom="overheating"), Fact(coolant_level=0), Fact(fan_function=0), Fact(leak_presence=0))
    def diagnose_radiator(self):
        self.declare(Fact(diagnosis="Problema con el radiador"))

    @Rule(Fact(symptom="overheating"), Fact(coolant_level=1), Fact(fan_function=1), Fact(leak_presence=0))
    def diagnose_radiator2(self):
        self.declare(Fact(diagnosis="Recargue el nivel de refrigerante"))
    
    @Rule(Fact(symptom="vibrations"), Fact(speed_dependency=1), Fact(tire_wear=0), Fact(steering_vibrates=1))
    def diagnose_tires_or_alignment(self):
        self.declare(Fact(diagnosis="Desbalanceo de ruedas, llevar al mecanico para un balanceo"))

    @Rule(Fact(symptom="vibrations"), Fact(speed_dependency=1), Fact(tire_wear=1), Fact(steering_vibrates=0))
    def diagnose_tires_or_alignment2(self):
        self.declare(Fact(diagnosis="Desgate grave en las llantas, cambielas y reduzca la velocidad"))

    @Rule(Fact(battery_issue_prob= lambda x: 0.15 <= x <= 0.25))
    def diagnose_battery_from_bayesian(self):
        print("Regla activada: diagnose_battery_from_bayesian")
        print("Probabilidad de fallo de batería según el modelo bayesiano: 0.2")
        self.declare(Fact(diagnosis="La batería podría estar descargada o desconectada (probabilidad alta)"))

    @Rule(Fact(ignition_issue_prob=0.15))
    def diagnose_ignition_from_bayesian(self):
        print("Regla activada: diagnose_ignition_from_bayesian")
        print("Probabilidad de fallo de encendido según el modelo bayesiano: 0.15")
        self.declare(Fact(diagnosis="Posible fallo en el sistema de encendido"))

    @Rule(Fact(coolant_leak_prob=0.0805))
    def diagnose_coolant_leak(self):
        print("Regla activada: diagnose_coolant_leak")
        print("Probabilidad de fuga de refrigerante según el modelo bayesiano: 0.0805")
        self.declare(Fact(diagnosis="Posible fuga de refrigerante"))

    @Rule(Fact(radiator_issue_prob=0.115))
    def diagnose_radiator_from_bayesian(self):
        print("Regla activada: diagnose_radiator_from_bayesian")
        print("Probabilidad de fallo en radiador según el modelo bayesiano: 0.115")
        self.declare(Fact(diagnosis="Posible problema con el radiador"))

    @Rule(Fact(tire_issue_prob=0.1904))
    def diagnose_tire_issue(self):
        print("Regla activada: diagnose_tire_issue")
        print("Probabilidad de fallo en llantas según el modelo bayesiano: 0.1904")
        self.declare(Fact(diagnosis="Posible problema con las llantas"))

    @Rule(Fact(engine_mount_issue_prob=0.2))
    def diagnose_engine_mount(self):
        print("Regla activada: diagnose_engine_mount")
        print("Probabilidad de fallo en montura del motor según el modelo bayesiano: 0.2")
        self.declare(Fact(diagnosis="Posible fallo en la montura del motor"))

    def get_diagnosis(self):
        """Recupera todos los diagnósticos declarados."""
        diagnosis_facts = []
        for fact in self.facts.values():
            if 'diagnosis' in fact:
                diagnosis_facts.append(fact['diagnosis'])
        return diagnosis_facts


def pass_evidence_to_engine(evidence, bayesian_diagnosis):
    print("Evidencia recibida en motor de reglas:", evidence)
    print("Diagnóstico bayesiano:", bayesian_diagnosis)
    rule_engine = TroubleshootingExpert()
    rule_engine.reset()  

    for key, value in evidence.items():
        rule_engine.declare(Fact(**{key: value}))

    for issue, probability in bayesian_diagnosis.items():
        rule_engine.declare(Fact(issue_prob=probability))

    rule_engine.run()
    return rule_engine.get_diagnosis()  
