"""
Demographic Analyzer for Gender and Age Group Analysis
Analyzes patient data across demographic dimensions
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, date
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px

# Try to import demographic constants from a few common locations.
# Many projects expose modules under a top-level `src` package when installed
# or when running from the repository root; when running the file directly
# from Downloads (or another folder) that package path may not exist.
try:
    from src.utils.demographic_constants import (
        Gender, AgeGroup, AgeSubGroup,
        DemographicConstants
    )
except Exception:
    # Try a few fallbacks: a local `utils` package, or a module in the same dir.
    try:
        from utils.demographic_constants import (
            Gender, AgeGroup, AgeSubGroup,
            DemographicConstants
        )
    except Exception:
        try:
            from demographic_constants import (
                Gender, AgeGroup, AgeSubGroup,
                DemographicConstants
            )
        except Exception:
            # As a last resort, add the parent directory to sys.path and try again.
            import os
            import sys

            parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            if parent not in sys.path:
                sys.path.insert(0, parent)

            try:
                from src.utils.demographic_constants import (
                    Gender, AgeGroup, AgeSubGroup,
                    DemographicConstants
                )
            except Exception:
                # Provide a clear error explaining what to do next.
                raise ModuleNotFoundError(
                    "Could not import 'demographic_constants'.\n"
                    "Tried: 'src.utils.demographic_constants', 'utils.demographic_constants', and 'demographic_constants'.\n"
                    "If this module is part of your project, either:\n"
                    "  * Run the script from the project root where the 'src' package is resolvable, or\n"
                    "  * Install the package (pip install -e .) so 'src' is importable, or\n"
                    "  * Move 'demographic_constants.py' into the same folder as this script or create a 'utils' package.\n"
                )

@dataclass
class DemographicProfile:
    """Patient demographic profile"""
    patient_id: str
    age: int
    gender: Gender
    age_group: AgeGroup
    age_subgroup: Optional[AgeSubGroup] = None
    comorbidities: List[str] = None
    medications: List[str] = None
    ethnicity: Optional[str] = None
    bmi: Optional[float] = None
    smoking_status: Optional[str] = None
    
    def __post_init__(self):
        if self.comorbidities is None:
            self.comorbidities = []
        if self.medications is None:
            self.medications = []

class DemographicAnalyzer:
    """Analyzes patient data across gender and age groups"""
    
    def __init__(self):
        self.demographic_data = {}
        self.gender_stats = {}
        self.age_group_stats = {}
        
    def add_patient_profile(self, profile: DemographicProfile):
        """Add a patient's demographic profile"""
        self.demographic_data[profile.patient_id] = profile
        
    def analyze_gender_differences(self, clinical_data: Dict) -> Dict:
        """Analyze clinical differences between genders"""
        male_data = []
        female_data = []
        other_data = []
        
        for patient_id, vitals in clinical_data.items():
            profile = self.demographic_data.get(patient_id)
            if not profile:
                continue
                
            if profile.gender == Gender.MALE:
                male_data.append(vitals)
            elif profile.gender == Gender.FEMALE:
                female_data.append(vitals)
            else:
                other_data.append(vitals)
        
        # Convert to DataFrames
        male_df = pd.DataFrame(male_data) if male_data else pd.DataFrame()
        female_df = pd.DataFrame(female_data) if female_data else pd.DataFrame()
        
        analysis = {
            'gender_counts': {
                'male': len(male_data),
                'female': len(female_data),
                'other': len(other_data)
            },
            'gender_comparisons': {}
        }
        
        # Compare key metrics
        metrics = ['heart_rate', 'temperature', 'respiration_rate', 'systolic_bp']
        
        for metric in metrics:
            if not male_df.empty and not female_df.empty:
                male_values = male_df[metric].dropna()
                female_values = female_df[metric].dropna()
                
                if len(male_values) > 1 and len(female_values) > 1:
                    # T-test for difference
                    t_stat, p_value = stats.ttest_ind(male_values, female_values, 
                                                      equal_var=False)
                    
                    analysis['gender_comparisons'][metric] = {
                        'male_mean': float(male_values.mean()),
                        'female_mean': float(female_values.mean()),
                        'mean_difference': float(male_values.mean() - female_values.mean()),
                        't_statistic': float(t_stat),
                        'p_value': float(p_value),
                        'significant': p_value < 0.05
                    }
        
        return analysis
    
    def analyze_age_group_trends(self, clinical_data: Dict) -> Dict:
        """Analyze trends across different age groups"""
        age_group_data = {ag: [] for ag in AgeGroup}
        
        for patient_id, vitals in clinical_data.items():
            profile = self.demographic_data.get(patient_id)
            if not profile:
                continue
                
            age_group_data[profile.age_group].append(vitals)
        
        analysis = {
            'age_group_counts': {},
            'age_group_means': {},
            'age_trends': {}
        }
        
        metrics = ['heart_rate', 'temperature', 'respiration_rate', 'systolic_bp']
        
        for age_group, data_list in age_group_data.items():
            analysis['age_group_counts'][age_group.value] = len(data_list)
            
            if data_list:
                df = pd.DataFrame(data_list)
                for metric in metrics:
                    if metric in df.columns:
                        values = df[metric].dropna()
                        if not values.empty:
                            if metric not in analysis['age_group_means']:
                                analysis['age_group_means'][metric] = {}
                            analysis['age_group_means'][metric][age_group.value] = {
                                'mean': float(values.mean()),
                                'std': float(values.std()),
                                'count': len(values)
                            }
        
        # Analyze age trends
        for metric in metrics:
            if metric in analysis['age_group_means']:
                age_means = analysis['age_group_means'][metric]
                
                # Create ordered age groups for trend analysis
                age_order = [
                    AgeGroup.NEONATE, AgeGroup.INFANT, AgeGroup.TODDLER,
                    AgeGroup.PRESCHOOL, AgeGroup.SCHOOL_AGE, AgeGroup.ADOLESCENT,
                    AgeGroup.YOUNG_ADULT, AgeGroup.MIDDLE_ADULT, AgeGroup.GERIATRIC
                ]
                
                x = []
                y = []
                for age_group in age_order:
                    if age_group.value in age_means:
                        x.append(age_group.value)
                        y.append(age_means[age_group.value]['mean'])
                
                if len(x) > 1:
                    # Calculate correlation with age (simplified ordinal)
                    age_numeric = list(range(len(x)))
                    correlation = np.corrcoef(age_numeric, y)[0, 1]
                    
                    analysis['age_trends'][metric] = {
                        'age_groups': x,
                        'means': y,
                        'correlation': float(correlation),
                        'trend': 'increasing' if correlation > 0.1 else 
                                'decreasing' if correlation < -0.1 else 'stable'
                    }
        
        return analysis
    
    def calculate_demographic_risk_score(self, patient_id: str, 
                                         clinical_data: Dict) -> Dict:
        """Calculate demographic-adjusted risk score"""
        profile = self.demographic_data.get(patient_id)
        if not profile:
            return {}
        
        vitals = clinical_data.get(patient_id, {})
        
        # Get demographic-specific thresholds
        thresholds = DemographicConstants.get_vital_thresholds(
            profile.gender, profile.age
        )
        
        risk_factors = []
        risk_score = 0
        
        # Age-based risk
        age_risk_multiplier = DemographicConstants.AGE_SEPSIS_RISK_FACTORS.get(
            profile.age_group, {}
        ).get('risk_multiplier', 1.0)
        
        # Gender-based risk adjustment
        gender_risk_adjustment = DemographicConstants.get_gender_risk_adjustment(
            profile.gender, profile.age_group
        )
        
        # Check vital signs against demographic-specific thresholds
        if 'heart_rate' in vitals:
            hr = vitals['heart_rate']
            hr_normal_max = thresholds['heart_rate']['normal_max']
            hr_critical = thresholds['heart_rate']['critical']
            
            if hr > hr_critical:
                risk_factors.append(f"Heart rate critically high for {profile.age_group}")
                risk_score += 3
            elif hr > hr_normal_max:
                risk_factors.append(f"Heart rate elevated for {profile.age_group}")
                risk_score += 1
        
        if 'respiration_rate' in vitals:
            rr = vitals['respiration_rate']
            rr_normal_max = thresholds['respiratory_rate']['normal_max']
            rr_critical = thresholds['respiratory_rate']['critical']
            
            if rr > rr_critical:
                risk_factors.append(f"Respiratory rate critically high for {profile.age_group}")
                risk_score += 3
            elif rr > rr_normal_max:
                risk_factors.append(f"Respiratory rate elevated for {profile.age_group}")
                risk_score += 1
        
        if 'temperature' in vitals:
            temp = vitals['temperature']
            temp_fever = thresholds['temperature']['fever']
            
            if temp > temp_fever:
                risk_factors.append(f"Fever for {profile.gender}")
                risk_score += 2
        
        # Apply demographic adjustments
        adjusted_score = risk_score * age_risk_multiplier * gender_risk_adjustment
        
        return {
            'patient_id': patient_id,
            'age': profile.age,
            'gender': profile.gender.value,
            'age_group': profile.age_group.value,
            'raw_risk_score': risk_score,
            'age_risk_multiplier': age_risk_multiplier,
            'gender_risk_adjustment': gender_risk_adjustment,
            'adjusted_risk_score': adjusted_score,
            'risk_factors': risk_factors,
            'risk_level': self._determine_risk_level(adjusted_score),
            'demographic_context': f"{profile.age_group} {profile.gender}"
        }
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from score"""
        if score < 2:
            return "LOW"
        elif score < 5:
            return "MEDIUM"
        elif score < 8:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def create_demographic_dashboard(self, clinical_data: Dict) -> Dict:
        """Create comprehensive demographic dashboard"""
        gender_analysis = self.analyze_gender_differences(clinical_data)
        age_analysis = self.analyze_age_group_trends(clinical_data)
        
        # Calculate individual risk scores
        risk_scores = {}
        for patient_id in self.demographic_data.keys():
            risk_scores[patient_id] = self.calculate_demographic_risk_score(
                patient_id, clinical_data
            )
        
        # Aggregate statistics
        avg_risk_by_gender = {}
        avg_risk_by_age_group = {}
        
        for patient_id, risk_data in risk_scores.items():
            profile = self.demographic_data[patient_id]
            
            # By gender
            gender = profile.gender.value
            if gender not in avg_risk_by_gender:
                avg_risk_by_gender[gender] = []
            avg_risk_by_gender[gender].append(risk_data['adjusted_risk_score'])
            
            # By age group
            age_group = profile.age_group.value
            if age_group not in avg_risk_by_age_group:
                avg_risk_by_age_group[age_group] = []
            avg_risk_by_age_group[age_group].append(risk_data['adjusted_risk_score'])
        
        # Calculate averages
        avg_risk_by_gender = {
            gender: np.mean(scores) if scores else 0
            for gender, scores in avg_risk_by_gender.items()
        }
        
        avg_risk_by_age_group = {
            age_group: np.mean(scores) if scores else 0
            for age_group, scores in avg_risk_by_age_group.items()
        }
        
        return {
            'summary': {
                'total_patients': len(self.demographic_data),
                'gender_distribution': gender_analysis['gender_counts'],
                'age_group_distribution': age_analysis['age_group_counts']
            },
            'gender_analysis': gender_analysis,
            'age_group_analysis': age_analysis,
            'risk_analysis': {
                'avg_risk_by_gender': avg_risk_by_gender,
                'avg_risk_by_age_group': avg_risk_by_age_group,
                'high_risk_patients': [
                    risk for risk in risk_scores.values() 
                    if risk['risk_level'] in ['HIGH', 'CRITICAL']
                ]
            },
            'visualizations': self._create_visualizations(
                gender_analysis, age_analysis, risk_scores
            )
        }
    
    def _create_visualizations(self, gender_analysis: Dict, 
                              age_analysis: Dict, risk_scores: Dict) -> Dict:
        """Create visualization data for dashboard"""
        visualizations = {}
        
        # Gender comparison bar chart
        if 'gender_comparisons' in gender_analysis:
            metrics = list(gender_analysis['gender_comparisons'].keys())
            male_means = []
            female_means = []
            
            for metric in metrics:
                comp = gender_analysis['gender_comparisons'][metric]
                male_means.append(comp['male_mean'])
                female_means.append(comp['female_mean'])
            
            visualizations['gender_comparison_chart'] = {
                'type': 'bar',
                'data': {
                    'metrics': metrics,
                    'male': male_means,
                    'female': female_means
                },
                'title': 'Gender Comparison of Vital Signs'
            }
        
        # Age group trends
        if 'age_trends' in age_analysis:
            for metric, trend_data in age_analysis['age_trends'].items():
                visualizations[f'age_trend_{metric}'] = {
                    'type': 'line',
                    'data': {
                        'age_groups': trend_data['age_groups'],
                        'means': trend_data['means']
                    },
                    'title': f'{metric} Across Age Groups',
                    'trend': trend_data['trend']
                }
        
        # Risk distribution by gender and age
        gender_risks = {}
        age_group_risks = {}
        
        for patient_id, risk_data in risk_scores.items():
            profile = self.demographic_data[patient_id]
            
            gender = profile.gender.value
            if gender not in gender_risks:
                gender_risks[gender] = []
            gender_risks[gender].append(risk_data['adjusted_risk_score'])
            
            age_group = profile.age_group.value
            if age_group not in age_group_risks:
                age_group_risks[age_group] = []
            age_group_risks[age_group].append(risk_data['adjusted_risk_score'])
        
        # Calculate average risks
        avg_gender_risks = {
            gender: np.mean(risks) if risks else 0
            for gender, risks in gender_risks.items()
        }
        
        avg_age_risks = {
            age_group: np.mean(risks) if risks else 0
            for age_group, risks in age_group_risks.items()
        }
        
        visualizations['risk_by_gender'] = {
            'type': 'bar',
            'data': avg_gender_risks,
            'title': 'Average Risk Score by Gender'
        }
        
        visualizations['risk_by_age_group'] = {
            'type': 'bar',
            'data': avg_age_risks,
            'title': 'Average Risk Score by Age Group'
        }
        
        return visualizations
    
    def generate_clinical_insights(self, patient_id: str, 
                                  clinical_data: Dict) -> List[str]:
        """Generate demographic-specific clinical insights"""
        profile = self.demographic_data.get(patient_id)
        if not profile:
            return []
        
        vitals = clinical_data.get(patient_id, {})
        insights = []
        
        # Get demographic-specific thresholds
        thresholds = DemographicConstants.get_vital_thresholds(
            profile.gender, profile.age
        )
        
        # Gender-specific insights
        immune_response = DemographicConstants.GENDER_IMMUNE_RESPONSE.get(
            profile.gender, {}
        )
        
        if immune_response.get('immune_response') == 'stronger' and 'temperature' in vitals:
            if vitals['temperature'] > 38.5:
                insights.append(
                    f"High fever in {profile.gender} may indicate robust immune response. "
                    f"Consider {profile.gender}-specific antipyretic thresholds."
                )
        
        # Age-specific insights
        age_risk_factors = DemographicConstants.AGE_SEPSIS_RISK_FACTORS.get(
            profile.age_group, {}
        )
        
        if age_risk_factors.get('immune_immature'):
            insights.append(
                f"Neonate: High sepsis risk due to immature immune system. "
                f"Lower threshold for antibiotic initiation recommended."
            )
        
        if age_risk_factors.get('atypical_presentation'):
            insights.append(
                f"Geriatric patient: May present with atypical sepsis symptoms. "
                f"Watch for delirium, falls, or functional decline as early signs."
            )
        
        # Pharmacokinetic insights
        pharmacokinetics = DemographicConstants.GENDER_PHARMACOKINETICS.get(
            profile.gender, {}
        )
        
        if pharmacokinetics.get('drug_clearance') == 'slower':
            insights.append(
                f"Female patient: May require adjusted medication dosing due to "
                f"slower drug clearance. Monitor for side effects."
            )
        
        # Check vital signs against demographic norms
        if 'heart_rate' in vitals:
            hr_thresholds = thresholds['heart_rate']
            if vitals['heart_rate'] > hr_thresholds['critical']:
                insights.append(
                    f"Tachycardia exceeds {profile.gender}-specific critical threshold. "
                    f"Consider {profile.age_group}-appropriate fluid management."
                )
        
        if 'respiration_rate' in vitals:
            rr_thresholds = thresholds['respiratory_rate']
            if vitals['respiration_rate'] > rr_thresholds['critical']:
                insights.append(
                    f"Tachypnea exceeds {profile.age_group} norm. "
                    f"Monitor for respiratory fatigue, especially in geriatric patients."
                )
        
        return insights