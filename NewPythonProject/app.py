import streamlit as st
import re
import string
import secrets
import math
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Password Strength Checker",
    page_icon="🔒",
    layout="centered"
)

def calculate_entropy(password):
    """Calculate password entropy in bits"""
    charset_size = 0
    
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32
    if any(ord(c) > 127 for c in password):
        charset_size += 100
    
    if charset_size == 0:
        return 0
    
    entropy = len(password) * math.log2(charset_size)
    return entropy

def estimate_crack_time(entropy):
    """Estimate time to crack password based on entropy"""
    # Assuming 1 billion guesses per second
    guesses_per_second = 1e9
    total_combinations = 2 ** entropy
    seconds = total_combinations / (2 * guesses_per_second)
    
    if seconds < 1:
        return "Less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 2592000:
        return f"{int(seconds/86400)} days"
    elif seconds < 31536000:
        return f"{int(seconds/2592000)} months"
    else:
        years = int(seconds/31536000)
        if years > 1000000:
            return "Millions of years"
        elif years > 1000:
            return f"{int(years/1000)}k+ years"
        else:
            return f"{years} years"

def check_password_strength(password):
    """Analyze password and return strength score and feedback"""
    if not password:
        return None
    
    score = 0
    feedback = []
    criteria = {}
    
    # Length check
    length = len(password)
    criteria['length'] = length >= 8
    if length >= 12:
        score += 25
        feedback.append("✓ Excellent length (12+ characters)")
    elif length >= 8:
        score += 15
        feedback.append("✓ Good length (8+ characters)")
    else:
        feedback.append("✗ Too short (minimum 8 characters recommended)")
    
    # Lowercase check
    has_lower = any(c.islower() for c in password)
    criteria['lowercase'] = has_lower
    if has_lower:
        score += 10
        feedback.append("✓ Contains lowercase letters")
    else:
        feedback.append("✗ Missing lowercase letters")
    
    # Uppercase check
    has_upper = any(c.isupper() for c in password)
    criteria['uppercase'] = has_upper
    if has_upper:
        score += 10
        feedback.append("✓ Contains uppercase letters")
    else:
        feedback.append("✗ Missing uppercase letters")
    
    # Numbers check
    has_digit = any(c.isdigit() for c in password)
    criteria['numbers'] = has_digit
    if has_digit:
        score += 10
        feedback.append("✓ Contains numbers")
    else:
        feedback.append("✗ Missing numbers")
    
    # Special characters check
    has_special = any(c in string.punctuation for c in password)
    criteria['special'] = has_special
    if has_special:
        score += 15
        feedback.append("✓ Contains special characters")
    else:
        feedback.append("✗ Missing special characters")
    
    # Common patterns check
    common_patterns = ['123', 'abc', 'password', 'qwerty', '111', '000']
    has_common = any(pattern in password.lower() for pattern in common_patterns)
    if has_common:
        score -= 10
        feedback.append("⚠ Contains common patterns (avoid sequences like '123', 'abc', 'password')")
    else:
        score += 10
        feedback.append("✓ No common patterns detected")
    
    # Repeated characters check
    if re.search(r'(.)\1{2,}', password):
        score -= 5
        feedback.append("⚠ Contains repeated characters")
    else:
        score += 10
        feedback.append("✓ No excessive character repetition")
    
    # Calculate entropy
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)
    
    # Determine strength level
    if score >= 75:
        strength = "Strong"
        color = "green"
        emoji = "🟢"
    elif score >= 50:
        strength = "Medium"
        color = "orange"
        emoji = "🟡"
    else:
        strength = "Weak"
        color = "red"
        emoji = "🔴"
    
    return {
        'score': max(0, min(100, score)),
        'strength': strength,
        'color': color,
        'emoji': emoji,
        'feedback': feedback,
        'criteria': criteria,
        'entropy': entropy,
        'crack_time': crack_time
    }

def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    """Generate a secure random password"""
    charset = ''
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_special:
        charset += string.punctuation
    
    if not charset:
        return None
    
    password = ''.join(secrets.choice(charset) for _ in range(length))
    return password

def check_common_breach(password):
    """Check if password contains common breached patterns"""
    # List of very common breached passwords
    common_breached = [
        'password', '123456', '12345678', 'qwerty', 'abc123', 
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321',
        'superman', 'qazwsx', 'michael', 'football', 'password1'
    ]
    
    return password.lower() in common_breached

# Title and description
st.title("🔒 Password Strength Checker")
st.markdown("Check how strong your password is and get recommendations to improve it.")
st.markdown("---")

# Create tabs for different features
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Check Password", "🔑 Generate Password", "⚖️ Compare Passwords", "📊 Export Report"])

with tab1:
    st.subheader("Password Strength Analysis")
    
    # Password input
    password = st.text_input(
        "Enter your password",
        type="password",
        placeholder="Type your password here...",
        help="Your password is not stored or transmitted anywhere",
        key="password_check"
    )
    
    # Show/hide password toggle
    show_password = st.checkbox("Show password", key="show_check")
    if show_password and password:
        st.code(password)
    
    # Analyze password
    if password:
        result = check_password_strength(password)
        
        # Display strength indicator
        st.markdown("### Strength Rating")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"## {result['emoji']} {result['strength']}")
            st.progress(result['score'] / 100)
            st.caption(f"Score: {result['score']}/100")
        
        # Entropy and crack time
        st.markdown("### Security Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Entropy", f"{result['entropy']:.1f} bits")
        with col2:
            st.metric("Estimated Crack Time", result['crack_time'])
        
        # Breach check
        if check_common_breach(password):
            st.error("⚠️ **WARNING**: This password appears in common breach databases! Do not use this password.")
        
        # Detailed feedback
        st.markdown("### Detailed Analysis")
        for item in result['feedback']:
            if item.startswith('✓'):
                st.success(item)
            elif item.startswith('✗'):
                st.error(item)
            else:
                st.warning(item)
        
        # Security tips
        st.markdown("### 💡 Security Tips")
        st.info("""
        **Best Practices for Strong Passwords:**
        - Use at least 12 characters (longer is better)
        - Mix uppercase and lowercase letters
        - Include numbers and special characters (!@#$%^&*)
        - Avoid common words, names, and patterns
        - Don't reuse passwords across different accounts
        - Consider using a password manager
        - Enable two-factor authentication (2FA) when available
        """)
    else:
        st.info("👆 Enter a password above to check its strength")

with tab2:
    st.subheader("Password Generator")
    st.markdown("Generate a secure random password with customizable options.")
    
    col1, col2 = st.columns(2)
    with col1:
        gen_length = st.slider("Password Length", min_value=8, max_value=32, value=16)
        use_upper = st.checkbox("Uppercase Letters (A-Z)", value=True, key="gen_upper")
        use_lower = st.checkbox("Lowercase Letters (a-z)", value=True, key="gen_lower")
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        use_digits = st.checkbox("Numbers (0-9)", value=True, key="gen_digits")
        use_special = st.checkbox("Special Characters (!@#$...)", value=True, key="gen_special")
    
    if st.button("🎲 Generate Password", type="primary"):
        generated_pwd = generate_password(gen_length, use_upper, use_lower, use_digits, use_special)
        if generated_pwd:
            st.session_state['generated_password'] = generated_pwd
        else:
            st.error("Please select at least one character type!")
    
    if 'generated_password' in st.session_state:
        st.success("Generated Password:")
        st.code(st.session_state['generated_password'], language=None)
        
        # Analyze the generated password
        gen_result = check_password_strength(st.session_state['generated_password'])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Strength", gen_result['strength'])
        with col2:
            st.metric("Score", f"{gen_result['score']}/100")
        with col3:
            st.metric("Entropy", f"{gen_result['entropy']:.1f} bits")

with tab3:
    st.subheader("Compare Multiple Passwords")
    st.markdown("Compare the strength of different passwords side by side.")
    
    num_passwords = st.number_input("Number of passwords to compare", min_value=2, max_value=5, value=2)
    
    passwords_to_compare = []
    for i in range(num_passwords):
        pwd = st.text_input(
            f"Password {i+1}",
            type="password",
            key=f"compare_{i}",
            placeholder=f"Enter password {i+1}"
        )
        passwords_to_compare.append(pwd)
    
    if st.button("Compare Passwords"):
        if all(passwords_to_compare):
            st.markdown("### Comparison Results")
            
            results = []
            for i, pwd in enumerate(passwords_to_compare):
                result = check_password_strength(pwd)
                results.append({
                    'Password': f"Password {i+1}",
                    'Strength': f"{result['emoji']} {result['strength']}",
                    'Score': result['score'],
                    'Entropy': f"{result['entropy']:.1f}",
                    'Crack Time': result['crack_time']
                })
            
            # Create comparison table
            import pandas as pd
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Highlight strongest
            best_idx = max(range(len(results)), key=lambda i: results[i]['Score'])
            st.success(f"🏆 {results[best_idx]['Password']} is the strongest!")
        else:
            st.warning("Please enter all passwords to compare.")

with tab4:
    st.subheader("Export Password Strength Report")
    st.markdown("Generate a detailed report of your password analysis.")
    
    export_password = st.text_input(
        "Enter password to analyze",
        type="password",
        key="export_pwd",
        placeholder="Type your password here..."
    )
    
    if export_password:
        result = check_password_strength(export_password)
        
        report = f"""
PASSWORD STRENGTH REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

OVERALL RATING: {result['strength']} {result['emoji']}
Score: {result['score']}/100

SECURITY METRICS:
- Entropy: {result['entropy']:.2f} bits
- Estimated Crack Time: {result['crack_time']}

CRITERIA MET:
- Length (8+ chars): {'✓' if result['criteria']['length'] else '✗'}
- Lowercase Letters: {'✓' if result['criteria']['lowercase'] else '✗'}
- Uppercase Letters: {'✓' if result['criteria']['uppercase'] else '✗'}
- Numbers: {'✓' if result['criteria']['numbers'] else '✗'}
- Special Characters: {'✓' if result['criteria']['special'] else '✗'}

DETAILED FEEDBACK:
"""
        for item in result['feedback']:
            report += f"- {item}\n"
        
        report += f"""
BREACH CHECK:
{'⚠️ WARNING: Password found in common breach databases!' if check_common_breach(export_password) else '✓ Not found in common breach databases'}

RECOMMENDATIONS:
- Use at least 12 characters (longer is better)
- Mix uppercase and lowercase letters
- Include numbers and special characters
- Avoid common words and patterns
- Don't reuse passwords across accounts
- Consider using a password manager
- Enable two-factor authentication (2FA)

{'='*50}
Note: This report does not contain your actual password.
"""
        
        st.text_area("Report Preview", report, height=400)
        
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name=f"password_strength_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("👆 Enter a password to generate a report")

# Footer
st.markdown("---")
st.caption("🔒 Your passwords are analyzed locally and never stored or transmitted.")
