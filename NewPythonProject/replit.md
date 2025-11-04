# Password Strength Checker

## Overview

A fully-featured Streamlit web application that analyzes password strength through multiple metrics including entropy calculation, crack time estimation, breach database checking, and detailed criteria analysis. The tool provides an intuitive interface for users to check password strength, generate secure passwords, compare multiple passwords, and export detailed strength reports.

**Status**: Production-ready web application
**Last Updated**: 2025-11-04

## User Preferences

- Preferred communication style: Simple, everyday language
- Application purpose: Web-based tool for public use via shareable link

## Features Implemented

### Core Password Analysis
✅ **Real-time Strength Checker**
- Comprehensive password analysis with 0-100 scoring system
- Visual strength indicators: 🔴 Weak (0-49), 🟡 Medium (50-74), 🟢 Strong (75+)
- Color-coded feedback with progress bar visualization
- Password visibility toggle for user convenience

✅ **Detailed Criteria Analysis**
- Length validation (8+ good, 12+ excellent)
- Character type detection (lowercase, uppercase, digits, special characters)
- Common pattern detection (123, abc, password, qwerty)
- Repeated character analysis
- Individual criterion feedback with ✓/✗ indicators

✅ **Security Metrics**
- Shannon entropy calculation in bits
- Estimated crack time (seconds to millions of years)
- Breach database check against 25+ common compromised passwords
- Assumptions: 1 billion guesses/second for modern GPU attacks

### Advanced Features
✅ **Password Generator**
- Cryptographically secure random generation using `secrets` module
- Customizable length (8-32 characters)
- Toggle character types: uppercase, lowercase, digits, special characters
- Automatic strength analysis of generated passwords

✅ **Password Comparison Tool**
- Side-by-side comparison of 2-5 passwords
- Tabular display using pandas DataFrame
- Comparative metrics: strength, score, entropy, crack time
- Automatic identification of strongest password

✅ **Export Functionality**
- Detailed text-based strength reports
- Timestamped report generation
- Downloadable .txt format
- Includes: rating, metrics, criteria checklist, feedback, and recommendations

## System Architecture

### Frontend Architecture
**Framework**: Streamlit 
- **Port**: 5000 (configured for Replit deployment)
- **Layout**: Centered, single-page with tabbed interface
- **Tabs**: Check Password | Generate Password | Compare Passwords | Export Report
- **Page Icon**: 🔒 (lock emoji for security branding)

### Core Algorithm Design

**Password Strength Scoring (0-100 scale)**
```
Length:     +15 (8-11 chars) or +25 (12+ chars)
Lowercase:  +10
Uppercase:  +10
Numbers:    +10
Special:    +15
No common:  +10
No repeat:  +10
Penalties:  -10 (common patterns), -5 (repetition)
```

**Entropy Calculation**
- Character set detection: lowercase(26), uppercase(26), digits(10), punctuation(32), extended ASCII(100)
- Formula: `entropy = password_length × log₂(charset_size)`
- Used for crack time estimation

**Crack Time Estimation**
- Assumption: 1 billion guesses per second (realistic for GPU-based attacks)
- Formula: `time = 2^entropy / (2 × guesses_per_second)` (average case at 50% search space)
- Display granularity: seconds → minutes → hours → days → months → years → thousands of years → millions of years

**Breach Database**
- Local heuristic check against 25 common breached passwords
- Immediate warning display for matched passwords
- Future enhancement opportunity: Integration with Have I Been Pwned API

### File Structure

```
.
├── app.py                    # Main Streamlit application (all features)
├── .streamlit/
│   └── config.toml          # Server configuration (port 5000, headless mode)
└── replit.md                # Project documentation (this file)
```

## External Dependencies

### Python Libraries
**Streamlit** (`streamlit`)
- Purpose: Web application framework for UI rendering and interactivity
- Usage: Page configuration, tabs, inputs, metrics, downloads

**Pandas** (`pandas`)
- Purpose: Data manipulation and display
- Usage: Password comparison table formatting

**Standard Library**:
- `re`: Regular expression for pattern detection
- `string`: Character set constants (punctuation, ascii)
- `secrets`: Cryptographically secure random generation
- `math`: Logarithmic calculations for entropy
- `datetime`: Timestamp generation for reports

## Security Considerations

✅ **Privacy Protection**
- All password analysis performed client-side (local processing)
- No password storage or transmission to external servers
- No logging of user passwords
- Clear user notification: "Your password is analyzed locally and never stored or transmitted"

✅ **Secure Password Generation**
- Uses `secrets.choice()` for cryptographically secure randomness
- Avoids predictable `random` module

⚠️ **Breach Check Limitations**
- Current: Local heuristic with 25 common passwords
- Recommended enhancement: Integration with Have I Been Pwned API for comprehensive breach checking

## Deployment Considerations

**Platform**: Replit
**Runtime**: Python 3.11
**Port**: 5000 (configured via .streamlit/config.toml)
**Database**: Not required (stateless application)
**External APIs**: None (self-contained)

**Publishing**: Ready for deployment via Replit's publish feature to generate shareable link

## Testing Status

✅ **Automated E2E Tests Passed** (2025-11-04)
- Weak password detection (abc123 → Weak, score 20)
- Strong password validation (MyStr0ng!P@ssw0rd2024 → Strong, score 90)
- Password visibility toggle
- Password generation with customizable options
- Multi-password comparison (2 passwords tested)
- Report export functionality
- All UI elements and navigation verified

**Known Non-Critical Issues**:
- Type checker warnings for None subscriptability (false positives - runtime checks in place)
- Minor deprecation warning for `use_container_width` parameter (non-blocking)

## Future Enhancement Opportunities

Based on architect review:
1. **Enhanced Breach Checking**: Integrate Have I Been Pwned API for real-time breach database queries
2. **Improved Password Visibility**: Enhance "Show password" control to dynamically toggle input field type
3. **Extended Test Coverage**: Add edge case tests for Unicode-heavy passwords and generator toggle combinations
4. **Advanced Pattern Detection**: Expand common pattern recognition (keyboard walks, date formats, names)
5. **Password History**: Optional session-based history for comparison purposes (with user consent)
