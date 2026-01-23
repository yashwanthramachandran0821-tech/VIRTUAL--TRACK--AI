import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class DemographicAnalytics {
    public static void main(String[] args) {
        initializeDemographicAnalytics();
    }
class DemographicAnalytics {
    constructor() {
        this.overviewData = null;
        this.genderAnalysis = null;
        this.ageGroupAnalysis = null;
        this.riskStratification = null;
        this.demographicInsights = null;
        this.populationNorms = null;
    }
}

new DemographicAnalytics();
document.addEventListener('DOMContentLoaded', function() {
    initializeDemographicAnalytics();
});

async function initializeDemographicAnalytics() {
    try {
        // Load overview data
        await loadOverviewData();
        
        // Load gender analysis
        await loadGenderAnalysis();
        
        // Load age group analysis
        await loadAgeGroupAnalysis();
        
        // Load risk stratification
        await loadRiskStratification();
        
        // Load demographic insights
        await loadDemographicInsights();
        
        // Load population norms
        await loadPopulationNorms();
        
        // Set up periodic updates
        setInterval(updateDemographicData, 300000); // Update every 5 minutes
        
    } catch (error) {
        console.error('Error initializing demographic analytics:', error);
        showError('Failed to load demographic analytics');
    }
}

async function loadOverviewData() {
    try {
        const response = await fetch('/api/demographic/dashboard');
        const data = await response.json();
        
        if (data.summary) {
            document.getElementById('total-patients').textContent = 
                data.summary.total_patients.toLocaleString();
            
            // Calculate average age
            const ageGroups = Object.keys(data.summary.age_group_distribution || {});
            let totalAge = 0;
            let count = 0;
            
            // Simplified average age calculation
            ageGroups.forEach(group => {
                const groupCount = data.summary.age_group_distribution[group];
                // Approximate age from group
                const avgAge = estimateAverageAge(group);
                totalAge += avgAge * groupCount;
                count += groupCount;
            });
            
            const averageAge = count > 0 ? Math.round(totalAge / count) : 0;
            document.getElementById('average-age').textContent = `${averageAge} years`;
            
            // Gender distribution
            const genderDist = data.summary.gender_distribution || {};
            document.getElementById('gender-distribution').textContent = 
                `M:${genderDist.male || 0} F:${genderDist.female || 0} O:${genderDist.other || 0}`;
        }
        
    } catch (error) {
        console.error('Error loading overview data:', error);
    }
}

function estimateAverageAge(ageGroup) {
    // Estimate average age from age group label
    const estimates = {
        'Neonate (0-28 days)': 0.04, // ~14 days
        'Infant (29 days - 1 year)': 0.5,
        'Toddler (1-3 years)': 2,
        'Preschool (3-5 years)': 4,
        'School Age (5-12 years)': 8,
        'Adolescent (12-18 years)': 15,
        'Young Adult (18-40 years)': 29,
        'Middle Adult (40-65 years)': 52,
        'Geriatric (>65 years)': 75
    };
    
    return estimates[ageGroup] || 40;
}

async function loadGenderAnalysis() {
    try {
        // Load gender comparison data
        const response = await fetch('/api/demographic/analysis?analysis_type=gender_comparison');
        const data = await response.json();
        
        // Create gender comparison chart
        createGenderComparisonChart(data);
        
        // Create gender risk chart
        createGenderRiskChart(data);
        
    } catch (error) {
        console.error('Error loading gender analysis:', error);
    }
}

function createGenderComparisonChart(data) {
    if (!data.gender_comparisons) return;
    
    const metrics = Object.keys(data.gender_comparisons);
    const maleValues = [];
    const femaleValues = [];
    const pValues = [];
    
    metrics.forEach(metric => {
        const comparison = data.gender_comparisons[metric];
        maleValues.push(comparison.male_mean);
        femaleValues.push(comparison.female_mean);
        pValues.push(comparison.p_value);
    });
    
    const trace1 = {
        x: metrics,
        y: maleValues,
        name: 'Male',
        type: 'bar',
        marker: {
            color: '#3498db'
        }
    };
    
    const trace2 = {
        x: metrics,
        y: femaleValues,
        name: 'Female',
        type: 'bar',
        marker: {
            color: '#e74c3c'
        }
    };
    
    const layout = {
        title: 'Vital Sign Comparison by Gender',
        xaxis: {
            title: 'Vital Signs'
        },
        yaxis: {
            title: 'Mean Value'
        },
        barmode: 'group',
        showlegend: true,
        legend: {
            x: 0,
            y: 1.2
        }
    };
    
    Plotly.newPlot('gender-comparison-chart', [trace1, trace2], layout);
}

function createGenderRiskChart(data) {
    // This would use actual risk data
    // For now, create a sample chart
    
    const genders = ['Male', 'Female', 'Other'];
    const riskScores = [0.35, 0.28, 0.31];
    
    const trace = {
        x: genders,
        y: riskScores,
        type: 'bar',
        marker: {
            color: ['#3498db', '#e74c3c', '#9b59b6']
        }
    };
    
    const layout = {
        title: 'Average Sepsis Risk by Gender',
        xaxis: {
            title: 'Gender'
        },
        yaxis: {
            title: 'Risk Score',
            range: [0, 1]
        }
    };
    
    Plotly.newPlot('gender-risk-chart', [trace], layout);
}

async function loadAgeGroupAnalysis() {
    try {
        const response = await fetch('/api/demographic/analysis?analysis_type=age_group_trends');
        const data = await response.json();
        
        // Create age distribution chart
        createAgeDistributionChart(data);
        
        // Create age risk chart
        createAgeRiskChart(data);
        
    } catch (error) {
        console.error('Error loading age group analysis:', error);
    }
}

function createAgeDistributionChart(data) {
    if (!data.age_group_counts) return;
    
    const ageGroups = Object.keys(data.age_group_counts);
    const counts = Object.values(data.age_group_counts);
    
    // Define colors for age groups
    const ageGroupColors = {
        'Neonate (0-28 days)': '#9b59b6',
        'Infant (29 days - 1 year)': '#1abc9c',
        'Toddler (1-3 years)': '#2ecc71',
        'Preschool (3-5 years)': '#3498db',
        'School Age (5-12 years)': '#2980b9',
        'Adolescent (12-18 years)': '#e74c3c',
        'Young Adult (18-40 years)': '#e67e22',
        'Middle Adult (40-65 years)': '#d35400',
        'Geriatric (>65 years)': '#c0392b'
    };
    
    const colors = ageGroups.map(group => ageGroupColors[group] || '#95a5a6');
    
    const trace = {
        labels: ageGroups,
        values: counts,
        type: 'pie',
        marker: {
            colors: colors
        },
        textinfo: 'label+percent',
        hoverinfo: 'label+value+percent'
    };
    
    const layout = {
        title: 'Patient Distribution by Age Group',
        showlegend: true,
        legend: {
            x: 1,
            y: 0.5
        }
    };
    
    Plotly.newPlot('age-distribution-chart', [trace], layout);
}

function createAgeRiskChart(data) {
    if (!data.age_group_means || !data.age_group_means.heart_rate) return;
    
    const ageGroups = Object.keys(data.age_group_means.heart_rate);
    const heartRates = ageGroups.map(group => 
        data.age_group_means.heart_rate[group].mean
    );
    
    const trace = {
        x: ageGroups,
        y: heartRates,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Heart Rate',
        line: {
            color: '#e74c3c',
            width: 3
        },
        marker: {
            size: 8
        }
    };
    
    const layout = {
        title: 'Heart Rate Trends Across Age Groups',
        xaxis: {
            title: 'Age Group',
            tickangle: -45
        },
        yaxis: {
            title: 'Mean Heart Rate (bpm)'
        }
    };
    
    Plotly.newPlot('age-risk-chart', [trace], layout);
}

async function loadRiskStratification() {
    try {
        const response = await fetch('/api/demographic/analysis?analysis_type=population_risk');
        const data = await response.json();
        
        populateRiskLists(data);
        
    } catch (error) {
        console.error('Error loading risk stratification:', error);
    }
}

function populateRiskLists(data) {
    const highRiskList = document.getElementById('high-risk-list');
    const mediumRiskList = document.getElementById('medium-risk-list');
    const lowRiskList = document.getElementById('low-risk-list');
    
    // Clear existing content
    highRiskList.innerHTML = '';
    mediumRiskList.innerHTML = '';
    lowRiskList.innerHTML = '';
    
    if (!data.high_risk_demographics) return;
    
    data.high_risk_demographics.forEach(group => {
        const item = document.createElement('div');
        item.className = 'risk-item risk-high';
        item.innerHTML = `
            <div class="risk-demographic">${group.demographic}</div>
            <div class="risk-value">${group.mean_risk.toFixed(2)}</div>
        `;
        highRiskList.appendChild(item);
    });
    
    // Add sample medium risk items
    const mediumRiskItems = [
        { demographic: 'Female, Young Adult', risk: 0.42 },
        { demographic: 'Male, Middle Adult', risk: 0.38 }
    ];
    
    mediumRiskItems.forEach(item => {
        const element = document.createElement('div');
        element.className = 'risk-item risk-medium';
        element.innerHTML = `
            <div class="risk-demographic">${item.demographic}</div>
            <div class="risk-value">${item.risk.toFixed(2)}</div>
        `;
        mediumRiskList.appendChild(element);
    });
    
    // Add sample low risk items
    const lowRiskItems = [
        { demographic: 'Female, Adolescent', risk: 0.18 },
        { demographic: 'Male, School Age', risk: 0.15 }
    ];
    
    lowRiskItems.forEach(item => {
        const element = document.createElement('div');
        element.className = 'risk-item risk-low';
        element.innerHTML = `
            <div class="risk-demographic">${item.demographic}</div>
            <div class="risk-value">${item.risk.toFixed(2)}</div>
        `;
        lowRiskList.appendChild(element);
    });
}

async function loadDemographicInsights() {
    try {
        // Load insights for different demographic groups
        const femaleInsights = [
            'Higher autoimmune disease prevalence may complicate diagnosis',
            'Consider pregnancy status in women of childbearing age',
            'Gynecological sources should be considered in sepsis workup',
            'May present with more robust inflammatory response'
        ];
        
        const maleInsights = [
            'Higher baseline mortality risk from sepsis',
            'Consider prostate/urinary sources in older males',
            'May have delayed presentation to healthcare',
            'Higher risk of community-acquired pneumonia'
        ];
        
        const geriatricInsights = [
            'Atypical presentation common - watch for delirium or functional decline',
            'Lower fever threshold (≥37.8°C may be significant)',
            'Multiple comorbidities can mask sepsis symptoms',
            'Higher risk of healthcare-associated infections'
        ];
        
        const pediatricInsights = [
            'Rapid deterioration possible in neonates and infants',
            'Non-specific symptoms: poor feeding, lethargy, irritability',
            'Higher heart rate and respiratory rate baselines',
            'Consider maternal risk factors for early-onset sepsis'
        ];
        
        populateInsightList('female-insights', femaleInsights);
        populateInsightList('male-insights', maleInsights);
        populateInsightList('geriatric-insights', geriatricInsights);
        populateInsightList('pediatric-insights', pediatricInsights);
        
    } catch (error) {
        console.error('Error loading demographic insights:', error);
    }
}

function populateInsightList(listId, insights) {
    const list = document.getElementById(listId);
    if (!list) return;
    
    list.innerHTML = '';
    
    insights.forEach(insight => {
        const li = document.createElement('li');
        li.textContent = insight;
        list.appendChild(li);
    });
}

async function loadPopulationNorms() {
    try {
        // Load norms for different age groups
        const ageGroups = [
            'Neonate',
            'Infant',
            'Toddler',
            'Preschool',
            'School Age',
            'Adolescent',
            'Young Adult',
            'Middle Adult',
            'Geriatric'
        ];
        
        const tableBody = document.querySelector('#population-norms-table tbody');
        tableBody.innerHTML = '';
        
        // Sample data - in real app, this would come from API
        const sampleNorms = {
            'Neonate': { hr: '120-160', bp: '60-90', rr: '30-60', temp: '36.5-37.5', risk: '2.5' },
            'Infant': { hr: '80-140', bp: '70-100', rr: '20-40', temp: '36.6-37.7', risk: '1.8' },
            'Toddler': { hr: '70-120', bp: '80-110', rr: '20-30', temp: '36.7-37.8', risk: '1.2' },
            'Preschool': { hr: '65-110', bp: '85-115', rr: '20-30', temp: '36.5-37.5', risk: '0.9' },
            'School Age': { hr: '60-100', bp: '90-120', rr: '15-25', temp: '36.5-37.5', risk: '0.8' },
            'Adolescent': { hr: '55-95', bp: '95-125', rr: '12-20', temp: '36.5-37.5', risk: '0.6' },
            'Young Adult': { hr: '60-100', bp: '105-130', rr: '12-20', temp: '36.5-37.5', risk: '0.9' },
            'Middle Adult': { hr: '60-100', bp: '110-135', rr: '12-20', temp: '36.5-37.5', risk: '1.2' },
            'Geriatric': { hr: '60-100', bp: '115-140', rr: '12-25', temp: '36.0-37.2', risk: '5.4' }
        };
        
        ageGroups.forEach(group => {
            const norms = sampleNorms[group] || {};
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td><span class="age-group-badge badge-${getAgeGroupClass(group)}">${group}</span></td>
                <td>${norms.hr || 'N/A'}</td>
                <td>${norms.bp || 'N/A'}</td>
                <td>${norms.rr || 'N/A'}</td>
                <td>${norms.temp || 'N/A'}</td>
                <td>${norms.risk || 'N/A'}</td>
            `;
            
            tableBody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading population norms:', error);
    }
}

function getAgeGroupClass(ageGroup) {
    const classes = {
        'Neonate': 'neonate',
        'Infant': 'pediatric',
        'Toddler': 'pediatric',
        'Preschool': 'pediatric',
        'School Age': 'pediatric',
        'Adolescent': 'adult',
        'Young Adult': 'adult',
        'Middle Adult': 'adult',
        'Geriatric': 'geriatric'
    };
    
    return classes[ageGroup] || 'adult';
}

async function updateDemographicData() {
    console.log('Updating demographic data...');
    
    try {
        await loadOverviewData();
        await loadGenderAnalysis();
        await loadAgeGroupAnalysis();
        
        showNotification('Demographic data updated', 'success');
        
    } catch (error) {
        console.error('Error updating demographic data:', error);
    }
}

function showError(message) {
    // Simple error notification
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'warning': return 'exclamation-triangle';
        case 'error': return 'times-circle';
        default: return 'info-circle';
    }
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeDemographicAnalytics,
        loadOverviewData,
        loadGenderAnalysis,
        loadAgeGroupAnalysis
    };

}
