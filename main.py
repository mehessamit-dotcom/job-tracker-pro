#!/usr/bin/env python3
"""
Job Tracker Pro - Main CLI Application
Combines data management + analytics in one professional interface
"""

from models import JobTracker
import pandas as pd
from Analysis import df_functions
import os

def print_header():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                  🚀 JOB TRACKER PRO 🚀                      ║
║     Track applications + Analyze conversion rates           ║
╚══════════════════════════════════════════════════════════════╝
    """)

def print_menu():
    print("""
📋 1. Show All Applications
📄 2. View Specific Application
➕ 3. Add New Application
🔄 4. Update Status
🗑️  5. Delete Application
📊 6. Run Full Analysis
📈 7. Conversion Funnel (Sources)
🗺️  8. Best Countries for Interviews
💰 9. Salary Trends
📅 10. Monthly Trends
❌ Q. Quit
    """)

def run_analysis_menu(tracker):
    """Quick analysis submenu"""
    df = pd.read_sql_query("SELECT * FROM applications", tracker.conn)
    df['date_applied'] = pd.to_datetime(df['date_applied'])
    analyzer = df_functions(df)

    print("\n📊 ANALYSIS RESULTS:")
    print(analyzer.Response_rate_all_source('source', ['interview', 'offer']))
    print("\n💰 Salary Trends:")
    print(analyzer.salary_per_role())
    print("\n✅ Check 'reports/' for charts!")

    analyzer.plot_conversion_funnel('source')

def main():
    print_header()
    tracker = JobTracker()

    while True:
        print_menu()
        choice = input("Choose option: ").strip().upper()

        if choice == '1':
            tracker.show_all_applications()
        elif choice == '2':
            app_id = input("Enter App ID: ").strip()
            tracker.show_application(app_id)
        elif choice == '3':
            tracker.add_application()
        elif choice == '4':
            app_id = input("Enter App ID: ").strip()
            tracker.update_status(app_id)
        elif choice == '5':
            app_id = input("Enter App ID to delete: ").strip()
            tracker.delete_application(app_id)
        elif choice == '6':
            run_analysis_menu(tracker)
        elif choice == '7':
            df = pd.read_sql_query("SELECT * FROM applications", tracker.conn)
            df['date_applied'] = pd.to_datetime(df['date_applied'])
            analyzer = df_functions(df)
            print("\n📈 Conversion Funnel by Source:")
            print(analyzer.Response_rate_all_source('source', ['interview']))
        elif choice == '8':
            df = pd.read_sql_query("SELECT * FROM applications", tracker.conn)
            df['date_applied'] = pd.to_datetime(df['date_applied'])
            analyzer = df_functions(df)
            analyzer.best_country_for_interviews('country')
        elif choice == '9':
            df = pd.read_sql_query("SELECT * FROM applications", tracker.conn)
            df['date_applied'] = pd.to_datetime(df['date_applied'])
            analyzer = df_functions(df)
            print("\n💰 Salary Trends by Role:")
            print(analyzer.salary_per_role())
        elif choice == '10':
            df = pd.read_sql_query("SELECT * FROM applications", tracker.conn)
            df['date_applied'] = pd.to_datetime(df['date_applied'])
            analyzer = df_functions(df)
            analyzer.application_per_month()
        elif choice == 'Q':
            print("👋 Thanks for using Job Tracker Pro!")
            break
        else:
            print("❌ Invalid option. Try again.")

        input("\nPress Enter to continue...")

    tracker.commit_close()

if __name__ == "__main__":
    main()