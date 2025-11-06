#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GUI application for building and serving the Pelican blog.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import io
import time
from contextlib import redirect_stdout, redirect_stderr
from build import build_site, rebuild_site, ServerManager, clean_site


class BuildGUI:
    """GUI application for managing Pelican blog builds."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pelican Blog Builder")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Server manager
        self.server_manager = None
        self.is_building = False
        
        # Create UI
        self.create_widgets()
        
        # Check for Pelican
        self.check_pelican()
        
        # Start periodic status check
        self.check_status()
    
    def check_pelican(self):
        """Check if Pelican is installed."""
        try:
            import pelican
            self.log("✓ Pelican is installed")
        except ImportError:
            self.log("✗ Pelican is not installed. Please install dependencies:")
            self.log("  pip install -r requirements.txt")
            messagebox.showerror(
                "Pelican Not Found",
                "Pelican is not installed.\n\n"
                "Please install dependencies:\n"
                "pip install -r requirements.txt"
            )
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        self.build_button = ttk.Button(
            button_frame,
            text="Build",
            command=self.on_build,
            width=12
        )
        self.build_button.grid(row=0, column=0, padx=5)
        
        self.rebuild_button = ttk.Button(
            button_frame,
            text="Rebuild",
            command=self.on_rebuild,
            width=12
        )
        self.rebuild_button.grid(row=0, column=1, padx=5)
        
        self.serve_button = ttk.Button(
            button_frame,
            text="Serve",
            command=self.on_serve,
            width=12
        )
        self.serve_button.grid(row=0, column=2, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            command=self.on_stop,
            width=12,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=3, padx=5)
        
        self.refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=self.on_refresh,
            width=12,
            state=tk.DISABLED
        )
        self.refresh_button.grid(row=0, column=4, padx=5)
        
        self.exit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=self.on_exit,
            width=12
        )
        self.exit_button.grid(row=0, column=5, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            font=("Arial", 10, "bold")
        )
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Log output area
        log_frame = ttk.LabelFrame(main_frame, text="Output", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Server info label
        self.server_info_label = ttk.Label(
            main_frame,
            text="",
            font=("Arial", 9)
        )
        self.server_info_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)
    
    def _safe_ui_update(self, func):
        """Safely update UI from background thread."""
        try:
            if hasattr(self, 'root') and self.root:
                try:
                    if self.root.winfo_exists():
                        self.root.after(0, func)
                except (tk.TclError, RuntimeError, AttributeError):
                    # Window is being destroyed or doesn't exist
                    pass
        except (AttributeError, RuntimeError):
            # Object is being destroyed
            pass
    
    def _clear_server_info(self):
        """Safely clear server info label."""
        try:
            if hasattr(self, 'server_info_label') and self.server_info_label:
                self.server_info_label.config(text="")
        except (tk.TclError, RuntimeError, AttributeError):
            pass
    
    def log(self, message):
        """Add a message to the log output (thread-safe)."""
        # Use safe UI update to ensure UI updates happen in main thread
        self._safe_ui_update(lambda: self._log_impl(message))
    
    def _log_impl(self, message):
        """Internal log implementation (called in main thread)."""
        try:
            if self.log_text and self.root.winfo_exists():
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
                self.root.update_idletasks()
        except:
            pass  # Widget might be destroyed
    
    def set_status(self, status):
        """Update the status label (thread-safe)."""
        # Use safe UI update to ensure UI updates happen in main thread
        self._safe_ui_update(lambda: self.status_label.config(text=status))
    
    def update_button_states(self):
        """Update button states based on current status."""
        server_running = self.server_manager and self.server_manager.is_server_running()
        
        if self.is_building:
            self.build_button.config(state=tk.DISABLED)
            self.rebuild_button.config(state=tk.DISABLED)
            self.serve_button.config(state=tk.DISABLED)
            self.refresh_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
        else:
            self.build_button.config(state=tk.NORMAL)
            self.rebuild_button.config(state=tk.NORMAL)
            
            if server_running:
                self.serve_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.refresh_button.config(state=tk.NORMAL)
            else:
                self.serve_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.refresh_button.config(state=tk.DISABLED)
    
    def run_in_thread(self, func, *args, **kwargs):
        """Run a function in a separate thread."""
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
    
    def on_build(self):
        """Handle Build button click."""
        if self.is_building:
            return
        
        self.is_building = True
        self.update_button_states()
        self.set_status("Building...")
        self.log("\n" + "="*60)
        self.log("Building site (development mode)")
        self.log("="*60)
        
        def build():
            try:
                # Capture output
                output = io.StringIO()
                with redirect_stdout(output), redirect_stderr(output):
                    success = build_site(production=False)
                
                output_text = output.getvalue()
                if output_text:
                    self.log(output_text)
                
                if success:
                    self.log("\n✓ Site built successfully!")
                    self.set_status("Build complete")
                else:
                    self.log("\n✗ Build failed")
                    self.set_status("Build failed")
                    self._safe_ui_update(lambda: messagebox.showerror("Build Failed", "The build process failed. Check the output for details."))
            except Exception as e:
                import traceback
                error_msg = f"{e}\n{traceback.format_exc()}"
                self.log(f"\n✗ Error: {error_msg}")
                self.set_status("Build error")
                self._safe_ui_update(lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
            finally:
                self.is_building = False
                self._safe_ui_update(self.update_button_states)
        
        self.run_in_thread(build)
    
    def on_rebuild(self):
        """Handle Rebuild button click."""
        if self.is_building:
            return
        
        self.is_building = True
        self.update_button_states()
        self.set_status("Rebuilding...")
        self.log("\n" + "="*60)
        self.log("Rebuilding site")
        self.log("="*60)
        
        def rebuild():
            try:
                # Capture output
                output = io.StringIO()
                with redirect_stdout(output), redirect_stderr(output):
                    success = rebuild_site(production=False)
                
                output_text = output.getvalue()
                if output_text:
                    self.log(output_text)
                
                if success:
                    self.log("\n✓ Rebuild complete!")
                    self.set_status("Rebuild complete")
                else:
                    self.log("\n✗ Rebuild failed")
                    self.set_status("Rebuild failed")
                    self._safe_ui_update(lambda: messagebox.showerror("Rebuild Failed", "The rebuild process failed. Check the output for details."))
            except Exception as e:
                import traceback
                error_msg = f"{e}\n{traceback.format_exc()}"
                self.log(f"\n✗ Error: {error_msg}")
                self.set_status("Rebuild error")
                self._safe_ui_update(lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
            finally:
                self.is_building = False
                self._safe_ui_update(self.update_button_states)
        
        self.run_in_thread(rebuild)
    
    def on_serve(self):
        """Handle Serve button click."""
        if self.server_manager and self.server_manager.is_server_running():
            return
        
        self.set_status("Starting server...")
        self.log("\n" + "="*60)
        self.log("Starting server...")
        self.log("="*60)
        
        def start_server():
            try:
                if not self.server_manager:
                    self.server_manager = ServerManager(
                        port=8000,
                        production=False,
                        log_callback=self.log
                    )
                
                if self.server_manager.start():
                    self.set_status("Server running")
                    self._safe_ui_update(lambda: self.server_info_label.config(
                        text=f"Server running at http://localhost:8000"
                    ))
                else:
                    self.set_status("Server failed to start")
                    self._safe_ui_update(lambda: messagebox.showerror("Server Error", "Failed to start the server. Check the output for details."))
            except Exception as e:
                import traceback
                error_msg = f"{e}\n{traceback.format_exc()}"
                self.log(f"\n✗ Error: {error_msg}")
                self.set_status("Server error")
                self._safe_ui_update(lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
            finally:
                self._safe_ui_update(self.update_button_states)
        
        self.run_in_thread(start_server)
        self.update_button_states()
    
    def on_stop(self):
        """Handle Stop button click."""
        try:
            if not self.server_manager:
                return
            
            # Check if running (with error handling)
            try:
                if not self.server_manager.is_server_running():
                    return
            except Exception:
                # If check fails, try to stop anyway
                pass
            
            self.set_status("Stopping server...")
            self.log("\nStopping server...")
            
            def stop_server():
                try:
                    server_stopped = False
                    if self.server_manager:
                        try:
                            # Stop without logging from server thread
                            self.server_manager.stop()
                            server_stopped = True
                        except Exception as e:
                            import traceback
                            error_msg = f"{e}\n{traceback.format_exc()}"
                            # Only log if we can safely do so
                            try:
                                self.log(f"⚠ Error during server stop: {error_msg}")
                            except:
                                pass
                    
                    if server_stopped:
                        self.set_status("Server stopped")
                        self._safe_ui_update(lambda: self._clear_server_info())
                        try:
                            self.log("✓ Server stopped")
                        except:
                            pass
                    else:
                        self.set_status("Server stop may have failed")
                        try:
                            self.log("⚠ Server stop may have failed")
                        except:
                            pass
                except Exception as e:
                    import traceback
                    error_msg = f"{e}\n{traceback.format_exc()}"
                    try:
                        self.log(f"\n✗ Unexpected error stopping server: {error_msg}")
                    except:
                        pass
                    try:
                        self.set_status("Error")
                    except:
                        pass
                finally:
                    try:
                        self._safe_ui_update(self.update_button_states)
                    except:
                        pass
            
            self.run_in_thread(stop_server)
            self.update_button_states()
        except Exception as e:
            # Last resort error handling
            import traceback
            try:
                print(f"Error in on_stop: {e}\n{traceback.format_exc()}")
            except:
                pass
    
    def on_refresh(self):
        """Handle Refresh button click - stops, rebuilds, and serves."""
        if not self.server_manager or not self.server_manager.is_server_running():
            messagebox.showwarning("Not Running", "Server is not running. Use 'Serve' to start it.")
            return
        
        if self.is_building:
            return
        
        self.is_building = True
        self.update_button_states()
        self.set_status("Refreshing...")
        self.log("\n" + "="*60)
        self.log("Refreshing: Stopping, rebuilding, and restarting server...")
        self.log("="*60)
        
        def refresh():
            try:
                # Stop server
                self.log("\nStopping server...")
                server_stopped = False
                if self.server_manager:
                    try:
                        self.server_manager.stop()
                        server_stopped = True
                        # Give it a moment to fully stop and release port
                        time.sleep(1.0)
                    except Exception as e:
                        self.log(f"⚠ Error stopping server: {e}")
                
                if server_stopped:
                    self.log("✓ Server stopped")
                else:
                    self.log("⚠ Server stop may have failed")
                
                # Rebuild
                self.log("\nRebuilding site...")
                rebuild_success = False
                try:
                    output = io.StringIO()
                    with redirect_stdout(output), redirect_stderr(output):
                        rebuild_success = rebuild_site(production=False)
                    
                    output_text = output.getvalue()
                    if output_text:
                        self.log(output_text)
                except Exception as e:
                    import traceback
                    error_msg = f"{e}\n{traceback.format_exc()}"
                    self.log(f"\n✗ Rebuild exception: {error_msg}")
                    rebuild_success = False
                
                if not rebuild_success:
                    self.log("\n✗ Rebuild failed")
                    self.set_status("Refresh failed")
                    self._safe_ui_update(lambda: messagebox.showerror("Refresh Failed", "The rebuild process failed. Check the output for details."))
                    return
                
                self.log("\n✓ Rebuild complete!")
                
                # Restart server - make sure server_manager still exists
                if not self.server_manager:
                    try:
                        self.server_manager = ServerManager(
                            port=8000,
                            production=False,
                            log_callback=self.log
                        )
                    except Exception as e:
                        self.log(f"✗ Failed to create server manager: {e}")
                        self.set_status("Refresh failed")
                        return
                
                # Verify server_manager is still valid
                if not self.server_manager:
                    self.log("✗ Server manager is not available")
                    self.set_status("Refresh failed")
                    return
                
                self.log("\nRestarting server...")
                # Additional small delay to ensure port is fully released
                time.sleep(0.5)
                
                server_started = False
                try:
                    if self.server_manager:
                        server_started = self.server_manager.start()
                    else:
                        self.log("✗ Server manager became unavailable")
                except Exception as e:
                    import traceback
                    error_msg = f"{e}\n{traceback.format_exc()}"
                    self.log(f"\n✗ Server start exception: {error_msg}")
                    server_started = False
                
                if server_started:
                    self.log("✓ Server restarted")
                    self.set_status("Refresh complete - Server running")
                    self._safe_ui_update(lambda: self.server_info_label.config(
                        text=f"Server running at http://localhost:8000"
                    ))
                else:
                    self.log("\n✗ Failed to restart server")
                    self.set_status("Refresh failed - Server not started")
                    self._safe_ui_update(lambda: messagebox.showerror("Server Error", "Failed to restart the server. Check the output for details."))
            except Exception as e:
                import traceback
                error_msg = f"{e}\n{traceback.format_exc()}"
                self.log(f"\n✗ Unexpected error: {error_msg}")
                self.set_status("Refresh error")
                self._safe_ui_update(lambda: messagebox.showerror("Error", f"An unexpected error occurred: {e}"))
            finally:
                self.is_building = False
                self._safe_ui_update(self.update_button_states)
        
        self.run_in_thread(refresh)
    
    def check_status(self):
        """Periodically check server status and update UI."""
        if self.server_manager:
            if not self.server_manager.is_server_running() and self.server_info_label.cget("text"):
                # Server stopped unexpectedly
                self.server_info_label.config(text="")
                self.set_status("Server stopped")
                self.log("\n⚠ Server stopped unexpectedly")
        
        self.update_button_states()
        
        # Schedule next check
        self.root.after(1000, self.check_status)
    
    def on_exit(self):
        """Handle Exit button click."""
        if self.server_manager and self.server_manager.is_server_running():
            if messagebox.askyesno("Server Running", "Server is currently running. Stop it and exit?"):
                self.server_manager.stop()
                self.root.quit()
        else:
            self.root.quit()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = BuildGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

