"""
Enhanced Sepsis Predictor with Demographic Integration
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier

from src.utils.demographic_constants import (
    Gender, AgeGroup, DemographicConstants
)
# Change these:
from demographic_constants import (
    Gender, AgeGroup, DemographicConstants
)
from population_norms import PopulationNorms

class EnhancedSepsisPredictor:
    """Sepsis predictor enhanced with demographic features"""
    
    def __init__(self):
        self.models = {}
        self.demographic_weights = self._load_demographic_weights()
        
    def _load_demographic_weights(self) -> Dict:
        """Load demographic-specific model weights"""
        return {
            'gender_weights': {
                Gender.MALE: 1.15,
                Gender.FEMALE: 0.95,
                Gender.OTHER: 1.05
            },
            'age_group_weights': {
                AgeGroup.NEONATE: 2.5,
                AgeGroup.INFANT: 2.0,
                AgeGroup.GERIATRIC: 1.8,
                AgeGroup.YOUNG_ADULT: 1.0,
                AgeGroup.MIDDLE_ADULT: 1.2
            }
        }
    
    def extract_demographic_features(self, patient_data: Dict, 
                                    vitals_data: List[Dict]) -> Dict:
        """Extract demographic-enhanced features"""
        age = patient_data.get('age', 50)
        gender = Gender(patient_data.get('gender', 'U'))
        age_group = DemographicConstants.get_age_group(age)
        
        # Get current vitals
        current_vitals = vitals_data[-1] if vitals_data else {}
        
        features = {}
        
        # Basic vitals
        features['heart_rate'] = current_vitals.get('heart_rate', 0)
        features['respiration_rate'] = current_vitals.get('respiration_rate', 0)
        features['temperature'] = current_vitals.get('temperature', 0)
        features['systolic_bp'] = current_vitals.get('blood_pressure_systolic', 0)
        features['diastolic_bp'] = current_vitals.get('blood_pressure_diastolic', 0)
        features['spo2'] = current_vitals.get('spO2', 0)
        
        # Demographic features
        features['age'] = age
        features['gender_numeric'] = self._encode_gender(gender)
        features['age_group_numeric'] = self._encode_age_group(age_group)
        
        # Demographic-adjusted vital scores
        age_group_str = PopulationNorms.get_age_group_from_age(age)
        gender_str = gender.value.lower() if gender != Gender.OTHER else 'other'
        
        # Calculate Z-scores for demographic-adjusted norms
        for metric in ['heart_rate', 'respiration_rate', 'temperature', 'systolic_bp']:
            value = features.get(metric, 0)
            if value > 0:
                z_score = PopulationNorms.calculate_z_score(
                    value, age_group_str, gender_str, metric
                )
                features[f'{metric}_z_score'] = z_score
                features[f'{metric}_demographic_deviation'] = abs(z_score)
        
        # Demographic risk multipliers
        features['gender_risk_multiplier'] = self.demographic_weights['gender_weights'].get(gender, 1.0)
        features['age_risk_multiplier'] = self.demographic_weights['age_group_weights'].get(age_group, 1.0)
        features['demographic_risk_score'] = features['gender_risk_multiplier'] * features['age_risk_multiplier']
        
        # Age-specific patterns
        features['is_geriatric'] = 1 if age_group == AgeGroup.GERIATRIC else 0
        features['is_neonate_infant'] = 1 if age_group in [AgeGroup.NEONATE, AgeGroup.INFANT] else 0
        
        # Gender-specific patterns
        features['is_female'] = 1 if gender == Gender.FEMALE else 0
        features['is_male'] = 1 if gender == Gender.MALE else 0
        
        return features
    
    def _encode_gender(self, gender: Gender) -> int:
        """Encode gender as numeric"""
        encoding = {
            Gender.MALE: 0,
            Gender.FEMALE: 1,
            Gender.OTHER: 2,
            Gender.UNKNOWN: 3
        }
        return encoding.get(gender, 3)
    
    def _encode_age_group(self, age_group: AgeGroup) -> int:
        """Encode age group as numeric"""
        encoding = {
            AgeGroup.NEONATE: 0,
            AgeGroup.INFANT: 1,
            AgeGroup.TODDLER: 2,
            AgeGroup.PRESCHOOL: 3,
            AgeGroup.SCHOOL_AGE: 4,
            AgeGroup.ADOLESCENT: 5,
            AgeGroup.YOUNG_ADULT: 6,
            AgeGroup.MIDDLE_ADULT: 7,
            AgeGroup.GERIATRIC: 8
        }
        return encoding.get(age_group, 6)
    
    def predict_with_demographics(self, patient_data: Dict, 
                                 vitals_data: List[Dict]) -> Dict:
        """Make sepsis prediction with demographic adjustment"""
        # Extract features
        features = self.extract_demographic_features(patient_data, vitals_data)
        
        # Base prediction from models
        base_prediction = self._base_prediction(features)
        
        # Demographic adjustment
        demographic_adjustment = self._apply_demographic_adjustment(
            base_prediction, patient_data
        )
        
        # Generate demographic-specific insights
        insights = self._generate_demographic_insights(
            features, patient_data, demographic_adjustment
        )
        
        # Calculate final risk score
        final_risk = self._calculate_final_risk(
            base_prediction, demographic_adjustment
        )
        
        return {
            'patient_id': patient_data.get('patient_id'),
            'age': patient_data.get('age'),
            'gender': patient_data.get('gender'),
            'age_group': DemographicConstants.get_age_group(patient_data.get('age', 50)).value,
            'base_prediction': base_prediction,
            'demographic_adjustment': demographic_adjustment,
            'final_risk_score': final_risk,
            'demographic_risk_level': self._determine_demographic_risk_level(final_risk),
            'insights': insights,
            'demographic_features': features,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _base_prediction(self, features: Dict) -> Dict:
        """Base prediction without demographic adjustment"""
        # This would use the trained ML models
        # For now, return a simplified version
        risk_score = 0.0
        
        # Heart rate contribution
        hr_z = features.get('heart_rate_z_score', 0)
        if abs(hr_z) > 2:
            risk_score += 0.3
        
        # Temperature contribution
        temp_z = features.get('temperature_z_score', 0)
        if temp_z > 2:
            risk_score += 0.4
        
        # Respiratory rate contribution
        rr_z = features.get('respiration_rate_z_score', 0)
        if rr_z > 2:
            risk_score += 0.3
        
        # Normalize to 0-1
        base_risk = min(1.0, risk_score)
        
        return {
            'probability': base_risk,
            'contributing_factors': [],
            'confidence': 0.85
        }
    
    def _apply_demographic_adjustment(self, base_prediction: Dict, 
                                     patient_data: Dict) -> Dict:
        """Apply demographic-specific adjustments to prediction"""
        age = patient_data.get('age', 50)
        gender = Gender(patient_data.get('gender', 'U'))
        age_group = DemographicConstants.get_age_group(age)
        
        base_prob = base_prediction['probability']
        
        # Get demographic multipliers
        gender_multiplier = self.demographic_weights['gender_weights'].get(gender, 1.0)
        age_multiplier = self.demographic_weights['age_group_weights'].get(age_group, 1.0)
        
        # Calculate adjusted probability
        adjusted_prob = base_prob * gender_multiplier * age_multiplier
        adjusted_prob = min(1.0, adjusted_prob)  # Cap at 1.0
        
        # Special adjustments
        adjustments = []
        
        # Neonates and infants
        if age_group in [AgeGroup.NEONATE, AgeGroup.INFANT]:
            adjustments.append("Higher risk due to immature immune system")
            adjusted_prob = min(1.0, adjusted_prob * 1.3)
        
        # Geriatric patients
        if age_group == AgeGroup.GERIATRIC:
            adjustments.append("Higher risk due to immunosenescence and comorbidities")
            adjusted_prob = min(1.0, adjusted_prob * 1.4)
        
        # Gender-specific adjustments
        if gender == Gender.MALE:
            adjustments.append("Males have higher baseline sepsis risk")
        elif gender == Gender.FEMALE:
            adjustments.append("Females may present with different symptom patterns")
        
        return {
            'adjusted_probability': adjusted_prob,
            'gender_multiplier': gender_multiplier,
            'age_multiplier': age_multiplier,
            'total_multiplier': gender_multiplier * age_multiplier,
            'adjustments': adjustments,
            'age_group': age_group.value,
            'gender': gender.value
        }
    
    def _generate_demographic_insights(self, features: Dict, 
                                      patient_data: Dict, 
                                      adjustment: Dict) -> List[str]:
        """Generate demographic-specific clinical insights"""
        age = patient_data.get('age', 50)
        gender = Gender(patient_data.get('gender', 'U'))
        age_group = DemographicConstants.get_age_group(age)
        
        insights = []
        
        # Age-specific insights
        if age_group == AgeGroup.NEONATE:
            insights.append("Neonate: Sepsis may present with temperature instability, feeding difficulties, or lethargy")
            insights.append("Consider maternal risk factors and early-onset vs late-onset sepsis")
        
        elif age_group == AgeGroup.GERIATRIC:
            insights.append("Geriatric: Atypical presentation common - watch for delirium, falls, or functional decline")
            insights.append("Lower fever threshold in elderly (≥37.8°C may be significant)")
        
        # Gender-specific insights
        if gender == Gender.FEMALE:
            insights.append("Female: Consider pregnancy status and gynecological sources of infection")
            insights.append("Higher autoimmune disease prevalence may complicate diagnosis")
        
        elif gender == Gender.MALE:
            insights.append("Male: Higher baseline mortality risk from sepsis")
            insights.append("Consider prostate/urinary sources in older males")
        
        # Vital sign insights based on demographic norms
        for metric in ['heart_rate', 'respiration_rate', 'temperature']:
            z_score = features.get(f'{metric}_z_score', 0)
            if abs(z_score) > 2:
                insights.append(
                    f"{metric.replace('_', ' ').title()} significantly "
                    f"{'elevated' if z_score > 0 else 'reduced'} for {age_group} {gender}"
                )
        
        # Demographic risk factor insights
        total_multiplier = adjustment['total_multiplier']
        if total_multiplier > 1.5:
            insights.append(f"High demographic risk multiplier ({total_multiplier:.1f}x) - increased vigilance needed")
        
        return insights
    
    def _calculate_final_risk(self, base_prediction: Dict, 
                             demographic_adjustment: Dict) -> Dict:
        """Calculate final risk score with demographic adjustment"""
        base_prob = base_prediction['probability']
        adjusted_prob = demographic_adjustment['adjusted_probability']
        
        # Weighted combination
        demographic_weight = 0.3  # Weight given to demographic factors
        clinical_weight = 0.7     # Weight given to clinical factors
        
        final_prob = (clinical_weight * base_prob + 
                     demographic_weight * adjusted_prob)
        
        # Ensure reasonable bounds
        final_prob = max(0.0, min(1.0, final_prob))
        
        return {
            'probability': final_prob,
            'base_contribution': base_prob * clinical_weight,
            'demographic_contribution': adjusted_prob * demographic_weight,
            'demographic_weight': demographic_weight,
            'clinical_weight': clinical_weight
        }
    
    def _determine_demographic_risk_level(self, final_risk: Dict) -> str:
        """Determine risk level with demographic context"""
        prob = final_risk['probability']
        
        if prob < 0.1:
            return "VERY_LOW"
        elif prob < 0.3:
            return "LOW"
        elif prob < 0.5:
            return "MODERATE"
        elif prob < 0.7:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    def predict_population_risk(self, patients_data: List[Dict]) -> Dict:
        """Analyze sepsis risk across population demographics"""
        gender_risks = {'M': [], 'F': [], 'O': []}
        age_group_risks = {}
        
        all_predictions = []
        
        for patient in patients_data:
            # Simulate vitals for population analysis
            vitals = [{
                'heart_rate': 80 + np.random.randint(-20, 40),
                'respiration_rate': 18 + np.random.randint(-6, 10),
                'temperature': 37.0 + np.random.uniform(-0.5, 1.5),
                'blood_pressure_systolic': 120 + np.random.randint(-20, 30),
                'blood_pressure_diastolic': 80 + np.random.randint(-10, 20),
                'spO2': 96 + np.random.randint(-4, 4)
            }]
            
            prediction = self.predict_with_demographics(patient, vitals)
            all_predictions.append(prediction)
            
            # Aggregate by gender
            gender = patient.get('gender', 'U')
            if gender in gender_risks:
                gender_risks[gender].append(prediction['final_risk_score']['probability'])
            
            # Aggregate by age group
            age_group = DemographicConstants.get_age_group(patient.get('age', 50))
            if age_group.value not in age_group_risks:
                age_group_risks[age_group.value] = []
            age_group_risks[age_group.value].append(prediction['final_risk_score']['probability'])
        
        # Calculate statistics
        gender_stats = {}
        for gender, risks in gender_risks.items():
            if risks:
                gender_stats[gender] = {
                    'mean_risk': np.mean(risks),
                    'std_risk': np.std(risks),
                    'count': len(risks),
                    'high_risk_count': sum(1 for r in risks if r > 0.5)
                }
        
        age_group_stats = {}
        for age_group, risks in age_group_risks.items():
            if risks:
                age_group_stats[age_group] = {
                    'mean_risk': np.mean(risks),
                    'std_risk': np.std(risks),
                    'count': len(risks),
                    'high_risk_proportion': sum(1 for r in risks if r > 0.5) / len(risks)
                }
        
        # Identify high-risk demographics
        high_risk_groups = []
        for age_group, stats in age_group_stats.items():
            if stats['mean_risk'] > 0.4:
                high_risk_groups.append({
                    'demographic': f"Age Group: {age_group}",
                    'mean_risk': stats['mean_risk'],
                    'reason': "High baseline risk due to age-related factors"
                })
        
        return {
            'population_summary': {
                'total_patients': len(all_predictions),
                'overall_mean_risk': np.mean([p['final_risk_score']['probability'] 
                                            for p in all_predictions]),
                'high_risk_patients': sum(1 for p in all_predictions 
                                        if p['final_risk_score']['probability'] > 0.5)
            },
            'gender_analysis': gender_stats,
            'age_group_analysis': age_group_stats,
            'high_risk_demographics': high_risk_groups,
            'recommendations': self._generate_population_recommendations(
                gender_stats, age_group_stats
            )
        }
    
    def _generate_population_recommendations(self, gender_stats: Dict, 
                                           age_group_stats: Dict) -> List[str]:
        """Generate recommendations based on population risk analysis"""
        recommendations = []
        
        # Gender-based recommendations
        if 'M' in gender_stats and 'F' in gender_stats:
            male_risk = gender_stats['M']['mean_risk']
            female_risk = gender_stats['F']['mean_risk']
            
            if male_risk > female_risk * 1.2:
                recommendations.append(
                    "Higher sepsis risk in males detected. Consider gender-specific "
                    "screening protocols and education about male sepsis awareness."
                )
        
        # Age-group based recommendations
        high_risk_age_groups = []
        for age_group, stats in age_group_stats.items():
            if stats['mean_risk'] > 0.4:
                high_risk_age_groups.append(age_group)
        
        if high_risk_age_groups:
            recommendations.append(
                f"High sepsis risk in {', '.join(high_risk_age_groups)}. "
                f"Implement targeted monitoring and early intervention protocols "
                f"for these age groups."
            )
        
        # General recommendations
        recommendations.append(
            "Implement demographic-specific vital sign thresholds in monitoring systems"
        )
        recommendations.append(
            "Train staff on demographic variations in sepsis presentation"
        )
        recommendations.append(
            "Develop age and gender-specific sepsis screening tools"
        )
        
        return recommendations