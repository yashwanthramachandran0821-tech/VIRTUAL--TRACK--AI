"""
Demographic Constants and Configuration
Gender and Age Group specific thresholds and norms
"""

from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import date

class Gender(str, Enum):
    """Gender enumeration"""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    

class AgeGroup(str, Enum):
    """Age group categories"""
    NEONATE = "Neonate (0-28 days)"
    INFANT = "Infant (29 days - 1 year)"
    TODDLER = "Toddler (1-3 years)"
    PRESCHOOL = "Preschool (3-5 years)"
    SCHOOL_AGE = "School Age (5-12 years)"
    ADOLESCENT = "Adolescent (12-18 years)"
    YOUNG_ADULT = "Young Adult (18-40 years)"
    MIDDLE_ADULT = "Middle Adult (40-65 years)"
    GERIATRIC = "Geriatric (>65 years)"

class AgeSubGroup(str, Enum):
    """More granular age subgroups"""
    YOUNG_GERIATRIC = "Young Geriatric (65-74)"
    MID_GERIATRIC = "Mid Geriatric (75-84)"
    OLD_GERIATRIC = "Old Geriatric (85+)"

@dataclass
class GenderSpecificNorms:
    """Gender-specific vital sign norms"""
    gender: Gender
    heart_rate_min: float
    heart_rate_max: float
    systolic_bp_min: float
    systolic_bp_max: float
    diastolic_bp_min: float
    diastolic_bp_max: float
    respiration_rate_min: float
    respiration_rate_max: float
    temperature_min: float
    temperature_max: float

@dataclass
class AgeGroupNorms:
    """Age-group specific vital sign norms"""
    age_group: AgeGroup
    heart_rate_min: float
    heart_rate_max: float
    systolic_bp_min: float
    systolic_bp_max: float
    respiration_rate_min: float
    respiration_rate_max: float
    temperature_mean: float
    temperature_std: float

class DemographicConstants:
    """Centralized demographic constants"""
    
    # Gender-specific thresholds for sepsis detection
    GENDER_SEPSIS_THRESHOLDS = {
        Gender.MALE: {
            'heart_rate_critical': 110,
            'respiratory_rate_critical': 24,
            'systolic_bp_critical': 100,
            'temperature_fever': 38.0,
        },
        Gender.FEMALE: {
            'heart_rate_critical': 115,
            'respiratory_rate_critical': 22,
            'systolic_bp_critical': 95,
            'temperature_fever': 38.2,
        },
        Gender.OTHER: {
            'heart_rate_critical': 112,
            'respiratory_rate_critical': 23,
            'systolic_bp_critical': 98,
            'temperature_fever': 38.1,
        }
    }
    
    # Age-group specific sepsis risk factors
    AGE_SEPSIS_RISK_FACTORS = {
        AgeGroup.NEONATE: {
            'immune_immature': True,
            'skin_barrier_weak': True,
            'metabolic_rate_high': True,
            'risk_multiplier': 3.5
        },
        AgeGroup.INFANT: {
            'immune_developing': True,
            'vaccination_incomplete': True,
            'risk_multiplier': 2.8
        },
        AgeGroup.GERIATRIC: {
            'immune_senescence': True,
            'comorbidities_high': True,
            'atypical_presentation': True,
            'risk_multiplier': 2.5
        },
        AgeGroup.YOUNG_ADULT: {
            'risk_multiplier': 1.0
        }
    }
    
    # Gender-specific response to infection
    GENDER_IMMUNE_RESPONSE = {
        Gender.FEMALE: {
            'immune_response': 'stronger',
            'antibody_production': 'higher',
            'inflammatory_response': 'more_robust',
            'autoimmune_risk': 'higher'
        },
        Gender.MALE: {
            'immune_response': 'moderate',
            'susceptibility': 'higher',
            'mortality_risk': 'higher',
            'testosterone_effect': 'immunosuppressive'
        }
    }
    
    # Age-based vital sign normal ranges
    AGE_VITAL_RANGES = {
        AgeGroup.NEONATE: {
            'heart_rate': (120, 160),
            'respiratory_rate': (30, 60),
            'systolic_bp': (60, 90),
            'temperature': (36.5, 37.5)
        },
        AgeGroup.INFANT: {
            'heart_rate': (80, 140),
            'respiratory_rate': (20, 40),
            'systolic_bp': (70, 100),
            'temperature': (36.6, 37.7)
        },
        AgeGroup.TODDLER: {
            'heart_rate': (70, 120),
            'respiratory_rate': (20, 30),
            'systolic_bp': (80, 110),
            'temperature': (36.7, 37.8)
        },
        AgeGroup.ADOLESCENT: {
            'heart_rate': (60, 100),
            'respiratory_rate': (12, 20),
            'systolic_bp': (90, 120),
            'temperature': (36.5, 37.5)
        },
        AgeGroup.YOUNG_ADULT: {
            'heart_rate': (60, 100),
            'respiratory_rate': (12, 20),
            'systolic_bp': (100, 130),
            'temperature': (36.5, 37.5)
        },
        AgeGroup.GERIATRIC: {
            'heart_rate': (60, 100),
            'respiratory_rate': (12, 25),
            'systolic_bp': (110, 140),
            'temperature': (36.0, 37.2)
        }
    }
    
    # Gender-specific medication metabolism
    GENDER_PHARMACOKINETICS = {
        Gender.FEMALE: {
            'drug_clearance': 'slower',
            'volume_distribution': 'smaller',
            'enzyme_activity': 'variable',
            'side_effects': 'more_frequent'
        },
        Gender.MALE: {
            'drug_clearance': 'faster',
            'volume_distribution': 'larger',
            'enzyme_activity': 'higher',
            'side_effects': 'less_frequent'
        }
    }
    
    # Population demographics for risk adjustment
    POPULATION_DEMOGRAPHICS = {
        'baseline_sepsis_incidence': {
            Gender.MALE: 2.1,  # per 1000
            Gender.FEMALE: 1.8,
            Gender.OTHER: 1.9
        },
        'mortality_rate': {
            Gender.MALE: 0.25,
            Gender.FEMALE: 0.22,
            AgeGroup.GERIATRIC: 0.35,
            AgeGroup.NEONATE: 0.20
        }
    }
    
    @classmethod
    def get_age_group(cls, age_years: int) -> AgeGroup:
        """Determine age group from age in years"""
        if age_years < 0.0767:  # 28 days
            return AgeGroup.NEONATE
        elif age_years < 1:
            return AgeGroup.INFANT
        elif age_years < 3:
            return AgeGroup.TODDLER
        elif age_years < 5:
            return AgeGroup.PRESCHOOL
        elif age_years < 12:
            return AgeGroup.SCHOOL_AGE
        elif age_years < 18:
            return AgeGroup.ADOLESCENT
        elif age_years < 40:
            return AgeGroup.YOUNG_ADULT
        elif age_years < 65:
            return AgeGroup.MIDDLE_ADULT
        else:
            return AgeGroup.GERIATRIC
    
    @classmethod
    def get_age_subgroup(cls, age_years: int) -> AgeSubGroup:
        """Get more granular age subgroup for geriatric patients"""
        if age_years >= 65:
            if age_years < 75:
                return AgeSubGroup.YOUNG_GERIATRIC
            elif age_years < 85:
                return AgeSubGroup.MID_GERIATRIC
            else:
                return AgeSubGroup.OLD_GERIATRIC
        return None
    
    @classmethod
    def get_gender_risk_adjustment(cls, gender: Gender, age_group: AgeGroup) -> float:
        """Calculate risk adjustment factor based on gender and age"""
        base_risk = 1.0
        
        # Gender adjustment
        if gender == Gender.MALE:
            base_risk *= 1.15  # Males have 15% higher risk
        elif gender == Gender.FEMALE:
            base_risk *= 0.95  # Females have 5% lower risk
        
        # Age adjustment
        age_adjustments = {
            AgeGroup.NEONATE: 2.5,
            AgeGroup.INFANT: 2.0,
            AgeGroup.GERIATRIC: 1.8,
            AgeGroup.YOUNG_ADULT: 1.0
        }
        
        age_risk = age_adjustments.get(age_group, 1.0)
        
        return base_risk * age_risk
    
    @classmethod
    def get_vital_thresholds(cls, gender: Gender, age_years: int) -> Dict:
        """Get gender and age-specific vital sign thresholds"""
        age_group = cls.get_age_group(age_years)
        gender_thresholds = cls.GENDER_SEPSIS_THRESHOLDS.get(gender, {})
        age_ranges = cls.AGE_VITAL_RANGES.get(age_group, {})
        
        return {
            'gender': gender,
            'age_group': age_group,
            'heart_rate': {
                'normal_min': age_ranges.get('heart_rate', (60, 100))[0],
                'normal_max': age_ranges.get('heart_rate', (60, 100))[1],
                'critical': gender_thresholds.get('heart_rate_critical', 110)
            },
            'respiratory_rate': {
                'normal_min': age_ranges.get('respiratory_rate', (12, 20))[0],
                'normal_max': age_ranges.get('respiratory_rate', (12, 20))[1],
                'critical': gender_thresholds.get('respiratory_rate_critical', 22)
            },
            'systolic_bp': {
                'normal_min': age_ranges.get('systolic_bp', (90, 120))[0],
                'normal_max': age_ranges.get('systolic_bp', (90, 120))[1],
                'critical': gender_thresholds.get('systolic_bp_critical', 100)
            },
            'temperature': {
                'normal_min': age_ranges.get('temperature', (36.5, 37.5))[0],
                'normal_max': age_ranges.get('temperature', (36.5, 37.5))[1],
                'fever': gender_thresholds.get('temperature_fever', 38.0)
            }
        }