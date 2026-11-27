
# ENV FILE AND SECRET PROTECTION RULES

## 1. Sensitive File Protection

- Treat config as a confidential file.
- Never expose or display the actual contents of config.
- Never copy credentials from config into application source code.
- Never include config contents in generated documentation.
- Never commit config to GitHub.
- Never modify or delete config without explicit approval.

## 2. MySQL Credential Protection

- Never hardcode MySQL username in application code.
- Never hardcode MySQL password in application code.
- Read database credentials from environment variables.
- Never print database credentials in application logs.
- Never expose database connection strings containing passwords.

## 3. API Key Protection

- Never hardcode API_KEY or API_SECRET.
- Never expose API keys in frontend JavaScript or React components.
- Never return API keys through API responses.
- Never display API keys in error messages.
- Never print API keys in application logs.

## 4. Git Protection

- Ensure config is included in backend/.gitignore.
- Never stage or commit config.
- If config is accidentally committed, report the security risk.
- Recommend rotating exposed credentials immediately.
- Use config.example with placeholder values
  for documenting required environment variables.

## 5. Application Development Rules

- Use Python environment variables to access credentials.
- Validate that required environment variables exist.
- Never use dummy credentials as production credentials.
- Keep all database connections and secret handling
  inside the backend.
- Never expose confidential configuration to the frontend.

## 6. Mandatory Behaviour

Before modifying any configuration or application file:

1. Check whether the change involves sensitive credentials.
2. Identify potential exposure risks.
3. Never reveal actual secret values.
4. Explain any security violation.
5. Suggest a secure alternative.

These rules must be followed for all development
activities in this repository.
