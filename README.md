# Subdomain Enumeration Tool 🔍

A powerful and comprehensive Python-based subdomain discovery tool that combines multiple enumeration techniques to identify subdomains of a target domain. Perfect for security researchers, penetration testers, and bug bounty hunters.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Enumeration Techniques](#enumeration-techniques)
- [Output](#output)
- [Examples](#examples)
- [API Keys (Optional)](#api-keys-optional)
- [Contributing](#contributing)
- [Legal & Disclaimer](#legal--disclaimer)
- [License](#license)
- [Author](#author)

## Features

✅ **Multiple Enumeration Techniques**
- Sublist3r integration for search engine enumeration
- Certificate Transparency log querying (crt.sh)
- DNS record enumeration (NS, MX, A records)
- Common subdomain brute force
- Public API queries (HackerTarget, Shodan)

✅ **Flexible Output**
- JSON format (structured data)
- Plain text format (simple list)
- Subdomain verification with IP resolution
- Detailed enumeration reports

✅ **User-Friendly**
- Command-line interface with argument parsing
- Verbose output mode for debugging
- Progress indicators and logging
- Organized result display

✅ **Performance**
- Multi-threaded operations
- Rate limiting to avoid blocking
- Timeout handling for network requests
- Efficient duplicate removal

## Prerequisites

### System Requirements
- Python 3.7 or higher
- Internet connection for external API queries
- 100MB free disk space for dependencies

### Python Packages
- `sublist3r` - Main subdomain enumeration library
- `dnspython` - DNS query functionality
- `requests` - HTTP requests for API queries

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/subdomain-enumerator.git
cd subdomain-enumerator
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Make Script Executable (Linux/macOS)

```bash
chmod +x findomain.py
```

## Usage

### Basic Usage

```bash
python3 findomain.py example.com
```

### With All Options

```bash
python3 findomain.py example.com -v --verify -o results
```

### Command-Line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `domain` | - | Target domain to enumerate (required) |
| `--verbose` | `-v` | Enable verbose output with detailed logging |
| `--output` | `-o` | Specify output file name (without extension) |
| `--verify` | - | Verify DNS resolution for found subdomains |

## Enumeration Techniques

### 1. **Sublist3r**
- Uses multiple search engines (Google, Yahoo, Bing, Baidu, etc.)
- Queries public subdomain databases
- Multi-threaded for fast enumeration
- No authentication required

### 2. **Certificate Transparency (CT)**
- Queries crt.sh SSL certificate database
- Identifies subdomains from issued SSL certificates
- Very reliable for active subdomains
- No authentication required

### 3. **DNS Enumeration**
- Resolves NS records to find nameservers
- Queries A, MX, and other DNS records
- Identifies mail servers and other services
- No authentication required

### 4. **Brute Force**
- Tests common subdomain prefixes
- Covers 50+ common subdomain names
- Rate-limited to avoid blocking
- Includes: www, mail, ftp, api, dev, staging, admin, etc.

### 5. **Public APIs**
- **HackerTarget API** (Free, no key required)
- **Shodan API** (Optional, requires API key)
- Passive reconnaissance data
- No rate limiting issues for HackerTarget

## Output

The tool generates two output files:

### JSON Output (`subdomains_example.com_TIMESTAMP.json`)
```json
{
  "domain": "example.com",
  "timestamp": "2026-04-29T10:30:45.123456",
  "techniques": {
    "sublist3r": ["www.example.com", "mail.example.com"],
    "certificate_transparency": ["api.example.com", "cdn.example.com"],
    "dns_enumeration": ["mail.example.com"],
    "brute_force": ["ftp.example.com"],
    "public_apis": ["dev.example.com"]
  },
  "total_subdomains": 8,
  "subdomains": ["api.example.com", "cdn.example.com", ...],
  "verified_subdomains": {
    "www.example.com": "93.184.216.34",
    "mail.example.com": "93.184.216.35"
  }
}
```

### Text Output (`subdomains_example.com_TIMESTAMP.txt`)
```
Subdomains for example.com
Generated: 2026-04-29 10:30:45

============================================================

api.example.com
cdn.example.com
dev.example.com
ftp.example.com
mail.example.com
www.example.com
```

## Examples

### Example 1: Basic Enumeration
```bash
$ python3 findomain.py google.com

[2026-04-29 10:30:00] [INFO] Starting enumeration for domain: google.com
[2026-04-29 10:30:05] [SUCCESS] Found 45 subdomains via Sublist3r
[2026-04-29 10:30:10] [SUCCESS] Found 120 subdomains via Certificate Transparency
...
[2026-04-29 10:31:00] [SUCCESS] Enumeration complete. Found 200 unique subdomains

============================================================
SUBDOMAIN ENUMERATION SUMMARY FOR: google.com
============================================================

Total Subdomains Found: 200

Discovered Subdomains:
------------------------------------------------------------
  • accounts.google.com
  • ads.google.com
  • android.google.com
  • api.google.com
  ...
```

### Example 2: Verbose with Verification
```bash
python3 findomain.py example.com -v --verify -o my_results
```

### Example 3: Check Specific Domain with Output
```bash
python3 findomain.py tesla.com -o tesla_subdomains
```

## API Keys (Optional)

### Shodan API (Optional)

To use Shodan API for additional enumeration:

1. Get a free account at https://www.shodan.io/
2. Get your API key from https://account.shodan.io/
3. Add the key to line 244 in `findomain.py`:

```python
shodan_key = "YOUR_SHODAN_API_KEY_HERE"
```

**Note:** Shodan integration is optional. The tool works perfectly fine without it.

## Performance Tips

- **Use `--verify` flag** to ensure subdomains are actually resolvable
- **Save results to file** for large domain enumerations (100+ subdomains)
- **Use verbose mode** only when debugging issues
- **Run during off-peak hours** to minimize network impact on target

## Limitations

- Requires active internet connection
- Rate limited on some APIs to avoid blocking
- Can only find subdomains that:
  - Have DNS records
  - Have SSL certificates issued
  - Are indexed by search engines
  - Are in public databases
- Does not perform deep crawling or active probing

## Troubleshooting

### Issue: "sublist3r not installed"
```bash
pip install sublist3r
```

### Issue: "DNS resolution errors"
Check your internet connection and firewall settings. Some networks block DNS queries.

### Issue: "Certificate Transparency timeout"
The crt.sh server may be temporarily unavailable. Try again later.

### Issue: "Rate limited by HackerTarget"
The tool includes rate limiting. If you get blocked, wait a few minutes before retrying.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Additional enumeration techniques
- Performance improvements
- Additional API integrations
- Better documentation
- Bug fixes

## Legal & Disclaimer

⚠️ **IMPORTANT LEGAL NOTICE**

This tool is provided for **authorized security testing only**. Unauthorized access to computer systems is illegal.

### Before Using This Tool:

1. **Get Written Permission**: Only scan domains you own or have explicit written permission to test
2. **Follow Local Laws**: Ensure your activities comply with local, state, and federal laws
3. **Respect Terms of Service**: Comply with the terms of service of target websites
4. **Responsible Disclosure**: If you find vulnerabilities, report them responsibly through proper channels

### Disclaimer:

The authors and contributors assume no liability and are not responsible for any misuse or damage caused by this tool. Users are solely responsible for their actions.

**This tool is for educational and authorized security testing purposes only.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- Website: [yourwebsite.com](https://yourwebsite.com)

## Support

- 📝 Report bugs: [GitHub Issues](https://github.com/yourusername/subdomain-enumerator/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/subdomain-enumerator/discussions)
- 📧 Email: your.email@example.com

## Changelog

### Version 1.0.0 (2026-04-29)
- Initial release
- 5 enumeration techniques
- JSON and TXT output formats
- DNS verification capability
- Command-line interface

## Acknowledgments

- [Sublist3r](https://github.com/aboul3la/Sublist3r) - Core enumeration library
- [crt.sh](https://crt.sh) - Certificate Transparency database
- [HackerTarget](https://api.hackertarget.com) - Subdomain API
- Python community

---

**⭐ If you find this tool useful, please consider giving it a star on GitHub!**
