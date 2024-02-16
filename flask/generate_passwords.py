from flask import Flask, render_template, request, jsonify
import string
import random
import secrets

# Example word list for passphrase generation
word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]

# Function to create a pronounceable password
def generate_pronounceable_password(length):
    vowels = "aeiou"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))

    password = ""
    for i in range(length):
        if i % 2 == 0:
            # Add a consonant
            password += secrets.choice(consonants)
        else:
            # Add a vowel
            password += secrets.choice(vowels)
    
    return password

# Function to create a passphrase
def generate_passphrase(num_words, word_list):
    return '-'.join(secrets.choice(word_list) for _ in range(num_words))

def decorate_password(password, segment_length):
    # Function to replace a character at a given index in a string
    def replace_char(string, index, new_char):
        return string[:index] + new_char + string[index + 1:]

    # Split the password into segments of 'segment_length' each
    segments = [password[i:i + segment_length] for i in range(0, len(password), segment_length)]

    # Ensure each segment is exactly 'segment_length' characters
    segments = [seg if len(seg) == segment_length else seg + secrets.choice(string.ascii_letters + string.digits) * (segment_length - len(seg)) for seg in segments]

    # Check and replace characters if a segment starts or ends with '-'
    for i, segment in enumerate(segments):
        if segment.startswith('-'):
            # Replace the first character
            segments[i] = replace_char(segment, 0, random.choice(string.ascii_letters + string.digits))
        if segment.endswith('-'):
            # Replace the last character
            segments[i] = replace_char(segment, -1, random.choice(string.ascii_letters + string.digits))
    return '-'.join(segments)

def generate_passwords(num_passwords, length, use_uppercase, use_lowercase, use_digits, use_symbols, min_segment_length=3, max_segment_length=5, decorate_passwords=False):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    passwords = []
    for _ in range(num_passwords):
        password = ''
        while len(password) < length:
            segment_length = secrets.choice(range(min_segment_length, max_segment_length + 1))
            password += ''.join(secrets.choice(characters) for _ in range(segment_length))
        password = password[:length]  # Ensure password is not longer than the specified length
        if decorate_passwords:
            password = decorate_password(password, 4)  # Force segment length to 4 for decoration
        passwords.append(password)

    return passwords

def generate_password(version):
    data = request.form
    num_passwords = int(data.get('num_passwords', 5))
    password_length = int(data.get('password_length', 32))
    uppercase = 'uppercase' in data
    lowercase = 'lowercase' in data
    digits = 'digits' in data
    symbols = 'symbols' in data
    decorate_passwords = 'decorate_passwords' in data
    method_pronounceable = 'method_pronounceable' in data
    method_passphrase = 'method_passphrase' in data

    generated_passwords = []

    if request.method == 'POST':
        for _ in range(num_passwords):
            password = ''
            if method_pronounceable or method_passphrase:
                # Reset lowercase if pronounceable or passphrase is selected
                if lowercase:
                    lowercase = False

                # Generate password based on selected method
                if method_pronounceable:
                    password = generate_pronounceable_password(password_length)
                else:
                    password = generate_passphrase(4, word_list)  # Assuming 4 words per passphrase

                # Capitalize and modify each segment if required
                if decorate_passwords and (uppercase or digits):
                    segments = password.split('-')
                    modified_segments = [segment.capitalize() + secrets.choice(string.digits) for segment in segments]
                    password = '-'.join(modified_segments)
                elif decorate_passwords:
                    password = decorate_password(password, 4)

            else:
                # Standard password generation
                password = generate_passwords(1, password_length, uppercase, lowercase, digits, symbols, decorate_passwords=decorate_passwords)[0]

            generated_passwords.append(password)

        return render_template('random_password.html', passwords=generated_passwords, version=version)
    else:
        return render_template('random_password.html', version=version)






