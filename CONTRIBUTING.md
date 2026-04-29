# Contributing to Subdomain Enumeration Tool

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and constructive in all interactions
- Follow ethical guidelines for security research
- Respect the privacy and legal rights of others
- No harassment, discrimination, or offensive content

## Getting Started

### 1. Fork the Repository

Click the "Fork" button on the GitHub repository page to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/subhawk.git
cd subhawk
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest black flake8
```

### 4. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep lines under 100 characters when possible

### Code Format

Use `black` to format your code:

```bash
black subhawk.py
```

### Linting

Check your code with `flake8`:

```bash
flake8 subhawk.py
```

### Testing

- Test your changes thoroughly
- Write tests for new features
- Ensure existing tests still pass

```bash
# Run tests
pytest tests/

# Or test manually
python3 subhawk.py google.com -v
```

## Types of Contributions

### 🐛 Bug Reports

If you find a bug:

1. Check if the issue already exists
2. Create an issue with:
   - Clear title describing the bug
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Error traceback (if applicable)

Example:
```
Title: Certificate Transparency timeout on large domains

Description:
When enumerating large domains (>1000 subdomains), the CT enumeration times out.

Steps to Reproduce:
1. Run: python3 subhawk.py largedomain.com
2. CT enumeration hangs after 30 seconds

Expected: Graceful timeout with partial results
Actual: Process hangs indefinitely

Environment: Python 3.9.0, Ubuntu 20.04
```

### ✨ Feature Requests

For new features:

1. Check if it's already requested
2. Create an issue with:
   - Clear title
   - Description of the feature
   - Use cases and benefits
   - Potential implementation approach (optional)

Example:
```
Title: Add WHOIS enumeration technique

Description:
Implement subdomain discovery via WHOIS queries.

Benefits:
- Additional data source for subdomain discovery
- No rate limiting concerns
- Can identify registrant information

Use Cases:
- Finding hidden subdomains from WHOIS records
- Reconnaissance phase of penetration testing
```

### 🔧 Code Improvements

Areas where help is needed:

- **New Enumeration Techniques**
  - Additional API integrations
  - Alternative DNS techniques
  - Web scraping methods

- **Performance Optimization**
  - Faster enumeration
  - Better parallelization
  - Memory efficiency

- **Code Quality**
  - Refactoring
  - Better error handling
  - Additional logging

- **Documentation**
  - Improved README
  - API documentation
  - Usage examples

### 📝 Documentation

Help improve documentation:

- Fix typos
- Improve clarity
- Add examples
- Update outdated information
- Translate to other languages

## Submission Process

### 1. Make Your Changes

```bash
# Make your changes to the code
# Example: Add a new enumeration technique

nano subhawk.py
```

### 2. Commit Your Changes

```bash
git add .
git commit -m "Add new enumeration technique: XXX

Description of changes:
- Added XX class
- Implemented YY functionality
- Improved ZZ performance"
```

#### Commit Message Guidelines:

- First line: Brief summary (50 chars max)
- Blank line
- Detailed explanation (if needed)
- Reference issues: "Fixes #123"
- Use imperative mood: "Add feature" not "Added feature"

### 3. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 4. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill in the PR template with:
   - Description of changes
   - Related issues
   - Testing done
   - Screenshots (if applicable)

#### PR Template:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other

## Related Issues
Fixes #123
Related to #456

## Testing Done
- [ ] Manual testing on Windows
- [ ] Manual testing on Linux
- [ ] Manual testing on macOS
- [ ] Tested with Python 3.7
- [ ] Tested with Python 3.9
- [ ] Tested with Python 3.11

## Checklist
- [ ] Code follows PEP 8 style
- [ ] Code is properly documented
- [ ] No new warnings from flake8
- [ ] All existing tests pass
- [ ] Added tests for new functionality
- [ ] README updated if needed
- [ ] No sensitive data committed
```

## Code Review

- Respond to feedback constructively
- Be open to suggestions
- Make requested changes
- Request re-review after updates

## Recognition

Contributors will be recognized in:
- README.md contributors section
- GitHub contributors graph
- Release notes

## Questions?

- Check existing issues/discussions
- Comment on related issues
- Email: your.email@example.com

## Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Commit Best Practices](https://chris.beams.io/posts/git-commit/)
- [Semantic Versioning](https://semver.org/)

Thank you for contributing! 🙏
