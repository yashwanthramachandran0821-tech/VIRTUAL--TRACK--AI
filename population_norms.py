"""
Population Norms Database
Gender and Age Group specific normal ranges for vital signs
"""

from typing import Dict, List, Tuple
import numpy as np

class PopulationNorms:
    """Database of population norms for vital signs by gender and age"""
    
    # Heart Rate Norms (bpm) by Age and Gender
    HEART_RATE_NORMS = {
        'neonate': {'male': (120, 160), 'female': (120, 160)},
        'infant': {'male': (80, 140), 'female': (80, 140)},
        'toddler': {'male': (70, 120), 'female': (70, 120)},
        'preschool': {'male': (65, 110), 'female': (65, 110)},
        'school_age': {'male': (60, 100), 'female': (60, 100)},
        'adolescent': {'male': (55, 95), 'female': (60, 100)},
        'young_adult': {'male': (60, 100), 'female': (60, 100)},
        'middle_adult': {'male': (60, 100), 'female': (60, 100)},
        'geriatric': {'male': (60, 100), 'female': (60, 100)}
    }
    
    # Blood Pressure Norms (mmHg) by Age and Gender
    BLOOD_PRESSURE_NORMS = {
        'neonate': {'male': (60, 90), 'female': (60, 90)},
        'infant': {'male': (70, 100), 'female': (70, 100)},
        'toddler': {'male': (80, 110), 'female': (80, 110)},
        'preschool': {'male': (85, 115), 'female': (85, 115)},
        'school_age': {'male': (90, 120), 'female': (90, 120)},
        'adolescent': {'male': (100, 130), 'female': (95, 125)},
        'young_adult': {'male': (110, 135), 'female': (105, 130)},
        'middle_adult': {'male': (115, 140), 'female': (110, 135)},
        'geriatric': {'male': (120, 145), 'female': (115, 140)}
    }
    
    # Respiratory Rate Norms (breaths/min) by Age
    RESPIRATION_NORMS = {
        'neonate': (30, 60),
        'infant': (20, 40),
        'toddler': (20, 30),
        'preschool': (20, 30),
        'school_age': (15, 25),
        'adolescent': (12, 20),
        'young_adult': (12, 20),
        'middle_adult': (12, 20),
        'geriatric': (12, 25)  # Higher upper limit for elderly
    }
    
    # Temperature Norms (°C) by Age and Gender
    TEMPERATURE_NORMS = {
        'neonate': {'male': (36.5, 37.5), 'female': (36.5, 37.5)},
        'infant': {'male': (36.6, 37.7), 'female': (36.6, 37.7)},
        'toddler': {'male': (36.7, 37.8), 'female': (36.7, 37.8)},
        'school_age': {'male': (36.5, 37.5), 'female': (36.5, 37.5)},
        'adult': {'male': (36.5, 37.5), 'female': (36.5, 37.5)},
        'geriatric': {'male': (36.0, 37.2), 'female': (36.0, 37.2)}  # Lower in elderly
    }
    
    # Oxygen Saturation Norms (%) by Age
    SPO2_NORMS = {
        'neonate': (85, 100),
        'infant': (90, 100),
        'child': (94, 100),
        'adult': (95, 100),
        'geriatric': (92, 100)  # Slightly lower in elderly
    }
    
    # Gender-specific fever thresholds
    FEVER_THRESHOLDS = {
        'male': 38.0,
        'female': 38.2,
        'other': 38.1
    }
    
    # Age-group specific sepsis incidence
    SEPSIS_INCIDENCE = {
        'neonate': 2.5,  # per 1000
        'infant': 1.8,
        'child': 0.8,
        'adolescent': 0.6,
        'young_adult': 0.9,
        'middle_adult': 1.2,
        'geriatric': 5.4
    }
    
    # Gender-specific sepsis mortality
    SEPSIS_MORTALITY = {
        'male': 0.28,  # case fatality rate
        'female': 0.24,
        'other': 0.26
    }
    
    @classmethod
    def get_heart_rate_norms(cls, age_group: str, gender: str) -> Tuple[float, float]:
        """Get heart rate normal range for age group and gender"""
        return cls.HEART_RATE_NORMS.get(age_group, {}).get(gender, (60, 100))
    
    @classmethod
    def get_blood_pressure_norms(cls, age_group: str, gender: str) -> Tuple[float, float]:
        """Get blood pressure normal range for age group and gender"""
        return cls.BLOOD_PRESSURE_NORMS.get(age_group, {}).get(gender, (90, 120))
    
    @classmethod
    def get_respiration_norms(cls, age_group: str) -> Tuple[float, float]:
        """Get respiratory rate normal range for age group"""
        return cls.RESPIRATION_NORMS.get(age_group, (12, 20))
    
    @classmethod
    def get_temperature_norms(cls, age_group: str, gender: str) -> Tuple[float, float]:
        """Get temperature normal range for age group and gender"""
        if age_group in ['neonate', 'infant', 'toddler']:
            return cls.TEMPERATURE_NORMS.get(age_group, {}).get(gender, (36.5, 37.5))
        elif age_group == 'geriatric':
            return cls.TEMPERATURE_NORMS.get(age_group, {}).get(gender, (36.0, 37.2))
        else:
            return cls.TEMPERATURE_NORMS.get('adult', {}).get(gender, (36.5, 37.5))
    
    @classmethod
    def get_spo2_norms(cls, age_group: str) -> Tuple[float, float]:
        """Get SpO2 normal range for age group"""
        if age_group == 'neonate':
            return cls.SPO2_NORMS['neonate']
        elif age_group == 'infant':
            return cls.SPO2_NORMS['infant']
        elif age_group in ['toddler', 'preschool', 'school_age']:
            return cls.SPO2_NORMS['child']
        elif age_group == 'geriatric':
            return cls.SPO2_NORMS['geriatric']
        else:
            return cls.SPO2_NORMS['adult']
    
    @classmethod
    def get_fever_threshold(cls, gender: str) -> float:
        """Get gender-specific fever threshold"""
        return cls.FEVER_THRESHOLDS.get(gender, 38.0)
    
    @classmethod
    def get_sepsis_risk(cls, age_group: str, gender: str) -> float:
        """Calculate demographic-adjusted sepsis risk"""
        incidence = cls.SEPSIS_INCIDENCE.get(age_group, 1.0)
        mortality = cls.SEPSIS_MORTALITY.get(gender, 0.26)
        
        # Risk score combining incidence and mortality
        risk_score = incidence * (1 + mortality)
        
        # Adjust for age extremes
        if age_group in ['neonate', 'geriatric']:
            risk_score *= 1.5
        
        return risk_score
    
    @classmethod
    def calculate_z_score(cls, value: float, age_group: str, 
                         gender: str, metric: str) -> float:
        """Calculate Z-score for a vital sign based on population norms"""
        if metric == 'heart_rate':
            norms = cls.get_heart_rate_norms(age_group, gender)
        elif metric == 'systolic_bp':
            norms = cls.get_blood_pressure_norms(age_group, gender)
        elif metric == 'respiration_rate':
            norms = cls.get_respiration_norms(age_group)
        elif metric == 'temperature':
            norms = cls.get_temperature_norms(age_group, gender)
        elif metric == 'spo2':
            norms = cls.get_spo2_norms(age_group)
        else:
            return 0
        
        mean = (norms[0] + norms[1]) / 2
        std = (norms[1] - norms[0]) / 4  # Approximate std from range
        
        if std == 0:
            return 0
        
        z_score = (value - mean) / std
        return z_score
    
    @classmethod
    def get_age_group_from_age(cls, age_years: float) -> str:
        """Convert age in years to age group category"""
        if age_years < 0.0767:  # 28 days
            return 'neonate'
        elif age_years < 1:
            return 'infant'
        elif age_years < 3:
            return 'toddler'
        elif age_years < 5:
            return 'preschool'
        elif age_years < 12:
            return 'school_age'
        elif age_years < 18:
            return 'adolescent'
        elif age_years < 40:
            return 'young_adult'
        elif age_years < 65:
            return 'middle_adult'
        else:
            return 'geriatric'
