select
    budget_actual_id,
    fiscal_year,
    school_id,
    revenue_budget,
    revenue_actual,
    expense_budget,
    expense_actual
from {{ source('raw', 'budget_actuals') }}