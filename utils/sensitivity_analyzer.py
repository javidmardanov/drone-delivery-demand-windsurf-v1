import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol

class SensitivityAnalyzer:
    def __init__(self):
        self.problem = {
            'num_vars': 6,
            'names': ['alpha', 'beta', 'epsilon', 'zeta', 'eta', 'lambda_0'],
            'bounds': [
                [0.0, 2.0],  # alpha
                [0.0, 2.0],  # beta
                [0.0, 2.0],  # epsilon
                [0.0, 2.0],  # zeta
                [0.0, 2.0],  # eta
                [0.0, 100.0]  # lambda_0
            ]
        }
    
    def generate_samples(self, N=1000):
        """
        Generate parameter samples for sensitivity analysis using Saltelli's method
        """
        return saltelli.sample(self.problem, N)
    
    def run_analysis(self, model_func, samples):
        """
        Run sensitivity analysis using Sobol indices
        
        Parameters:
        - model_func: Function that takes parameters and returns model output
        - samples: Parameter samples generated by generate_samples()
        
        Returns:
        - Dictionary containing first-order (S1), second-order (S2), and total-order (ST) indices
        """
        # Run model for all parameter samples
        Y = np.array([model_func(sample) for sample in samples])
        
        # Calculate Sobol indices
        results = sobol.analyze(self.problem, Y)
        
        return {
            'S1': dict(zip(self.problem['names'], results['S1'])),
            'S2': results['S2'],
            'ST': dict(zip(self.problem['names'], results['ST'])),
            'confidence': {
                'S1': dict(zip(self.problem['names'], results['S1_conf'])),
                'ST': dict(zip(self.problem['names'], results['ST_conf']))
            }
        }
    
    def get_parameter_rankings(self, sensitivity_results):
        """
        Rank parameters by their total-order Sobol indices
        """
        ST = sensitivity_results['ST']
        rankings = sorted(ST.items(), key=lambda x: x[1], reverse=True)
        return rankings
