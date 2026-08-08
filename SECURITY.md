# Security Policy

## Supported Versions

The table below details which versions of the AI Voice IT Helpdesk Agent actively receive security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability within this repository (e.g. JWT secret handling, credential exposure, or SQL injection risks):

1. **Do NOT open a public GitHub issue.**
2. Send an email describing the vulnerability to `security@yourdomain.com` (or create a private GitHub Security Advisory).
3. Include:
   - Steps to reproduce the issue
   - Affected API endpoints or files
   - Potential impact
   - Suggested remediation (if available)

We will acknowledge receipt within **48 hours** and provide periodic status updates until the vulnerability is resolved.

---

## Best Practices for Deployment

- **Never Commit Secrets**: Never commit real `.env` files, JWT secret keys, OpenAI API keys, ElevenLabs keys, or Database URLs to version control.
- **Use `.env.example`**: Keep `.env.example` scrubbed of all real credentials.
- **Environment Isolation**: In production, pass sensitive environment variables via secure environment secret stores (e.g., Render, Railway, AWS Secrets Manager, GitHub Actions Secrets).
