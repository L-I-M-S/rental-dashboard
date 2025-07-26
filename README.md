# Rental Property Management Dashboard

A Django-based web application for tracking rent payments and expenses, with integration for Excel and QuickBooks.

## Features
- **Rent Tracking**: Record and view rent payments with due dates and payment status.
- **Expense Reporting**: Sync financial data from QuickBooks for expense tracking.
- **Excel Integration**: Upload tenant and payment data via Excel files.
- **Visualization**: Display rent collection trends with charts.

## Setup Instructions
1. Clone the repository: `https://github.com/your-username/rental-property-management-dashboard.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure QuickBooks API:
   - Sign up at [QuickBooks Developer Portal](https://developer.intuit.com).
   - Create an app to get Client ID and Client Secret.
   - Update `rental_dashboard/settings.py` with `QB_CLIENT_ID`, `QB_CLIENT_SECRET`, and `QB_REDIRECT_URI`.
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`
6. Access the app at `http://localhost:8000/dashboard/`

## Excel File Format
Excel files for upload should have the following columns:
- `Property`: Name of the property (e.g., "Apartment A")
- `Address`: Property address (optional)
- `Tenant`: Tenant name
- `Amount`: Rent amount (e.g., 1000.00)
- `Due Date`: Due date (e.g., 2025-07-01)
- `Payment Date`: Payment date (optional, e.g., 2025-07-05)

## Deployment
For production, deploy on a platform like Heroku or Render:
1. Set up a production database (e.g., PostgreSQL).
2. Update `QB_REDIRECT_URI` in `settings.py` for your domain.
3. Configure environment variables for `SECRET_KEY`, `QB_CLIENT_ID`, and `QB_CLIENT_SECRET`.

## Dependencies
- Django 4.2.16
- python-quickbooks 0.9.3
- pandas 2.2.3
- django-chartjs 2.4.0
- intuit-oauth 1.2.3
