# Weekly Individual Assignment 06

Vinka Alrezky As - 2206820200

A simple Django web app that validates form inputs and instantly shows errors and feedback.

## Features

### Form Fields
- Username and Email (Django's built-in User model)
- Password with confirmation (Django's UserCreationForm)
- Phone Number
  - Must start with country code
  - Length: 8-15 digits
  - Format: +[country code][number]
- Birth Date
  - Selectable date with dropdown menus
  - Minimum age validation: 12 years old
  - Year range: 1900-2025
- Blog URL
  - Must be a valid URL format
- Description
  - Minimum length: 5 characters
  - Maximum length: 1000 characters
- Chassis Number
  - Must be 15 characters
  - Format: 5 letters followed by 10 alphanumeric characters
- SIM Number
  - Must be 16 digits
  - Numbers only

### Validation Features
- Real-time error display
- Form reset after successful submission
- Submitted data display in a separate panel
- All fields are required
- Custom validation messages

## Setup and Installation

1. Clone the repository
```bash
git clone https://gitlab.cs.ui.ac.id/vinka.alrezky/pkpl-individu-2206820200-vinka-alrezky-as.git
```
```bash
cd <<project_folder>>
```

2. Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

3. Install dependencies
```bash
pip install requirements.txt
```

4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server
```bash
python manage.py runserver
```

6. Access the application at `http://localhost:8000`



## Form Validation Rules

### Phone Number
- Must start with country code (+XX)
- Total length: 8-15 digits
- Example: +628123456789

### Birth Date
- Three dropdown menus (day, month, year)
- Must be at least 12 years old
- Year range: 1900-2025

### Chassis Number
- Exactly 15 characters
- First 5 characters must be capital letters
- Remaining 10 characters can be letters or numbers
- Example: ABCDE1234567890

### SIM Number
- Exactly 16 digits
- Numbers only
- Example: 1234567890123456




