# The Internet - Login, Dynamic Controls, Dynamic Loading Test Plan

## Application Overview

This test plan covers three functional areas of the-internet.herokuapp.com: (1) Form Authentication at /login, verifying successful and failed login flows with flash messaging; (2) Dynamic Controls at /dynamic_controls, verifying asynchronous checkbox removal/addition and text input enable behavior; and (3) Dynamic Loading at /dynamic_loading, verifying that hidden and not-yet-rendered "Hello World!" elements are correctly revealed after clicking Start on examples 1 and 2. All scenarios assume a fresh browser context with no prior authentication state or cookies.

## Test Scenarios

### 1. Form Authentication (/login)

**Seed:** `tests/seed.spec.ts`

#### 1.1. Successful login with valid credentials reaches secure area

**File:** `tests/form-authentication/login.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/login
    - expect: Page loads with heading 'Login Page'
    - expect: Username and Password textboxes and a Login button are visible
  2. Enter 'tomsmith' into the Username textbox
    - expect: Username field contains 'tomsmith'
  3. Enter 'SuperSecretPassword!' into the Password textbox
    - expect: Password field contains the entered value (masked)
  4. Click the Login button
    - expect: Browser navigates to /secure
    - expect: Heading 'Secure Area' is displayed
    - expect: A green success flash message containing 'You logged into a secure area!' is displayed
    - expect: A 'Logout' link is visible

#### 1.2. Login rejected with invalid credentials shows error flash message

**File:** `tests/form-authentication/login.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/login
    - expect: Page loads with heading 'Login Page'
  2. Enter 'invaliduser' into the Username textbox
    - expect: Username field contains 'invaliduser'
  3. Enter 'wrongpassword' into the Password textbox
    - expect: Password field contains the entered value (masked)
  4. Click the Login button
    - expect: Browser remains on /login (no navigation to /secure)
    - expect: A red error flash message containing 'Your username is invalid!' is displayed
    - expect: The Login form is still visible for retry

#### 1.3. Login rejected with valid username but invalid password shows error flash message

**File:** `tests/form-authentication/login.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/login
    - expect: Page loads with heading 'Login Page'
  2. Enter 'tomsmith' into the Username textbox
    - expect: Username field contains 'tomsmith'
  3. Enter an incorrect password, e.g. 'WrongPassword!', into the Password textbox
    - expect: Password field contains the entered value (masked)
  4. Click the Login button
    - expect: Browser remains on /login (no navigation to /secure)
    - expect: A red error flash message containing 'Your password is invalid!' is displayed

### 2. Dynamic Controls (/dynamic_controls)

**Seed:** `tests/seed.spec.ts`

#### 2.1. Removing and re-adding the checkbox

**File:** `tests/dynamic-controls/checkbox.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/dynamic_controls
    - expect: Page loads with heading 'Dynamic Controls'
    - expect: A checkbox labeled 'A checkbox' is visible and checked/uncheckable
    - expect: A 'Remove' button is visible
  2. Click the 'Remove' button
    - expect: The 'Remove' button becomes disabled and a 'Wait for it...' loading indicator appears briefly
  3. Wait for the 'Wait for it...' loading indicator to disappear (up to ~5 seconds)
    - expect: The checkbox element is removed from the DOM / no longer visible
    - expect: A message 'It's gone!' is displayed
    - expect: The 'Remove' button is replaced by an 'Add' button
  4. Click the 'Add' button
    - expect: A 'Wait for it...' loading indicator appears briefly
  5. Wait for the 'Wait for it...' loading indicator to disappear (up to ~5 seconds)
    - expect: The checkbox is re-added and visible on the page
    - expect: A message 'It's back!' is displayed
    - expect: The 'Add' button is replaced by a 'Remove' button

#### 2.2. Enabling the disabled text input

**File:** `tests/dynamic-controls/input.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/dynamic_controls
    - expect: A text input is visible and is disabled
    - expect: An 'Enable' button is visible
  2. Verify the text input cannot be typed into while disabled
    - expect: Attempting to fill the disabled input has no effect / input remains empty and disabled
  3. Click the 'Enable' button
    - expect: A 'Wait for it...' loading indicator appears briefly
  4. Wait for the 'Wait for it...' loading indicator to disappear (up to ~5 seconds)
    - expect: The text input becomes enabled (no longer disabled)
    - expect: A message 'It's enabled!' is displayed
    - expect: The 'Enable' button is replaced by a 'Disable' button
  5. Type sample text, e.g. 'test input', into the now-enabled text input
    - expect: The text input accepts and displays the typed value

### 3. Dynamic Loading (/dynamic_loading)

**Seed:** `tests/seed.spec.ts`

#### 3.1. Example 1: Hidden element is revealed after Start is clicked

**File:** `tests/dynamic-loading/example-1.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/dynamic_loading/1
    - expect: Page loads with heading 'Dynamically Loaded Page Elements' and sub-heading 'Example 1: Element on page that is hidden'
    - expect: A 'Start' button is visible
    - expect: The 'Hello World!' text is not visible/present on the page (element is hidden via CSS)
  2. Click the 'Start' button
    - expect: A 'Loading...' indicator is displayed while the element is being revealed
  3. Wait for the 'Loading...' indicator to disappear (up to ~5 seconds)
    - expect: The 'Loading...' indicator is no longer visible
    - expect: The text 'Hello World!' becomes visible on the page

#### 3.2. Example 2: Element rendered after fetch appears after Start is clicked

**File:** `tests/dynamic-loading/example-2.spec.ts`

**Steps:**
  1. Navigate to https://the-internet.herokuapp.com/dynamic_loading/2
    - expect: Page loads with heading 'Dynamically Loaded Page Elements' and sub-heading 'Example 2: Element rendered after the fact'
    - expect: A 'Start' button is visible
    - expect: The 'Hello World!' element does not exist in the DOM at all (not merely hidden)
  2. Click the 'Start' button
    - expect: A 'Loading...' indicator is displayed while the element is being fetched/rendered
  3. Wait for the 'Loading...' indicator to disappear (up to ~5 seconds)
    - expect: The 'Loading...' indicator is no longer visible
    - expect: The text 'Hello World!' element is now rendered into the DOM and visible on the page
