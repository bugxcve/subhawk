#!/usr/bin/env python3
"""
Subdomain Enumeration Tool
A comprehensive subdomain discovery tool using multiple enumeration techniques.

Author: Your Name
Date: 2026
License: MIT
"""

import requests
import dns.resolver
import subprocess
import json
import argparse
import sys
import time
from datetime import datetime
from typing import Set, List
import socket

# Try to import sublist3r, if not installed, provide installation instructions
try:
    import sublist3r
except ImportError:
    print("[!] sublist3r not installed. Install with: pip install sublist3r")
    sys.exit(1)


class SubdomainEnumerator:
    """
    Main class for subdomain enumeration using multiple techniques.
    """

    def __init__(self, domain: str, verbose: bool = False):
        """
        Initialize the enumerator.
        
        Args:
            domain (str): Target domain to enumerate
            verbose (bool): Enable verbose output
        """
        self.domain = domain
        self.verbose = verbose
        self.subdomains: Set[str] = set()
        self.results = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'techniques': {},
            'total_subdomains': 0
        }

    def log(self, message: str, level: str = "INFO"):
        """Print log messages with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    # ==================== Technique 1: Sublist3r ====================
    def enumerate_sublist3r(self) -> Set[str]:
        """
        Use Sublist3r for subdomain enumeration.
        Uses search engines and other public sources.
        """
        self.log("Starting Sublist3r enumeration...")
        sublist3r_subs = set()
        
        try:
            # Run sublist3r
            subdomains = sublist3r.main(
                self.domain,
                40,  # number of threads
                output=None,
                ports=None,
                silent=True,
                verbose=self.verbose,
                enable_bruteforce=False,
                save=False
            )
            
            if subdomains:
                sublist3r_subs = set(subdomains)
                self.log(f"Found {len(sublist3r_subs)} subdomains via Sublist3r", "SUCCESS")
            else:
                self.log("Sublist3r found no subdomains", "WARNING")
                
        except Exception as e:
            self.log(f"Sublist3r enumeration failed: {str(e)}", "ERROR")
        
        self.results['techniques']['sublist3r'] = list(sublist3r_subs)
        return sublist3r_subs

    # ==================== Technique 2: Certificate Transparency ====================
    def enumerate_certificate_transparency(self) -> Set[str]:
        """
        Query Certificate Transparency logs via crt.sh for subdomains.
        """
        self.log("Starting Certificate Transparency enumeration...")
        ct_subs = set()
        
        try:
            url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            ct_data = response.json()
            
            for entry in ct_data:
                name_value = entry.get('name_value', '')
                # Split by newline in case of multiple names
                for subdomain in name_value.split('\n'):
                    subdomain = subdomain.strip()
                    if subdomain and subdomain.endswith(self.domain):
                        ct_subs.add(subdomain)
            
            self.log(f"Found {len(ct_subs)} subdomains via Certificate Transparency", "SUCCESS")
            
        except requests.RequestException as e:
            self.log(f"Certificate Transparency enumeration failed: {str(e)}", "ERROR")
        except json.JSONDecodeError:
            self.log("Failed to parse Certificate Transparency response", "ERROR")
        
        self.results['techniques']['certificate_transparency'] = list(ct_subs)
        return ct_subs

    # ==================== Technique 3: DNS Enumeration ====================
    def enumerate_dns_records(self) -> Set[str]:
        """
        Perform DNS enumeration to find subdomains.
        """
        self.log("Starting DNS enumeration...")
        dns_subs = set()
        
        try:
            # Try to get DNS NS records
            try:
                ns_records = dns.resolver.resolve(self.domain, 'NS')
                nameservers = [str(rr.target).rstrip('.') for rr in ns_records]
                self.log(f"Found nameservers: {', '.join(nameservers)}", "INFO")
            except Exception as e:
                self.log(f"Failed to resolve NS records: {str(e)}", "WARNING")
                nameservers = []
            
            # Try to get A records
            try:
                a_records = dns.resolver.resolve(self.domain, 'A')
                self.log(f"Domain resolves to: {[str(rr) for rr in a_records]}", "INFO")
            except Exception as e:
                self.log(f"Failed to resolve A records: {str(e)}", "WARNING")
            
            # Try to get MX records
            try:
                mx_records = dns.resolver.resolve(self.domain, 'MX')
                for mx in mx_records:
                    mx_host = str(mx.exchange).rstrip('.')
                    dns_subs.add(mx_host)
            except Exception as e:
                self.log(f"Failed to resolve MX records: {str(e)}", "WARNING")
            
        except Exception as e:
            self.log(f"DNS enumeration failed: {str(e)}", "ERROR")
        
        self.results['techniques']['dns_enumeration'] = list(dns_subs)
        return dns_subs

    # ==================== Technique 4: Common Subdomain Bruteforce ====================
    def enumerate_brute_force(self) -> Set[str]:
        """
        Brute force common subdomain names.
        """
        self.log("Starting brute force enumeration...")
        brute_subs = set()
        
        # Common subdomain prefixes
        common_subs = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1',
            'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig',
            'm', 'imap', 'test', 'portal', 'admin', 'api', 'cdn', 'blog',
            'shop', 'dev', 'staging', 'staging-api', 'test-api', 'demo',
            'dashboard', 'panel', 'backup', 'mail1', 'mail2', 'db', 'database',
            'git', 'gitlab', 'github', 'jenkins', 'vpn', 'vpn2', 'server',
            'app', 'apps', 'service', 'services', 'static', 'downloads',
            'documents', 'docs', 'support', 'help', 'helpdesk', 'wiki',
            'forum', 'forums', 'chat', 'slack', 'teams', 'social',
            'internal', 'corp', 'corporate', 'secure', 'cloud', 'storage'
        ]
        
        for subdomain in common_subs:
            test_url = f"{subdomain}.{self.domain}"
            try:
                # Try DNS resolution
                socket.gethostbyname(test_url)
                brute_subs.add(test_url)
                self.log(f"Found subdomain via brute force: {test_url}", "SUCCESS")
            except socket.gaierror:
                pass  # Subdomain doesn't exist
            except Exception as e:
                pass  # Other errors, continue
            
            time.sleep(0.1)  # Rate limiting to avoid blocking
        
        self.log(f"Found {len(brute_subs)} subdomains via brute force", "SUCCESS")
        self.results['techniques']['brute_force'] = list(brute_subs)
        return brute_subs

    # ==================== Technique 5: Public APIs ====================
    def enumerate_public_apis(self) -> Set[str]:
        """
        Query public subdomain APIs like Shodan, VirusTotal, etc.
        Note: These may require API keys.
        """
        self.log("Starting public API enumeration...")
        api_subs = set()
        
        # Try Shodan API (requires API key)
        shodan_key = None  # Set your Shodan API key here
        if shodan_key:
            try:
                import shodan
                api = shodan.Shodan(shodan_key)
                results = api.search(f'hostname:{self.domain}')
                for result in results['matches']:
                    api_subs.add(result['hostname'])
                self.log(f"Found {len(api_subs)} subdomains via Shodan", "SUCCESS")
            except Exception as e:
                self.log(f"Shodan API enumeration failed: {str(e)}", "WARNING")
        
        # Try HackerTarget API (Free, no key needed)
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            for line in response.text.strip().split('\n'):
                if line and ',' in line:
                    subdomain = line.split(',')[0].strip()
                    if subdomain:
                        api_subs.add(subdomain)
            
            if api_subs:
                self.log(f"Found {len(api_subs)} subdomains via HackerTarget", "SUCCESS")
        except Exception as e:
            self.log(f"HackerTarget API enumeration failed: {str(e)}", "WARNING")
        
        self.results['techniques']['public_apis'] = list(api_subs)
        return api_subs

    # ==================== Main Enumeration ====================
    def enumerate_all(self) -> Set[str]:
        """
        Run all enumeration techniques.
        """
        self.log(f"Starting enumeration for domain: {self.domain}")
        self.log("=" * 60)
        
        # Run all techniques
        self.subdomains.update(self.enumerate_sublist3r())
        self.subdomains.update(self.enumerate_certificate_transparency())
        self.subdomains.update(self.enumerate_dns_records())
        self.subdomains.update(self.enumerate_brute_force())
        self.subdomains.update(self.enumerate_public_apis())
        
        # Remove root domain if it got added
        self.subdomains.discard(self.domain)
        
        self.log("=" * 60)
        self.log(f"Enumeration complete. Found {len(self.subdomains)} unique subdomains")
        
        self.results['total_subdomains'] = len(self.subdomains)
        self.results['subdomains'] = sorted(list(self.subdomains))
        
        return self.subdomains

    def verify_subdomains(self) -> dict:
        """
        Verify which subdomains are actually resolvable.
        """
        self.log("Verifying subdomains...")
        verified = {}
        
        for subdomain in self.subdomains:
            try:
                ip = socket.gethostbyname(subdomain)
                verified[subdomain] = ip
                self.log(f"✓ {subdomain} -> {ip}", "SUCCESS")
            except socket.gaierror:
                self.log(f"✗ {subdomain} (no DNS record)", "WARNING")
            except Exception as e:
                pass
        
        self.results['verified_subdomains'] = verified
        return verified

    def save_results(self, output_file: str = None):
        """
        Save results to files (JSON and TXT formats).
        """
        if output_file is None:
            output_file = f"subdomains_{self.domain}_{int(time.time())}"
        
        # Save as JSON
        json_file = f"{output_file}.json"
        try:
            with open(json_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            self.log(f"Results saved to {json_file}", "SUCCESS")
        except Exception as e:
            self.log(f"Failed to save JSON: {str(e)}", "ERROR")
        
        # Save as TXT (simple list)
        txt_file = f"{output_file}.txt"
        try:
            with open(txt_file, 'w') as f:
                f.write(f"Subdomains for {self.domain}\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write("=" * 60 + "\n\n")
                for subdomain in sorted(self.subdomains):
                    f.write(f"{subdomain}\n")
            self.log(f"Results saved to {txt_file}", "SUCCESS")
        except Exception as e:
            self.log(f"Failed to save TXT: {str(e)}", "ERROR")
        
        return json_file, txt_file

    def print_summary(self):
        """Print a summary of results."""
        print("\n" + "=" * 60)
        print(f"SUBDOMAIN ENUMERATION SUMMARY FOR: {self.domain}")
        print("=" * 60)
        print(f"\nTotal Subdomains Found: {len(self.subdomains)}\n")
        
        if self.subdomains:
            print("Discovered Subdomains:")
            print("-" * 60)
            for subdomain in sorted(self.subdomains):
                print(f"  • {subdomain}")
        
        print("\n" + "=" * 60 + "\n")


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Comprehensive Subdomain Enumeration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 subdomain_enumerator.py google.com
  python3 subdomain_enumerator.py example.com -v
  python3 subdomain_enumerator.py test.com -o results
  python3 subdomain_enumerator.py test.com -v --verify
        '''
    )
    
    parser.add_argument('domain', help='Target domain to enumerate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-o', '--output', help='Output file name (without extension)')
    parser.add_argument('--verify', action='store_true', help='Verify DNS resolution for found subdomains')
    
    args = parser.parse_args()
    
    try:
        # Initialize enumerator
        enumerator = SubdomainEnumerator(args.domain, args.verbose)
        
        # Run enumeration
        subdomains = enumerator.enumerate_all()
        
        # Verify if requested
        if args.verify:
            print()
            enumerator.verify_subdomains()
        
        # Save results
        output_file = args.output or f"subdomains_{args.domain}"
        json_file, txt_file = enumerator.save_results(output_file)
        
        # Print summary
        enumerator.print_summary()
        
        print(f"Results saved to:")
        print(f"  • {json_file}")
        print(f"  • {txt_file}\n")
        
    except KeyboardInterrupt:
        print("\n\n[!] Enumeration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
