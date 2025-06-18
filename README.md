## Weekly Individual Assignment 08

Vinka Alrezky As - 2206820200

A Django web application implementing a complete transportation ticket booking system with user authentication, ticket management, payment processing, and real-time seat availability checking. The application features a responsive design, secure payment handling, and proper database transaction management.

<details>
<summary>Click to expand</summary>

### Features Implemented:
1. **Ticket Management System**
   - Users can view their booked tickets in a list view
   - Each ticket shows detailed information including:
     - Ticket number
     - Route details (origin, destination)
     - Departure date and time
     - Seat number
     - Price
     - Payment status

2. **Payment Integration**
   - Users can proceed to payment for pending tickets
   - Payment information is stored and linked to tickets
   - Payment status is updated after successful transaction
   - Users can view payment details including:
     - Payment number
     - Amount
     - Payment method
     - Payment date
     - Payment status

3. **User Experience Improvements**
   - Responsive navigation bar with user-specific options
   - Clear status indicators for tickets and payments
   - Intuitive flow from ticket booking to payment
   - Proper handling of pending tickets
   - Consistent styling across all pages

4. **Database Transaction Management**
   - Implementation of Django's atomic transactions
   - Ensures data consistency during ticket booking and payment
   - Proper handling of ticket status updates
   - Prevention of duplicate bookings

### Technical Implementation:
- Used Django's `LoginRequiredMixin` for authentication
- Implemented `ListView` and `DetailView` for ticket management
- Utilized Django's session management for payment flow
- Implemented proper error handling and user feedback
- Used Bootstrap for responsive design and consistent styling

### Security Features:
- User authentication required for all sensitive operations
- Proper session management for payment process
- Prevention of unauthorized access to tickets
- Secure handling of payment information

### Database Setup and Fixtures:
1. **Initial Data Setup**
   - Routes data is loaded from fixtures
   - Includes predefined routes with:
     - Origin and destination
     - Distance
     - Base price
     - Available times

2. **Loading Fixtures**
   ```bash
   # Load routes data
   python manage.py loaddata routes.json
   ```

</details>

## Weekly Individual Assignment 07

<details>
<summary>Click to expand</summary>

### Test Credentials

#### Admin Account
- Username: vinkakniv
- Password: V!nk@A1rezky_2025#Dj4ng0

#### Regular User Account
- Username: jasmine.mooney
- Password: J@sm1n3!M00n3y#2025$

## Features

### Django Admin Implementation
- Configured Django Admin for user and data management.
- Admin access restricted to authorized users.

### Authentication and Authorization
- Login page with username and password authentication.
- Logout functionality.
- Two user roles:
  - **Regular User** (cannot access Django Admin)
  - **Admin User** (can access Django Admin)
- Uses Django's built-in authentication system.

### Database Implementation (SQLite Recommended)
- Stores user authentication and authorization data.
- Implements database migrations to ensure consistency.

### CSRF Protection
- CSRF token added to all user-submitted forms.
- Protects against Cross-Site Request Forgery attacks.

</details>

---

## Weekly Individual Assignment 06

<details>
<summary>Click to expand</summary>

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
pip install -r requirements.txt
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

</details>

