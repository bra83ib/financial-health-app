import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
import time

# Set page configuration
st.set_page_config(
    page_title="Financial Health Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .good {
        color: #4CAF50;
        font-weight: bold;
    }
    .warning {
        color: #FFC107;
        font-weight: bold;
    }
    .danger {
        color: #F44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App title and introduction
st.markdown("<h1 class='main-header'>Financial Health Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
This dashboard helps you understand your current financial health, track your progress, 
and plan for your financial goals. Enter your financial information in the sidebar to get started.
""")

# Sidebar for user inputs
st.sidebar.header("📊 Your Financial Data")

# Income section
st.sidebar.subheader("Monthly Income")
monthly_salary = st.sidebar.number_input("Monthly Salary (After Tax)", min_value=0, value=4000, step=100)
side_income = st.sidebar.number_input("Side Income / Passive Income", min_value=0, value=500, step=100)
other_income = st.sidebar.number_input("Other Income", min_value=0, value=0, step=100)

total_monthly_income = monthly_salary + side_income + other_income

# Expenses section
st.sidebar.subheader("Monthly Expenses")
housing = st.sidebar.number_input("Housing (Rent/Mortgage)", min_value=0, value=1200, step=100)
utilities = st.sidebar.number_input("Utilities", min_value=0, value=200, step=50)
groceries = st.sidebar.number_input("Groceries", min_value=0, value=400, step=50)
transportation = st.sidebar.number_input("Transportation", min_value=0, value=300, step=50)
healthcare = st.sidebar.number_input("Healthcare", min_value=0, value=100, step=50)
entertainment = st.sidebar.number_input("Entertainment", min_value=0, value=200, step=50)
other_expenses = st.sidebar.number_input("Other Expenses", min_value=0, value=200, step=50)

total_monthly_expenses = housing + utilities + groceries + transportation + healthcare + entertainment + other_expenses

# Debt section
st.sidebar.subheader("Outstanding Debts")
student_loan = st.sidebar.number_input("Student Loan", min_value=0, value=15000, step=1000)
car_loan = st.sidebar.number_input("Car Loan", min_value=0, value=10000, step=1000)
credit_card = st.sidebar.number_input("Credit Card Debt", min_value=0, value=2000, step=500)
mortgage = st.sidebar.number_input("Mortgage Remaining", min_value=0, value=200000, step=10000)
other_debt = st.sidebar.number_input("Other Debt", min_value=0, value=0, step=1000)

total_debt = student_loan + car_loan + credit_card + mortgage + other_debt

# Monthly debt payments
st.sidebar.subheader("Monthly Debt Payments")
student_loan_payment = st.sidebar.number_input("Student Loan Payment", min_value=0, value=200, step=50)
car_loan_payment = st.sidebar.number_input("Car Loan Payment", min_value=0, value=300, step=50)
credit_card_payment = st.sidebar.number_input("Credit Card Payment", min_value=0, value=200, step=50)
mortgage_payment = st.sidebar.number_input("Mortgage Payment", min_value=0, value=900, step=50)
other_debt_payment = st.sidebar.number_input("Other Debt Payment", min_value=0, value=0, step=50)

total_debt_payment = student_loan_payment + car_loan_payment + credit_card_payment + mortgage_payment + other_debt_payment

# Assets section
st.sidebar.subheader("Assets")
emergency_fund = st.sidebar.number_input("Emergency Fund", min_value=0, value=10000, step=1000)
investments = st.sidebar.number_input("Investments", min_value=0, value=50000, step=5000)
retirement = st.sidebar.number_input("Retirement Accounts", min_value=0, value=40000, step=5000)
property_value = st.sidebar.number_input("Property Value", min_value=0, value=250000, step=10000)
other_assets = st.sidebar.number_input("Other Assets", min_value=0, value=5000, step=1000)

total_assets = emergency_fund + investments + retirement + property_value + other_assets

# Financial goal setting
st.sidebar.subheader("Financial Goal Setting")
goal_options = ["Build Emergency Fund", "Pay Off Debt", "Save for Retirement", "Save for House", "Save for Education"]
selected_goal = st.sidebar.selectbox("Select your primary financial goal", goal_options)

goal_amount = st.sidebar.number_input("Goal Amount", min_value=0, value=30000, step=1000)
goal_timeline_years = st.sidebar.slider("Timeline (Years)", min_value=1, max_value=30, value=5)

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Financial Health", "Expense Breakdown", "Financial Forecast"])

with tab1:
    # Overview section
    st.markdown("<h2 class='sub-header'>Financial Overview</h2>", unsafe_allow_html=True)
    
    # Display key metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("Monthly Income")
        st.markdown(f"<h2>${total_monthly_income:,.2f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("Monthly Expenses")
        st.markdown(f"<h2>${total_monthly_expenses:,.2f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        monthly_savings = total_monthly_income - total_monthly_expenses - total_debt_payment
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("Monthly Savings")
        st.markdown(f"<h2>${monthly_savings:,.2f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Net worth calculation
    net_worth = total_assets - total_debt
    
    # Display net worth with progress bar
    st.markdown("<h3>Net Worth</h3>", unsafe_allow_html=True)
    st.progress(min(max(net_worth / (total_assets * 2), 0), 1.0))
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Assets", f"${total_assets:,.2f}", delta=None)
    with col2:
        st.metric("Total Debt", f"${total_debt:,.2f}", delta=None, delta_color="inverse")
    st.metric("Net Worth", f"${net_worth:,.2f}")
    
    # Income vs Expenses chart
    st.markdown("<h3>Income vs Expenses</h3>", unsafe_allow_html=True)
    
    categories = ['Income', 'Expenses', 'Debt Payments', 'Savings']
    values = [total_monthly_income, total_monthly_expenses, total_debt_payment, monthly_savings]
    colors = ['#4CAF50', '#FF9800', '#F44336', '#2196F3']
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors
    )])
    
    fig.update_layout(
        title="Monthly Cash Flow",
        xaxis_title="Category",
        yaxis_title="Amount ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Financial Health Metrics
    st.markdown("<h2 class='sub-header'>Financial Health Metrics</h2>", unsafe_allow_html=True)
    
    # Calculate key financial health metrics
    savings_rate = (monthly_savings / total_monthly_income) * 100 if total_monthly_income > 0 else 0
    debt_to_income = (total_debt_payment / total_monthly_income) * 100 if total_monthly_income > 0 else 0
    housing_to_income = (housing / total_monthly_income) * 100 if total_monthly_income > 0 else 0
    emergency_months = emergency_fund / total_monthly_expenses if total_monthly_expenses > 0 else 0
    debt_to_asset = (total_debt / total_assets) * 100 if total_assets > 0 else 0
    
    # Function to get health status and color
    def get_health_status(value, thresholds, categories):
        for i, threshold in enumerate(thresholds):
            if value <= threshold:
                return categories[i]
        return categories[-1]
    
    # Display metrics with health indicators
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3>Savings Rate</h3>", unsafe_allow_html=True)
        savings_status = get_health_status(savings_rate, [0, 10, 20], ["danger", "warning", "good"])
        st.markdown(f"<h2 class='{savings_status}'>{savings_rate:.1f}%</h2>", unsafe_allow_html=True)
        st.markdown("""
        <ul>
            <li>Less than 10%: <span class='danger'>Danger</span></li>
            <li>10-20%: <span class='warning'>Caution</span></li>
            <li>Over 20%: <span class='good'>Excellent</span></li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3>Debt-to-Income Ratio</h3>", unsafe_allow_html=True)
        dti_status = get_health_status(debt_to_income, [0, 28, 36], ["good", "warning", "danger"])
        st.markdown(f"<h2 class='{dti_status}'>{debt_to_income:.1f}%</h2>", unsafe_allow_html=True)
        st.markdown("""
        <ul>
            <li>Less than 28%: <span class='good'>Good</span></li>
            <li>28-36%: <span class='warning'>Caution</span></li>
            <li>Over 36%: <span class='danger'>High Risk</span></li>
        </ul>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Emergency Fund</h3>", unsafe_allow_html=True)
        emergency_status = get_health_status(emergency_months, [0, 3, 6], ["danger", "warning", "good"])
        st.markdown(f"<h2 class='{emergency_status}'>{emergency_months:.1f} months</h2>", unsafe_allow_html=True)
        st.markdown("""
        <ul>
            <li>Less than 3 months: <span class='danger'>Danger</span></li>
            <li>3-6 months: <span class='warning'>Building</span></li>
            <li>Over 6 months: <span class='good'>Secure</span></li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3>Housing Cost Ratio</h3>", unsafe_allow_html=True)
        housing_status = get_health_status(housing_to_income, [0, 25, 33], ["good", "warning", "danger"])
        st.markdown(f"<h2 class='{housing_status}'>{housing_to_income:.1f}%</h2>", unsafe_allow_html=True)
        st.markdown("""
        <ul>
            <li>Less than 25%: <span class='good'>Affordable</span></li>
            <li>25-33%: <span class='warning'>Moderate</span></li>
            <li>Over 33%: <span class='danger'>Cost Burdened</span></li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Financial Health Gauge Chart
    st.markdown("<h3>Overall Financial Health Score</h3>", unsafe_allow_html=True)
    
    # Calculate overall financial health score (0-100)
    savings_score = min(savings_rate / 30 * 25, 25)  # 25% weight
    debt_score = min(max(0, (50 - debt_to_income) / 50 * 25), 25)  # 25% weight
    emergency_score = min(emergency_months / 12 * 25, 25)  # 25% weight
    housing_score = min(max(0, (40 - housing_to_income) / 40 * 15), 15)  # 15% weight
    net_worth_score = min(max(0, net_worth / (total_monthly_income * 12 * 10) * 10), 10)  # 10% weight
    
    financial_health_score = savings_score + debt_score + emergency_score + housing_score + net_worth_score
    
    # Create gauge chart for financial health score
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = financial_health_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Financial Health Score"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "#F44336"},
                {'range': [30, 60], 'color': "#FFC107"},
                {'range': [60, 100], 'color': "#4CAF50"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': financial_health_score
            }
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial health recommendations based on scores
    st.markdown("<h3>Personalized Recommendations</h3>", unsafe_allow_html=True)
    
    recommendations = []
    
    if savings_rate < 10:
        recommendations.append("Increase your savings rate to at least 10% by cutting non-essential expenses.")
    elif savings_rate < 20:
        recommendations.append("Consider boosting your savings rate to 20% to build wealth faster.")
    
    if debt_to_income > 36:
        recommendations.append("Your debt payments are too high relative to income. Focus on paying down high-interest debt.")
    elif debt_to_income > 28:
        recommendations.append("Work on reducing your debt-to-income ratio to less than 28% for better financial health.")
    
    if emergency_months < 3:
        recommendations.append("Build your emergency fund to cover at least 3 months of expenses.")
    elif emergency_months < 6:
        recommendations.append("Continue building your emergency fund to reach a 6-month safety net.")
    
    if housing_to_income > 33:
        recommendations.append("Your housing costs are high relative to your income. Consider ways to reduce housing expenses.")
    
    if credit_card > 0:
        recommendations.append("Prioritize paying off high-interest credit card debt as quickly as possible.")
    
    if not recommendations:
        recommendations.append("Great job! Your financial health is strong. Consider increasing investments for long-term wealth.")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")

with tab3:
    # Expense Breakdown
    st.markdown("<h2 class='sub-header'>Expense Breakdown</h2>", unsafe_allow_html=True)
    
    # Create pie chart for expenses
    expense_labels = ['Housing', 'Utilities', 'Groceries', 'Transportation', 'Healthcare', 'Entertainment', 'Other Expenses', 'Debt Payments']
    expense_values = [housing, utilities, groceries, transportation, healthcare, entertainment, other_expenses, total_debt_payment]
    
    # Filter out zero values
    non_zero_labels = [label for label, value in zip(expense_labels, expense_values) if value > 0]
    non_zero_values = [value for value in expense_values if value > 0]
    
    # Create pie chart
    fig = px.pie(
        values=non_zero_values,
        names=non_zero_labels,
        title="Monthly Expenses Breakdown",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Expense comparison to 50/30/20 rule
    st.markdown("<h3>Expense Analysis: 50/30/20 Rule</h3>", unsafe_allow_html=True)
    st.markdown("""
    The 50/30/20 budgeting rule recommends:
    - 50% of income for needs (housing, groceries, utilities, etc.)
    - 30% for wants (entertainment, dining out, etc.)
    - 20% for savings and debt payment
    """)
    
    # Calculate current percentages
    needs = (housing + utilities + groceries + transportation + healthcare) / total_monthly_income * 100 if total_monthly_income > 0 else 0
    wants = entertainment / total_monthly_income * 100 if total_monthly_income > 0 else 0
    savings_debt = (monthly_savings + total_debt_payment) / total_monthly_income * 100 if total_monthly_income > 0 else 0
    
    # Display current percentages vs. ideal
    comparison_data = {
        'Category': ['Needs', 'Wants', 'Savings & Debt'],
        'Current (%)': [needs, wants, savings_debt],
        'Ideal (%)': [50, 30, 20]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Create bar chart for comparison
    fig = go.Figure(data=[
        go.Bar(name='Current', x=df_comparison['Category'], y=df_comparison['Current (%)']),
        go.Bar(name='Ideal', x=df_comparison['Category'], y=df_comparison['Ideal (%)'])
    ])
    
    fig.update_layout(
        barmode='group',
        title='Your Budget vs. 50/30/20 Rule',
        xaxis_title='Category',
        yaxis_title='Percentage of Income (%)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Budget optimization suggestions
    st.markdown("<h3>Budget Optimization Suggestions</h3>", unsafe_allow_html=True)
    
    budget_recommendations = []
    
    if needs > 50:
        budget_recommendations.append(f"Your essential expenses (needs) are {needs:.1f}% of income, which is above the recommended 50%. Consider finding ways to reduce housing, transportation, or utility costs.")
    
    if wants > 30:
        budget_recommendations.append(f"Your discretionary spending (wants) is {wants:.1f}% of income, above the recommended 30%. Try cutting back on entertainment and non-essential purchases.")
    
    if savings_debt < 20:
        budget_recommendations.append(f"You're only allocating {savings_debt:.1f}% to savings and debt repayment, below the recommended 20%. Increase this allocation to build long-term wealth.")
    
    highest_expense_category = expense_labels[expense_values.index(max(expense_values))]
    budget_recommendations.append(f"Your highest expense category is {highest_expense_category}. Look for ways to optimize this area of your budget.")
    
    for i, rec in enumerate(budget_recommendations, 1):
        st.markdown(f"{i}. {rec}")

with tab4:
    # Financial Forecast
    st.markdown("<h2 class='sub-header'>Financial Forecast</h2>", unsafe_allow_html=True)
    
    # Goal-based forecasting
    st.markdown(f"<h3>Timeline for {selected_goal}</h3>", unsafe_allow_html=True)
    
    # Basic calculations for forecast based on current savings
    annual_savings = monthly_savings * 12
    
    if annual_savings <= 0:
        st.warning("Your current savings rate is too low to achieve your goal. Please increase your monthly savings.")
    else:
        years_to_goal = goal_amount / annual_savings
        
        # Forecast data
        years = list(range(int(np.ceil(years_to_goal)) + 1))
        forecast_savings = [annual_savings * year for year in years]
        
        # Create goal line
        goal_line = [goal_amount] * len(years)
        
        # Create forecast plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=forecast_savings,
            mode='lines+markers',
            name='Projected Savings',
            line=dict(color='#2196F3', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=goal_line,
            mode='lines',
            name='Goal Amount',
            line=dict(color='#F44336', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title=f"Savings Projection for {selected_goal}",
            xaxis_title='Years',
            yaxis_title='Amount ($)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        if years_to_goal <= goal_timeline_years:
            st.success(f"Based on your current savings rate of ${monthly_savings:.2f}/month, you'll reach your goal of ${goal_amount:,.2f} in {years_to_goal:.1f} years, which is within your {goal_timeline_years} year timeline.")
        else:
            st.warning(f"Based on your current savings rate of ${monthly_savings:.2f}/month, it will take {years_to_goal:.1f} years to reach your goal of ${goal_amount:,.2f}, which exceeds your {goal_timeline_years} year timeline.")
            
            # Calculate required monthly savings to meet timeline
            required_monthly_savings = goal_amount / (goal_timeline_years * 12)
            savings_gap = required_monthly_savings - monthly_savings
            
            st.info(f"To meet your {goal_timeline_years}-year timeline, you need to save ${required_monthly_savings:.2f}/month, which is ${savings_gap:.2f} more than your current monthly savings.")
    
    # Retirement forecast (simplified)
    st.markdown("<h3>Retirement Planning</h3>", unsafe_allow_html=True)
    
    retirement_age = st.slider("Expected Retirement Age", min_value=50, max_value=75, value=65)
    current_age = st.slider("Current Age", min_value=18, max_value=70, value=30)
    expected_annual_return = st.slider("Expected Annual Return (%)", min_value=1, max_value=12, value=7) / 100
    
    years_to_retirement = retirement_age - current_age
    
    # Calculate current retirement savings and monthly contribution
    annual_retirement_contribution = monthly_savings * 0.5 * 12  # Assume 50% of savings goes to retirement
    
    # Calculate future value of current retirement savings
    future_retirement_savings = retirement * (1 + expected_annual_return) ** years_to_retirement
    
    # Calculate future value of retirement contributions
    future_value_contributions = annual_retirement_contribution * (((1 + expected_annual_return) ** years_to_retirement - 1) / expected_annual_return)
    
    total_retirement_savings = future_retirement_savings + future_value_contributions
    
    # Display retirement forecast
    st.markdown(f"Estimated retirement savings at age {retirement_age}: **${total_retirement_savings:,.2f}**")
    
    # Calculate withdrawal rate and monthly retirement income
    withdrawal_rate = 0.04  # 4% rule
    annual_retirement_income = total_retirement_savings * withdrawal_rate
    monthly_retirement_income = annual_retirement_income / 12
    
    st.markdown(f"Estimated monthly retirement income (4% withdrawal rate): **${monthly_retirement_income:,.2f}**")
    
    # Retirement income comparison
    retirement_income_ratio = monthly_retirement_income / total_monthly_income * 100 if total_monthly_income > 0 else 0
    
    st.progress(min(retirement_income_ratio / 100, 1.0))
    st.markdown(f"This retirement income would be **{retirement_income_ratio:.1f}%** of your current monthly income.")
    
    if retirement_income_ratio < 70:
        st.warning("Your projected retirement income is less than 70% of your current income. Consider increasing your retirement contributions.")
    else:
        st.success("Your projected retirement income is on track to replace a sufficient portion of your current income.")
    
    # What-if scenario for increased savings
    st.markdown("<h3>What-If Scenario: Increase Savings</h3>", unsafe_allow_html=True)
    
    additional_savings = st.slider("Additional Monthly Savings ($)", min_value=0, max_value=1000, value=200, step=50)
    
    # Calculate new total savings
    new_monthly_savings = monthly_savings + additional_savings
    new_annual_retirement_contribution = (monthly_savings + additional_savings) * 0.5 * 12
    
    # Calculate new future value of retirement contributions
    new_future_value_contributions = new_annual_retirement_contribution * (((1 + expected_annual_return) ** years_to_retirement - 1) / expected_annual_return)
    
    new_total_retirement_savings = future_retirement_savings + new_future_value_contributions
    
    # Calculate new monthly retirement income
    new_annual_retirement_income = new_total_retirement_savings * withdrawal_rate
    new_monthly_retirement_income = new_annual_retirement_income / 12
    
    # Calculate increase
    retirement_income_increase = new_monthly_retirement_income - monthly_retirement_income
    retirement_income_increase_percent = (retirement_income_increase / monthly_retirement_income) * 100 if monthly_retirement_income > 0 else 0
    
    st.markdown(f"By saving an additional **${additional_savings}/month**, your projected monthly retirement income would increase by **${retirement_income_increase:,.2f}** to **${new_monthly_retirement_income:,.2f}** (a **{retirement_income_increase_percent:.1f}%** increase).")
    
# Add footer with creator information
st.markdown("---")
st.markdown("Financial Health Dashboard | Created for AF3005 – Programming for Finance | Dr. Usama Arshad")