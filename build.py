#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build script for Pelican blog.
Handles building, serving, and cleaning the site.
"""

import os
import sys
import argparse
import subprocess
import threading
import time
from pathlib import Path


def run_command(command, description, capture_output=False):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        else:
            result = subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {description} failed with exit code {e.returncode}")
        if capture_output and e.stdout:
            print(e.stdout)
        if capture_output and e.stderr:
            print(e.stderr, file=sys.stderr)
        return False


def build_site(production=False):
    """Build the Pelican site."""
    config_file = 'publishconf.py' if production else 'pelicanconf.py'
    command = f'pelican content -s {config_file} -o output'
    
    if not run_command(command, f"Building site ({'production' if production else 'development'} mode)"):
        return False
    
    print("\n✓ Site built successfully!")
    print(f"  Output directory: {os.path.abspath('output')}")
    return True


def serve_site(port=8000, production=False):
    """Serve the site locally for preview with interactive rebuild support."""
    output_path = Path('output')
    if not output_path.exists():
        print("✗ Output directory not found. Building site first...")
        if not build_site(production=production):
            return False
    
    print(f"\n{'='*60}")
    print(f"Serving site at http://localhost:{port}")
    if sys.platform == 'win32':
        print(f"Press 'r' (or 'r' + Enter) to rebuild and restart")
    else:
        print(f"Press 'r' + Enter to rebuild and restart")
    print(f"Press Ctrl+C to stop the server")
    print(f"{'='*60}\n")
    
    import http.server
    import socketserver
    
    httpd = None
    server_thread = None
    should_stop = threading.Event()
    rebuild_requested = threading.Event()
    
    def run_server():
        """Run the HTTP server in a separate thread."""
        nonlocal httpd
        try:
            original_dir = os.getcwd()
            os.chdir('output')
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("", port), handler)
            httpd.timeout = 1  # Allow periodic checks for shutdown
            print(f"Server started at http://localhost:{port}\n")
            
            while not should_stop.is_set():
                httpd.handle_request()
            
            httpd.server_close()
            os.chdir(original_dir)
        except OSError as e:
            if e.errno == 98 or e.errno == 48:  # Address already in use
                print(f"✗ Port {port} is already in use. Try a different port:")
                print(f"  python build.py serve --port {port + 1}")
            else:
                print(f"✗ Error starting server: {e}")
            should_stop.set()
        except Exception as e:
            print(f"✗ Server error: {e}")
            should_stop.set()
    
    def input_handler():
        """Handle user input in a separate thread."""
        while not should_stop.is_set():
            try:
                # On Windows, use non-blocking key detection
                if sys.platform == 'win32':
                    try:
                        import msvcrt
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            try:
                                if isinstance(key, bytes):
                                    key = key.decode('utf-8', errors='ignore')
                                key = key.lower()
                                if key == 'r':
                                    rebuild_requested.set()
                                    # Consume any remaining buffered input
                                    while msvcrt.kbhit():
                                        msvcrt.getch()
                            except (UnicodeDecodeError, AttributeError):
                                pass
                    except ImportError:
                        # Fallback: use blocking input (requires Enter)
                        try:
                            user_input = input().strip().lower()
                            if user_input == 'r':
                                rebuild_requested.set()
                        except (EOFError, KeyboardInterrupt):
                            should_stop.set()
                            break
                else:
                    # Unix-like: use select for non-blocking input check
                    try:
                        import select
                        if select.select([sys.stdin], [], [], 0.1)[0]:
                            user_input = sys.stdin.readline().strip().lower()
                            if user_input == 'r':
                                rebuild_requested.set()
                    except (ImportError, OSError):
                        # Fallback: use blocking input
                        try:
                            user_input = input().strip().lower()
                            if user_input == 'r':
                                rebuild_requested.set()
                        except (EOFError, KeyboardInterrupt):
                            should_stop.set()
                            break
            except Exception:
                pass
            time.sleep(0.1)
    
    try:
        # Start server in a daemon thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Start input handler in a separate thread
        input_thread = threading.Thread(target=input_handler, daemon=True)
        input_thread.start()
        
        # Wait a moment for server to start
        time.sleep(0.5)
        
        if should_stop.is_set():
            return False
        
        # Main loop: check for rebuild requests
        while True:
            try:
                # Check if server thread is still alive
                if not server_thread.is_alive():
                    break
                
                # Check if rebuild was requested
                if rebuild_requested.is_set():
                    rebuild_requested.clear()
                    print("\n\n🔄 Rebuilding site...")
                    
                    # Stop the server
                    should_stop.set()
                    if httpd:
                        try:
                            httpd.shutdown()
                        except:
                            pass
                    server_thread.join(timeout=2)
                    
                    # Rebuild
                    if rebuild_site(production=production):
                        print("\n✓ Rebuild complete! Restarting server...\n")
                        
                        # Reset and restart
                        should_stop = threading.Event()
                        rebuild_requested = threading.Event()
                        server_thread = threading.Thread(target=run_server, daemon=True)
                        server_thread.start()
                        time.sleep(0.5)
                    else:
                        print("\n✗ Rebuild failed. Server stopped.")
                        return False
                
                time.sleep(0.2)  # Small delay to prevent CPU spinning
                
            except KeyboardInterrupt:
                print("\n\n✓ Server stopped")
                should_stop.set()
                if httpd:
                    try:
                        httpd.shutdown()
                    except:
                        pass
                break
            except Exception as e:
                print(f"\n✗ Error: {e}")
                should_stop.set()
                if httpd:
                    try:
                        httpd.shutdown()
                    except:
                        pass
                break
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        should_stop.set()
        if httpd:
            try:
                httpd.shutdown()
            except:
                pass
        return False


def clean_site():
    """Clean the output directory."""
    output_path = Path('output')
    if output_path.exists():
        import shutil
        try:
            shutil.rmtree(output_path)
            print("✓ Output directory cleaned")
            return True
        except Exception as e:
            print(f"✗ Error cleaning output directory: {e}")
            return False
    else:
        print("✓ Output directory does not exist (nothing to clean)")
        return True


def rebuild_site(production=False):
    """Clean and rebuild the site."""
    print("\n" + "="*60)
    print("Rebuilding site")
    print("="*60)
    
    if not clean_site():
        return False
    
    return build_site(production=production)


class ServerManager:
    """Manages the HTTP server for GUI applications."""
    
    def __init__(self, port=8000, production=False, log_callback=None):
        self.port = port
        self.production = production
        self.log_callback = log_callback
        self.httpd = None
        self.server_thread = None
        self.should_stop = threading.Event()
        self.is_running = False
        self.original_dir = os.getcwd()
        self._lock = threading.Lock()  # Lock for thread-safe operations
    
    def _log(self, message):
        """Log a message via callback or print (thread-safe)."""
        try:
            if self.log_callback:
                self.log_callback(message)
            else:
                print(message)
        except Exception:
            # Silently ignore errors from log callback to prevent crashes
            pass
    
    def start(self):
        """Start the HTTP server in a separate thread (thread-safe)."""
        old_thread = None
        with self._lock:
            if self.is_running:
                self._log("Server is already running")
                return False
            
            # Make sure previous server is fully stopped
            if self.server_thread and self.server_thread.is_alive():
                self._log("Waiting for previous server to stop...")
                self.should_stop.set()
                if self.httpd:
                    try:
                        self.httpd.shutdown()
                    except:
                        pass
                old_thread = self.server_thread
        
        # Join outside lock to avoid deadlock
        if old_thread and old_thread.is_alive():
            old_thread.join(timeout=2)
        
        # Check output path and build if needed (outside lock)
        output_path = Path('output')
        if not output_path.exists():
            self._log("Output directory not found. Building site first...")
            if not build_site(production=self.production):
                return False
        
        # Reset state and start server (inside lock)
        with self._lock:
            # Reset state
            self.should_stop.clear()
            self.httpd = None
            self.server_thread = None
            
            # Start new server thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
        
        # Wait a moment for server to start (outside lock)
        time.sleep(0.5)
        
        with self._lock:
            if self.should_stop.is_set():
                return False
            
            # Verify server actually started
            if not self.server_thread.is_alive():
                return False
            
            self.is_running = True
        
        self._log(f"Server started at http://localhost:{self.port}")
        return True
    
    def _run_server(self):
        """Run the HTTP server in a separate thread."""
        try:
            os.chdir('output')
            import http.server
            import socketserver
            
            handler = http.server.SimpleHTTPRequestHandler
            self.httpd = socketserver.TCPServer(("", self.port), handler)
            self.httpd.timeout = 0.5  # Allow periodic checks for shutdown
            self.httpd.allow_reuse_address = True  # Allow port reuse
            
            while not self.should_stop.is_set():
                try:
                    self.httpd.handle_request()
                except Exception as e:
                    if not self.should_stop.is_set():
                        # Only log if we're not intentionally stopping
                        self._log(f"⚠ Server request error: {e}")
            
            if self.httpd:
                try:
                    self.httpd.server_close()
                except:
                    pass
            
            os.chdir(self.original_dir)
        except OSError as e:
            if e.errno == 98 or e.errno == 48:  # Address already in use
                self._log(f"✗ Port {self.port} is already in use")
            else:
                self._log(f"✗ Error starting server: {e}")
            self.should_stop.set()
            self.is_running = False
        except Exception as e:
            if not self.should_stop.is_set():
                self._log(f"✗ Server error: {e}")
            self.should_stop.set()
            self.is_running = False
        finally:
            try:
                os.chdir(self.original_dir)
            except:
                pass
            self.is_running = False
    
    def stop(self):
        """Stop the HTTP server (thread-safe)."""
        httpd_to_close = None
        thread_to_join = None
        old_log_callback = None
        
        with self._lock:
            if not self.is_running:
                return
            
            try:
                # Temporarily disable log callback to prevent crashes during shutdown
                old_log_callback = self.log_callback
                self.log_callback = None
                
                # Just set the flag - don't try to log during shutdown
                self.should_stop.set()
                
                # Get references
                httpd_to_close = self.httpd
                thread_to_join = self.server_thread
                
                # Mark as not running immediately
                self.is_running = False
                
            except Exception as e:
                # Ensure state is cleaned up even if there's an error
                self.is_running = False
                self.httpd = None
                self.log_callback = old_log_callback
        
        # Shutdown server outside lock
        if httpd_to_close:
            try:
                # Create a dummy request to wake up handle_request()
                import socket
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect(("localhost", self.port))
                    sock.close()
                except (socket.error, OSError, Exception):
                    # Connection failed, server might already be down
                    pass
                
                # Shutdown the server
                try:
                    httpd_to_close.shutdown()
                except (OSError, AttributeError, Exception):
                    # Server might already be closed or in invalid state
                    pass
            except Exception:
                # Ignore all errors during shutdown
                pass
        
        # Wait for thread outside the lock
        if thread_to_join and thread_to_join.is_alive():
            thread_to_join.join(timeout=2)  # Reduced timeout
        
        # Final cleanup
        with self._lock:
            try:
                if self.httpd:
                    try:
                        self.httpd.server_close()
                    except:
                        pass
            except:
                pass
            
            self.httpd = None
            # Restore log callback
            self.log_callback = old_log_callback
    
    def is_server_running(self):
        """Check if the server is currently running (thread-safe)."""
        try:
            with self._lock:
                return self.is_running and self.server_thread and self.server_thread.is_alive()
        except:
            return False


def main():
    """Main entry point for the build script."""
    parser = argparse.ArgumentParser(
        description='Build and manage Pelican blog',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py build          # Build site (development)
  python build.py build --prod   # Build site (production)
  python build.py serve          # Serve site locally
  python build.py clean          # Clean output directory
  python build.py rebuild        # Clean and rebuild
        """
    )
    
    parser.add_argument(
        'action',
        choices=['build', 'serve', 'clean', 'rebuild'],
        help='Action to perform'
    )
    
    parser.add_argument(
        '--prod',
        action='store_true',
        help='Use production configuration (publishconf.py)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port for local server (default: 8000)'
    )
    
    args = parser.parse_args()
    
    # Check if Pelican is installed
    try:
        import pelican
    except ImportError:
        print("✗ Pelican is not installed.")
        print("  Please install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Execute the requested action
    success = False
    
    if args.action == 'build':
        success = build_site(production=args.prod)
    elif args.action == 'serve':
        success = serve_site(port=args.port, production=args.prod)
    elif args.action == 'clean':
        success = clean_site()
    elif args.action == 'rebuild':
        success = rebuild_site(production=args.prod)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

