#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         SUBHAWK v2.0                                   ║
║          Advanced Subdomain Discovery with Interactive CLI UI            ║
╚═══════════════════════════════════════════════════════════════════════════╝

Tool: subhawk
Author: bugxcve
Version: 2.0.0
License: MIT
GitHub: https://github.com/bugxcve/subhawk

Description:
    A comprehensive subdomain discovery tool using multiple enumeration
    techniques with beautiful CLI interface and interactive mode.

Features:
    ✓ 5 Enumeration Techniques
    ✓ Interactive CLI Mode
    ✓ Beautiful UI with Colors
    ✓ DNS Verification
    ✓ JSON & TXT Output
    ✓ Progress Indicators
    ✓ Domain Validation
"""

import requests
import dns.resolver
import json
import argparse
import sys
import time
import socket
import re
from datetime import datetime
from typing import Set, List, Dict
from pathlib import Path

# Try to import rich for beautiful UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.text import Text
    from rich.box import ROUNDED
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("[!] Rich library not installed. Install with: pip install rich")
    print("[*] Continuing with basic output...\n")

# Try to import sublist3r
try:
    import sublist3r
    SUBLIST3R_AVAILABLE = True
except ImportError:
    SUBLIST3R_AVAILABLE = False
    print("[!] sublist3r not installed. Install with: pip install sublist3r")

# Initialize console
console = Console() if RICH_AVAILABLE else None


def print_header():
    """Print beautiful header"""
    if RICH_AVAILABLE:
        header_text = Text()
        header_text.append("╔═══════════════════════════════════════════════════════════════════════════╗\n", style="cyan bold")
        header_text.append("║                        SUBHAWK v2.0                                   ║\n", style="cyan bold")
        header_text.append("║                   Author: bugxcve | License: MIT                         ║\n", style="magenta")
        header_text.append("║              Advanced Subdomain Discovery with Interactive CLI           ║\n", style="yellow")
        header_text.append("╚═══════════════════════════════════════════════════════════════════════════╝\n", style="cyan bold")
        console.print(header_text)
    else:
        print("╔═══════════════════════════════════════════════════════════════════════════╗")
        print("║                        SUBHAWK v2.0                                   ║")
        print("║                   Author: bugxcve | License: MIT                         ║")
        print("║              Advanced Subdomain Discovery with Interactive CLI           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════╝\n")


def validate_domain(domain: str) -> bool:
    """Validate domain name format"""
    domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return re.match(domain_pattern, domain) is not None


def log_msg(message: str, level: str = "INFO", emoji: str = "ℹ️"):
    """Print log message with style"""
    if RICH_AVAILABLE:
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "SUCCESS":
            console.print(f"[green]✓[/green] [{timestamp}] {message}")
        elif level == "ERROR":
            console.print(f"[red]✗[/red] [{timestamp}] {message}")
        elif level == "WARNING":
            console.print(f"[yellow]⚠[/yellow] [{timestamp}] {message}")
        elif level == "INFO":
            console.print(f"[cyan]ℹ[/cyan] [{timestamp}] {message}")
        else:
            console.print(f"[white]{emoji}[/white] [{timestamp}] {message}")
    else:
        print(f"[{level}] {message}")


class Findomain:
    """Advanced subdomain enumeration with CLI UI"""

    def __init__(self, domain: str, verbose: bool = False):
        self.domain = domain
        self.verbose = verbose
        self.subdomains: Set[str] = set()
        self.results = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'tool': 'findomain',
            'version': '2.0.0',
            'author': 'bugxcve',
            'techniques': {},
            'total_subdomains': 0,
            'subdomains': []
        }

    def enumerate_sublist3r(self) -> Set[str]:
        """Enumeration using Sublist3r"""
        subs = set()
        
        if not SUBLIST3R_AVAILABLE:
            log_msg("Sublist3r not available, skipping...", "WARNING")
            return subs

        try:
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Running Sublist3r...", total=None)
                    subdomains = sublist3r.main(
                        self.domain, 40, output=None, ports=None,
                        silent=True, verbose=False, enable_bruteforce=False, save=False
                    )
                    progress.update(task, completed=True)
            else:
                subdomains = sublist3r.main(
                    self.domain, 40, output=None, ports=None,
                    silent=True, verbose=False, enable_bruteforce=False, save=False
                )
            
            if subdomains:
                subs = set(subdomains)
                log_msg(f"Found {len(subs)} subdomains via Sublist3r", "SUCCESS")
            else:
                log_msg("Sublist3r found no subdomains", "WARNING")
        except Exception as e:
            log_msg(f"Sublist3r error: {str(e)}", "ERROR")
        
        self.results['techniques']['sublist3r'] = list(subs)
        return subs

    def enumerate_certificate_transparency(self) -> Set[str]:
        """Certificate Transparency enumeration"""
        ct_subs = set()
        
        try:
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Querying Certificate Transparency...", total=None)
                    url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    ct_data = response.json()
                    progress.update(task, completed=True)
            else:
                url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                ct_data = response.json()
            
            for entry in ct_data:
                name_value = entry.get('name_value', '')
                for subdomain in name_value.split('\n'):
                    subdomain = subdomain.strip()
                    if subdomain and subdomain.endswith(self.domain):
                        ct_subs.add(subdomain)
            
            log_msg(f"Found {len(ct_subs)} subdomains via Certificate Transparency", "SUCCESS")
        except Exception as e:
            log_msg(f"Certificate Transparency error: {str(e)}", "ERROR")
        
        self.results['techniques']['certificate_transparency'] = list(ct_subs)
        return ct_subs

    def enumerate_dns_records(self) -> Set[str]:
        """DNS record enumeration"""
        dns_subs = set()
        
        try:
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Performing DNS enumeration...", total=None)
                    
                    try:
                        ns_records = dns.resolver.resolve(self.domain, 'NS')
                        nameservers = [str(rr.target).rstrip('.') for rr in ns_records]
                        log_msg(f"Nameservers: {', '.join(nameservers[:3])}", "INFO")
                    except:
                        pass
                    
                    try:
                        mx_records = dns.resolver.resolve(self.domain, 'MX')
                        for mx in mx_records:
                            mx_host = str(mx.exchange).rstrip('.')
                            dns_subs.add(mx_host)
                    except:
                        pass
                    
                    progress.update(task, completed=True)
            else:
                try:
                    mx_records = dns.resolver.resolve(self.domain, 'MX')
                    for mx in mx_records:
                        mx_host = str(mx.exchange).rstrip('.')
                        dns_subs.add(mx_host)
                except:
                    pass
            
            if dns_subs:
                log_msg(f"Found {len(dns_subs)} records via DNS", "SUCCESS")
        except Exception as e:
            log_msg(f"DNS enumeration error: {str(e)}", "ERROR")
        
        self.results['techniques']['dns_enumeration'] = list(dns_subs)
        return dns_subs

    def enumerate_brute_force(self) -> Set[str]:
        """Brute force common subdomains"""
        brute_subs = set()
        
        common_subs = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1',
            'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig',
            'm', 'imap', 'test', 'portal', 'admin', 'api', 'cdn', 'blog',
            'shop', 'dev', 'staging', 'demo', 'dashboard', 'panel', 'backup',
            'git', 'jenkins', 'vpn', 'server', 'app', 'service', 'static',
            'docs', 'support', 'forum', 'chat', 'internal', 'secure', 'cloud'
        ]
        
        try:
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Brute forcing common subdomains...", total=len(common_subs))
                    
                    for subdomain in common_subs:
                        test_url = f"{subdomain}.{self.domain}"
                        try:
                            socket.gethostbyname(test_url)
                            brute_subs.add(test_url)
                        except:
                            pass
                        
                        progress.update(task, advance=1)
                        time.sleep(0.05)
            else:
                for subdomain in common_subs:
                    test_url = f"{subdomain}.{self.domain}"
                    try:
                        socket.gethostbyname(test_url)
                        brute_subs.add(test_url)
                    except:
                        pass
                    time.sleep(0.05)
            
            if brute_subs:
                log_msg(f"Found {len(brute_subs)} subdomains via brute force", "SUCCESS")
        except Exception as e:
            log_msg(f"Brute force error: {str(e)}", "ERROR")
        
        self.results['techniques']['brute_force'] = list(brute_subs)
        return brute_subs

    def enumerate_public_apis(self) -> Set[str]:
        """Public API enumeration"""
        api_subs = set()
        
        try:
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Querying public APIs...", total=None)
                    
                    try:
                        url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()
                        
                        for line in response.text.strip().split('\n'):
                            if line and ',' in line:
                                subdomain = line.split(',')[0].strip()
                                if subdomain:
                                    api_subs.add(subdomain)
                    except:
                        pass
                    
                    progress.update(task, completed=True)
            else:
                try:
                    url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    for line in response.text.strip().split('\n'):
                        if line and ',' in line:
                            subdomain = line.split(',')[0].strip()
                            if subdomain:
                                api_subs.add(subdomain)
                except:
                    pass
            
            if api_subs:
                log_msg(f"Found {len(api_subs)} subdomains via public APIs", "SUCCESS")
        except Exception as e:
            log_msg(f"Public API error: {str(e)}", "ERROR")
        
        self.results['techniques']['public_apis'] = list(api_subs)
        return api_subs

    def enumerate_all(self) -> Set[str]:
        """Run all enumeration techniques"""
        log_msg(f"Starting enumeration for: {self.domain}", "INFO")
        
        if RICH_AVAILABLE:
            console.print(Panel(f"[bold cyan]Target Domain:[/bold cyan] {self.domain}", title="[bold]Enumeration Started[/bold]", border_style="cyan"))
            console.print()
        else:
            print(f"\nTarget Domain: {self.domain}\n")
        
        self.subdomains.update(self.enumerate_sublist3r())
        self.subdomains.update(self.enumerate_certificate_transparency())
        self.subdomains.update(self.enumerate_dns_records())
        self.subdomains.update(self.enumerate_brute_force())
        self.subdomains.update(self.enumerate_public_apis())
        
        # Remove root domain
        self.subdomains.discard(self.domain)
        
        self.results['total_subdomains'] = len(self.subdomains)
        self.results['subdomains'] = sorted(list(self.subdomains))
        
        return self.subdomains

    def verify_subdomains(self) -> Dict[str, str]:
        """Verify subdomains with DNS resolution"""
        verified = {}
        
        try:
            if RICH_AVAILABLE:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Verifying DNS records...", total=len(self.subdomains))
                    
                    for subdomain in self.subdomains:
                        try:
                            ip = socket.gethostbyname(subdomain)
                            verified[subdomain] = ip
                        except:
                            pass
                        progress.update(task, advance=1)
            else:
                for subdomain in self.subdomains:
                    try:
                        ip = socket.gethostbyname(subdomain)
                        verified[subdomain] = ip
                    except:
                        pass
        except Exception as e:
            log_msg(f"Verification error: {str(e)}", "ERROR")
        
        self.results['verified_subdomains'] = verified
        return verified

    def save_results(self, output_file: str = None):
        """Save results to JSON and TXT"""
        if output_file is None:
            output_file = f"findomain_{self.domain}_{int(time.time())}"
        
        # JSON output
        json_file = f"{output_file}.json"
        try:
            with open(json_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            log_msg(f"Results saved to {json_file}", "SUCCESS")
        except Exception as e:
            log_msg(f"Failed to save JSON: {str(e)}", "ERROR")
        
        # TXT output
        txt_file = f"{output_file}.txt"
        try:
            with open(txt_file, 'w') as f:
                f.write(f"{'='*70}\n")
                f.write(f"FINDOMAIN v2.0 - Subdomains for: {self.domain}\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Total Found: {len(self.subdomains)}\n")
                f.write(f"Author: bugxcve\n")
                f.write(f"{'='*70}\n\n")
                for subdomain in sorted(self.subdomains):
                    f.write(f"{subdomain}\n")
            log_msg(f"Results saved to {txt_file}", "SUCCESS")
        except Exception as e:
            log_msg(f"Failed to save TXT: {str(e)}", "ERROR")
        
        return json_file, txt_file

    def display_results(self, verified: Dict[str, str] = None):
        """Display results in beautiful format"""
        if RICH_AVAILABLE:
            # Summary table
            summary_table = Table(title="[bold]Enumeration Summary[/bold]", box=ROUNDED)
            summary_table.add_column("Metric", style="cyan", width=30)
            summary_table.add_column("Value", style="green")
            
            summary_table.add_row("Target Domain", self.domain)
            summary_table.add_row("Total Subdomains", str(len(self.subdomains)))
            summary_table.add_row("Verified Subdomains", str(len(verified)) if verified else "0")
            summary_table.add_row("Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            console.print()
            console.print(summary_table)
            console.print()
            
            # Techniques breakdown
            tech_table = Table(title="[bold]Techniques Breakdown[/bold]", box=ROUNDED)
            tech_table.add_column("Technique", style="magenta")
            tech_table.add_column("Found", style="yellow")
            
            for technique, subdomains in self.results['techniques'].items():
                tech_table.add_row(technique.replace('_', ' ').title(), str(len(subdomains)))
            
            console.print(tech_table)
            console.print()
            
            # Subdomains list
            if self.subdomains:
                sub_table = Table(title="[bold]Discovered Subdomains[/bold]", box=ROUNDED)
                sub_table.add_column("No.", style="cyan", width=5)
                sub_table.add_column("Subdomain", style="green")
                sub_table.add_column("IP", style="yellow")
                
                for idx, subdomain in enumerate(sorted(self.subdomains), 1):
                    ip = verified.get(subdomain, "Not resolved") if verified else "Not checked"
                    sub_table.add_row(str(idx), subdomain, ip)
                
                console.print(sub_table)
        else:
            # Basic output
            print("\n" + "="*70)
            print(f"FINDOMAIN v2.0 - ENUMERATION SUMMARY FOR: {self.domain}")
            print("="*70)
            print(f"Total Subdomains Found: {len(self.subdomains)}")
            if verified:
                print(f"Verified Subdomains: {len(verified)}")
            print("="*70 + "\n")
            
            if self.subdomains:
                print("DISCOVERED SUBDOMAINS:")
                print("-"*70)
                for subdomain in sorted(self.subdomains):
                    if verified:
                        ip = verified.get(subdomain, "Not resolved")
                        print(f"  {subdomain:<40} | IP: {ip}")
                    else:
                        print(f"  {subdomain}")
            print("\n" + "="*70 + "\n")


def interactive_mode():
    """Interactive CLI mode"""
    print_header()
    
    while True:
        if RICH_AVAILABLE:
            domain = console.input("[bold cyan]Enter domain to enumerate[/bold cyan] (or 'quit' to exit): ").strip()
        else:
            domain = input("\n➤ Enter domain to enumerate (or 'quit' to exit): ").strip()
        
        if domain.lower() == 'quit':
            if RICH_AVAILABLE:
                console.print("[yellow]Goodbye![/yellow]")
            else:
                print("Goodbye!")
            sys.exit(0)
        
        if not domain:
            log_msg("Please enter a domain", "WARNING")
            continue
        
        if not validate_domain(domain):
            log_msg(f"Invalid domain format: {domain}", "ERROR")
            continue
        
        # Ask for verification
        if RICH_AVAILABLE:
            verify = console.input("\n[bold cyan]Verify DNS records?[/bold cyan] (y/n): ").strip().lower() == 'y'
        else:
            verify = input("\nVerify DNS records? (y/n): ").strip().lower() == 'y'
        
        # Run enumeration
        enumerator = Findomain(domain)
        subdomains = enumerator.enumerate_all()
        
        verified = None
        if verify:
            verified = enumerator.verify_subdomains()
        
        # Save results
        json_file, txt_file = enumerator.save_results()
        
        # Display results
        enumerator.display_results(verified)
        
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Results saved to:[/green]")
            console.print(f"  • {json_file}")
            console.print(f"  • {txt_file}\n")
        else:
            print(f"Results saved to:\n  • {json_file}\n  • {txt_file}\n")
        
        # Ask to continue
        if RICH_AVAILABLE:
            cont = console.input("[bold cyan]Enumerate another domain?[/bold cyan] (y/n): ").strip().lower() == 'y'
        else:
            cont = input("\nEnumerate another domain? (y/n): ").strip().lower() == 'y'
        
        if not cont:
            if RICH_AVAILABLE:
                console.print("[yellow]Goodbye![/yellow]")
            else:
                print("Goodbye!")
            break


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='findomain v2.0 - Advanced Subdomain Enumeration by bugxcve',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 findomain.py google.com
  python3 findomain.py example.com -v
  python3 findomain.py test.com --verify -o results
  python3 findomain.py                    (Interactive mode)
        '''
    )
    
    parser.add_argument('domain', nargs='?', help='Target domain (optional, use interactive mode if not provided)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('--verify', action='store_true', help='Verify DNS records')
    
    args = parser.parse_args()
    
    try:
        if not args.domain:
            # Interactive mode
            interactive_mode()
        else:
            # CLI mode
            print_header()
            
            if not validate_domain(args.domain):
                log_msg(f"Invalid domain format: {args.domain}", "ERROR")
                sys.exit(1)
            
            enumerator = Findomain(args.domain, args.verbose)
            subdomains = enumerator.enumerate_all()
            
            verified = None
            if args.verify:
                verified = enumerator.verify_subdomains()
            
            output_file = args.output or f"findomain_{args.domain}"
            json_file, txt_file = enumerator.save_results(output_file)
            
            enumerator.display_results(verified)
            
            if RICH_AVAILABLE:
                console.print(f"[green]✓ Results saved to:[/green]")
                console.print(f"  • {json_file}")
                console.print(f"  • {txt_file}\n")
            else:
                print(f"Results saved to:\n  • {json_file}\n  • {txt_file}\n")
            
    except KeyboardInterrupt:
        log_msg("\nEnumeration interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        log_msg(f"Fatal error: {str(e)}", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
