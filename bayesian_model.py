from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class VehicleDiagnosis:
    def __init__(self):
        self.model = BayesianNetwork([
            ('difficulty_starting', 'ignition_issue'),
            ('starter_sound', 'ignition_issue'),
            ('difficulty_starting', 'battery_issue'),
            ('battery_ok', 'battery_issue'),
            ('fuel_smell', 'ignition_issue'),
            ('noise_type', 'brake_issue'),
            ('brake_problem_frequency', 'brake_issue'),
            ('overheating', 'coolant_leak'),
            ('overheating', 'radiator_issue'),
            ('coolant_level', 'coolant_leak'),
            ('fan_function', 'radiator_issue'),
            ('leak_presence', 'coolant_leak'),
            ('vibrations', 'tire_issue'),
            ('vibrations', 'engine_mount_issue'),
            ('speed_dependency', 'tire_issue'),
            ('tire_wear', 'tire_issue'),
            ('steering_vibrates', 'tire_issue')
        ])

        self.cpd_difficulty_starting = TabularCPD(variable='difficulty_starting', variable_card=2, values=[[0.7], [0.3]])
        self.cpd_battery_ok = TabularCPD(variable='battery_ok', variable_card=2, values=[[0.8], [0.2]])
        self.cpd_starter_sound = TabularCPD(variable='starter_sound', variable_card=2, values=[[0.6], [0.4]])
        self.cpd_fuel_smell = TabularCPD(variable='fuel_smell', variable_card=2, values=[[0.5], [0.5]])
        self.cpd_noise_type = TabularCPD(variable='noise_type', variable_card=2, values=[[0.5], [0.5]])
        self.cpd_brake_responsiveness = TabularCPD(variable='brake_problem_frequency', variable_card=2, values=[[0.7], [0.3]])
        self.cpd_overheating = TabularCPD(variable='overheating', variable_card=2, values=[[0.9], [0.1]])
        self.cpd_coolant_level = TabularCPD(variable='coolant_level', variable_card=2, values=[[0.85], [0.15]])
        self.cpd_fan_function = TabularCPD(variable='fan_function', variable_card=2, values=[[0.95], [0.05]])
        self.cpd_leak_presence = TabularCPD(variable='leak_presence', variable_card=2, values=[[0.8], [0.2]])
        self.cpd_vibrations = TabularCPD(variable='vibrations', variable_card=2, values=[[0.6], [0.4]])
        self.cpd_tire_wear = TabularCPD(variable='tire_wear', variable_card=2, values=[[0.7], [0.3]])
        self.cpd_speed_dependency = TabularCPD(variable='speed_dependency', variable_card=2, values=[[0.6], [0.4]])
        self.cpd_steering_vibrates = TabularCPD(variable='steering_vibrates', variable_card=2, values=[[0.65], [0.35]])

        self.cpd_ignition_issue = TabularCPD(
            variable='ignition_issue', 
            variable_card=2, 
            values=[[0.95, 0.1, 0.8, 0.05, 0.85, 0.15, 0.75, 0.25],
                    [0.05, 0.9, 0.2, 0.95, 0.15, 0.85, 0.25, 0.75]],
            evidence=['difficulty_starting', 'starter_sound', 'fuel_smell'], 
            evidence_card=[2, 2, 2]  
        )

        self.cpd_battery_issue = TabularCPD(variable='battery_issue', variable_card=2, 
                                           values=[[0.9, 0.7, 0.8, 0.6],
                                                   [0.1, 0.3, 0.2, 0.4]],  
                                           evidence=['difficulty_starting', 'battery_ok'], 
                                           evidence_card=[2, 2])

        self.cpd_brake_issue = TabularCPD(variable='brake_issue', variable_card=2, 
                                         values=[[0.85, 0.75, 0.9, 0.8],
                                                 [0.15, 0.25, 0.1, 0.2]],
                                         evidence=['noise_type', 'brake_problem_frequency'], 
                                         evidence_card=[2, 2])


        self.cpd_coolant_leak = TabularCPD(
            variable='coolant_leak', 
            variable_card=2, 
            values=[[0.95, 0.85, 0.9, 0.7, 0.9, 0.75, 0.85, 0.65],
                    [0.05, 0.15, 0.1, 0.3, 0.1, 0.25, 0.15, 0.35]],
            evidence=['overheating', 'coolant_level', 'leak_presence'], 
            evidence_card=[2, 2, 2] 
        )


        self.cpd_radiator_issue = TabularCPD(variable='radiator_issue', variable_card=2, 
                                            values=[[0.9, 0.6, 0.8, 0.7],
                                                    [0.1, 0.4, 0.2, 0.3]],
                                            evidence=['overheating', 'fan_function'], 
                                            evidence_card=[2, 2])


        self.cpd_tire_issue = TabularCPD(
            variable='tire_issue', 
            variable_card=2, 
            values=[[0.85, 0.75, 0.7, 0.8, 0.9, 0.85, 0.75, 0.7, 0.85, 0.8, 0.75, 0.7, 0.8, 0.85, 0.75, 0.7],
                    [0.15, 0.25, 0.3, 0.2, 0.1, 0.15, 0.25, 0.3, 0.15, 0.2, 0.25, 0.3, 0.2, 0.15, 0.25, 0.3]],
            evidence=['vibrations', 'speed_dependency', 'tire_wear', 'steering_vibrates'], 
            evidence_card=[2, 2, 2, 2]
        )


        self.cpd_engine_mount_issue = TabularCPD(variable='engine_mount_issue', variable_card=2, 
                                                values=[[0.8, 0.6],
                                                        [0.2, 0.4]],
                                                evidence=['vibrations'], evidence_card=[2])

        self.model.add_cpds(
            self.cpd_difficulty_starting, self.cpd_battery_ok, self.cpd_starter_sound, self.cpd_fuel_smell, 
            self.cpd_noise_type, self.cpd_brake_responsiveness, self.cpd_overheating, self.cpd_coolant_level, 
            self.cpd_fan_function, self.cpd_leak_presence, self.cpd_vibrations, self.cpd_tire_wear, self.cpd_speed_dependency, 
            self.cpd_steering_vibrates, self.cpd_ignition_issue, self.cpd_battery_issue, self.cpd_brake_issue, 
            self.cpd_coolant_leak, self.cpd_radiator_issue, self.cpd_tire_issue, self.cpd_engine_mount_issue
        )

        self.model.check_model()

    def infer(self, evidence):
        """Realiza la inferencia en el modelo Bayesiano para las evidencias proporcionadas."""
        inference = VariableElimination(self.model)
        result = {}

        for query in ['ignition_issue', 'battery_issue', 'coolant_leak', 'radiator_issue', 'tire_issue', 'engine_mount_issue']:
            try:
                prob = inference.query([query], evidence=evidence)
                result[query] = prob.values[1]
            except Exception as e:
                print(f"Error al realizar la inferencia para {query}: {e}")

        return result

    def diagnose_vehicle(self, evidence):
        """Realiza la inferencia en el modelo Bayesiano con las evidencias proporcionadas."""
        inference = VariableElimination(self.model)
        result = {}

        for query in ['ignition_issue', 'battery_issue', 'brake_issue', 'coolant_leak', 'radiator_issue', 'tire_issue', 'engine_mount_issue']:
            try:
                prob = inference.query([query], evidence=evidence)
                result[query] = prob.values[1]  
            except Exception as e:
                print(f"Error al realizar la inferencia para {query}: {e}")

        most_probable_issue = max(result, key=result.get) if result else "Unknown"
        return {"issue": most_probable_issue, "probability": result.get(most_probable_issue, 0)}
    
    

    