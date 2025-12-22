import sqlite3
from datetime import datetime

class JobTracker:
    def __init__(self, db_path=r"C:\Users\hp\Documents\python\Jon tracker\job_tracker.db"):
        self.conn = sqlite3.connect(db_path)
        self.cr = self.conn.cursor()
        self.load_applications()

    def load_applications(self):
        """Cache applications for quick listing"""
        self.cr.execute("SELECT * FROM applications")
        self.applications = self.cr.fetchall()

    def commit_close(self):
        self.conn.commit()
        self.conn.close()
        print("🔌 Database connection closed")

    def show_all_applications(self):
        print("\n📋 ALL APPLICATIONS:")
        for i, row in enumerate(self.applications, 1):
            print(f"[{i}] ID:{row[0]} | {row[1]} | {row[3]}@{row[2]} | {row[4]} | {row[5]} | {row[6]}")
        return len(self.applications)

    def show_application(self, app_id):
        self.cr.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
        result = self.cr.fetchone()
        if result:
            print(f"\n📄 Application {app_id}: {result[1]} | {result[3]}@{result[2]} | Status: {result[6]}")
            return result
        print(f"❌ No application with ID {app_id}")
        return None

    def add_application(self):
        print("\n➕ ADD NEW APPLICATION")
        company = input("Company: ").strip()
        role = input("Role: ").strip()
        country = input("Country: ").strip()
        source = input("Source: ").strip()
        status = input("Status (applied/interview/offer/rejected): ").strip().lower()
        salary = input("Salary (or Enter): ").strip() or None
        tech_stack = input("Tech stack (comma-separated): ").strip()
        notes = input("Notes: ").strip()

        now = datetime.now().strftime("%Y-%m-%d")

        self.cr.execute("""
            INSERT INTO applications (date_applied, company, role, country, source, status, salary, tech_stack, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, company, role, country, source, status, salary, tech_stack, notes))

        self.conn.commit()
        self.load_applications()
        print("✅ Application added!")

    def update_status(self, app_id):
        app = self.show_application(app_id)
        if not app: return

        status = input("New status (applied/interview/offer/rejected): ").strip().lower()
        if status in ['applied', 'interview', 'offer', 'rejected']:
            self.cr.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
            self.conn.commit()
            self.load_applications()
            print(f"✅ Status updated to '{status}'")
        else:
            print("❌ Invalid status")

    def delete_application(self, app_id):
        confirm = input(f"Delete application {app_id}? (y/N): ").strip().lower()
        if confirm == 'y':
            self.cr.execute("DELETE FROM applications WHERE id = ?", (app_id,))
            self.conn.commit()
            self.load_applications()
            print("✅ Application deleted")

# MAIN RUNNER
if __name__ == "__main__":
    tracker = JobTracker()
    print("=== Job Tracker CLI ===")
    tracker.show_all_applications()

    while True:
        print("\n1. View all | 2. Add app | 3. Update status | 4. Delete | 5. Quit")
        choice = input("Choose: ").strip()

        if choice == '1':
            tracker.show_all_applications()
        elif choice == '2':
            tracker.add_application()
        elif choice == '3':
            app_id = input("App ID: ")
            tracker.update_status(app_id)
        elif choice == '4':
            app_id = input("App ID: ")
            tracker.delete_application(app_id)
        elif choice == '5':
            break

    tracker.commit_close()
