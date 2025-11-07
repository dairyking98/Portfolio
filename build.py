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


def serve_site(port=8000, production=False, interactive_mode=False, quit_event=None, listen=False):
    """Serve the site locally with a clean Ctrl+C exit.

    Note: listen is ignored in this implementation to preserve reliable stop behavior.
    """
    output_path = Path('output')
    if not output_path.exists():
        print("✗ Output directory not found. Building site first...")
        if not build_site(production=production):
            return False

    print(f"\n{'='*60}")
    print(f"Serving site at http://localhost:{port}")
    if listen:
        print("(Auto-rebuild disabled temporarily; press Ctrl+C to stop, then rebuild)")
    print("Press Ctrl+C to stop the server")
    if interactive_mode:
        print("(Returning to menu after stop)")
    print(f"{'='*60}\n")

    import http.server
    import socketserver
    import socket

    original_dir = os.getcwd()

    # Helper: directory snapshot for polling
    def get_primary_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        except Exception:
            return '127.0.0.1'
        finally:
            try:
                s.close()
            except Exception:
                pass

    lan_ip = get_primary_ip()
    def snapshot_content_dir() -> dict:
        content_root = Path('content')
        file_to_mtime = {}
        if not content_root.exists():
            return file_to_mtime
        for root, dirs, files in os.walk(content_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            for name in files:
                if name.startswith('.') or name.endswith('.pyc'):
                    continue
                p = Path(root) / name
                try:
                    file_to_mtime[p] = p.stat().st_mtime
                except (OSError, FileNotFoundError):
                    pass
        return file_to_mtime

    # If not listening, run the simple, robust server once
    if not listen:
        try:
            os.chdir('output')
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("0.0.0.0", port), handler)
            print("Server running...\n")
            print(f"  Local  : http://127.0.0.1:{port}")
            print(f"  Network: http://{lan_ip}:{port}\n")

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n✓ Stopping server...")
            finally:
                try:
                    httpd.shutdown()
                except Exception:
                    pass
                try:
                    httpd.server_close()
                except Exception:
                    pass
                os.chdir(original_dir)
                print("✓ Server stopped cleanly")

            return True

        except OSError as e:
            os.chdir(original_dir)
            if e.errno == 98 or e.errno == 48:  # Address already in use
                print(f"✗ Port {port} is already in use. Try a different port:")
                print(f"  python build.py serve --port {port + 1}")
            else:
                print(f"✗ Error: {e}")
            return False
        except Exception as e:
            os.chdir(original_dir)
            print(f"✗ Error: {e}")
            return False

    # Listen mode: poll for changes in a background thread and restart cleanly
    try:
        prev_snapshot = snapshot_content_dir()
        while True:
            restart_requested = threading.Event()

            # Start HTTP server
            os.chdir('output')
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("0.0.0.0", port), handler)
            print("Server running (listening for changes)...\n")
            print(f"  Local  : http://127.0.0.1:{port}")
            print(f"  Network: http://{lan_ip}:{port}\n")

            # Watcher thread (daemon), polling without touching stdin
            def watcher():
                nonlocal prev_snapshot
                try:
                    while True:
                        time.sleep(1.0)
                        new_snapshot = snapshot_content_dir()
                        if new_snapshot != prev_snapshot:
                            print("\n🔄 Change detected in content. Scheduling rebuild...")
                            prev_snapshot = new_snapshot
                            restart_requested.set()
                            try:
                                httpd.shutdown()  # Thread-safe; wakes serve_forever
                            except Exception:
                                pass
                            break
                except Exception:
                    # Silent watcher errors
                    pass

            t = threading.Thread(target=watcher, daemon=True)
            t.start()

            try:
                httpd.serve_forever(poll_interval=0.5)
            except KeyboardInterrupt:
                print("\n✓ Stopping server...")
                # Clean stop requested by user; stop listening loop
                try:
                    httpd.shutdown()
                except Exception:
                    pass
                try:
                    httpd.server_close()
                except Exception:
                    pass
                os.chdir(original_dir)
                print("✓ Server stopped cleanly")
                return True
            finally:
                # Ensure server closed before rebuild/restart
                try:
                    httpd.server_close()
                except Exception:
                    pass
                os.chdir(original_dir)

            # If restart requested, rebuild then loop to restart the server
            if restart_requested.is_set():
                print("🔧 Rebuilding site...")
                if not rebuild_site(production=production):
                    print("✗ Rebuild failed. Not restarting server.")
                    return False
                print("✓ Rebuild complete. Restarting server...\n")
                continue

            # Otherwise, serve_forever ended without restart or Ctrl+C; exit
            print("✓ Server stopped cleanly")
            return True

    except OSError as e:
        os.chdir(original_dir)
        if e.errno == 98 or e.errno == 48:
            print(f"✗ Port {port} is already in use. Try a different port:")
            print(f"  python build.py serve --port {port + 1}")
        else:
            print(f"✗ Error: {e}")
        return False
    except Exception as e:
        os.chdir(original_dir)
        print(f"✗ Error: {e}")
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


def interactive_mode(port=8000, production=False):
    """Run interactive mode with menu-driven commands."""
    # Check if Pelican is installed
    try:
        import pelican
    except ImportError:
        print("✗ Pelican is not installed.")
        print("  Please install dependencies:")
        print("  pip install -r requirements.txt")
        return False
    
    quit_program = threading.Event()
    
    def print_menu():
        """Print the interactive menu."""
        print("\n" + "="*60)
        print("Pelican Blog Manager - Interactive Mode")
        print("="*60)
        print("Commands:")
        print("  b - Build site")
        print("  r - Rebuild site (clean + build)")
        print("  s - Serve site")
        print("  l - Serve site with auto-rebuild (watch for changes)")
        print("  e - Exit interactive mode")
        print("  q - Quit program")
        print("="*60)
        print("Enter command: ", end='', flush=True)
    
    print_menu()
    
    while not quit_program.is_set():
        try:
            # Use blocking input for menu (more user-friendly)
            try:
                cmd = input().strip().lower()
            except (EOFError, KeyboardInterrupt):
                cmd = 'q'
            
            if not cmd:
                continue
            
            cmd = cmd[0] if len(cmd) > 0 else ''
            
            if cmd == 'b':
                print("\n🔄 Building site...")
                if build_site(production=production):
                    print("\n✓ Build completed successfully!")
                else:
                    print("\n✗ Build failed!")
                print_menu()
            
            elif cmd == 'r':
                print("\n🔄 Rebuilding site...")
                if rebuild_site(production=production):
                    print("\n✓ Rebuild completed successfully!")
                else:
                    print("\n✗ Rebuild failed!")
                print_menu()
            
            elif cmd == 's':
                print("\n🌐 Starting server...")
                if serve_site(port=port, production=production, interactive_mode=True, quit_event=quit_program, listen=False):
                    print("\n✓ Server stopped.")
                else:
                    print("\n✗ Server error occurred.")
                if quit_program.is_set():
                    break
                # Server stopped cleanly, return to menu
                print_menu()
            
            elif cmd == 'l':
                print("\n🌐 Starting server with auto-rebuild (watching for changes)...")
                if serve_site(port=port, production=production, interactive_mode=True, quit_event=quit_program, listen=True):
                    print("\n✓ Server stopped.")
                else:
                    print("\n✗ Server error occurred.")
                if quit_program.is_set():
                    break
                # Server stopped cleanly, return to menu
                print_menu()
            
            elif cmd == 'e':
                print("\n✓ Exiting interactive mode...")
                break
            
            elif cmd == 'q':
                print("\n✓ Quitting program...")
                quit_program.set()
                break
            
            else:
                print(f"\n✗ Unknown command: {cmd}")
                print_menu()
        
        except KeyboardInterrupt:
            print("\n\n✓ Exiting...")
            quit_program.set()
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print_menu()
    
    return True


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
  python build.py serve --listen # Serve with auto-rebuild on file changes
  python build.py clean          # Clean output directory
  python build.py rebuild        # Clean and rebuild
  python build.py                # Start interactive mode
        """
    )
    
    parser.add_argument(
        'action',
        nargs='?',
        choices=['build', 'serve', 'clean', 'rebuild'],
        help='Action to perform (omit for interactive mode)'
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
    
    parser.add_argument(
        '--listen',
        action='store_true',
        help='Watch for file changes and auto-rebuild (only for serve action)'
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
    
    # If no action specified, start interactive mode
    if args.action is None:
        success = interactive_mode(port=args.port, production=args.prod)
        sys.exit(0 if success else 1)
    
    # Execute the requested action
    success = False
    
    if args.action == 'build':
        success = build_site(production=args.prod)
    elif args.action == 'serve':
        success = serve_site(port=args.port, production=args.prod, interactive_mode=False, listen=args.listen)
    elif args.action == 'clean':
        success = clean_site()
    elif args.action == 'rebuild':
        success = rebuild_site(production=args.prod)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

