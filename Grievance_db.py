"""
Grievance Database Management
Handles storage and retrieval of grievances with SQLite
"""

import sqlite3
import pandas as pd
from datetime import datetime
import uuid
import json


class GrievanceDB:
    def __init__(self, db_path="mitra_grievances.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Grievances table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grievances (
                id TEXT PRIMARY KEY,
                erp_code TEXT NOT NULL,
                employee_name TEXT NOT NULL,
                branch TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                description TEXT NOT NULL,
                subject TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                admin_notes TEXT,
                attachment_metadata TEXT,
                shift_start_time TEXT,
                shift_end_time TEXT
            )
        """)
        
        # Grievance history table (for status tracking)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grievance_history (
                id TEXT PRIMARY KEY,
                grievance_id TEXT NOT NULL,
                status_from TEXT,
                status_to TEXT,
                changed_by TEXT,
                changed_at TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (grievance_id) REFERENCES grievances(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_grievance(self, erp_code, employee_name, branch, issue_type, 
                        description, subject, shift_start=None, shift_end=None):
        """Create a new grievance"""
        grievance_id = str(uuid.uuid4())[:12].upper()
        created_at = datetime.now()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO grievances 
            (id, erp_code, employee_name, branch, issue_type, description, 
             subject, created_at, updated_at, status, shift_start_time, shift_end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            grievance_id, erp_code, employee_name, branch, issue_type, 
            description, subject, created_at, created_at, 'pending',
            shift_start, shift_end
        ))
        
        # Add to history
        cursor.execute("""
            INSERT INTO grievance_history 
            (id, grievance_id, status_from, status_to, changed_by, changed_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            grievance_id,
            None,
            'pending',
            erp_code,
            created_at,
            'Grievance created by employee'
        ))
        
        conn.commit()
        conn.close()
        
        return grievance_id
    
    def get_grievance(self, grievance_id):
        """Get a specific grievance by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM grievances WHERE id = ?", (grievance_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_employee_grievances(self, erp_code):
        """Get all grievances for an employee"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM grievances WHERE erp_code = ? ORDER BY created_at DESC",
            (erp_code,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_all_grievances(self):
        """Get all grievances (for admin)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM grievances ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def update_grievance_status(self, grievance_id, new_status, admin_erp, admin_notes=""):
        """Update grievance status by admin"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute("SELECT status FROM grievances WHERE id = ?", (grievance_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
        
        current_status = result[0]
        updated_at = datetime.now()
        
        # Update grievance
        cursor.execute("""
            UPDATE grievances 
            SET status = ?, updated_at = ?, admin_notes = ?
            WHERE id = ?
        """, (new_status, updated_at, admin_notes, grievance_id))
        
        # Add to history
        cursor.execute("""
            INSERT INTO grievance_history 
            (id, grievance_id, status_from, status_to, changed_by, changed_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            grievance_id,
            current_status,
            new_status,
            admin_erp,
            updated_at,
            admin_notes
        ))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_grievance_history(self, grievance_id):
        """Get history of a grievance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM grievance_history WHERE grievance_id = ? ORDER BY changed_at",
            (grievance_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [self._history_row_to_dict(row) for row in rows]
    
    def get_grievances_by_type(self, issue_type):
        """Get grievances by type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM grievances WHERE issue_type = ? ORDER BY created_at DESC",
            (issue_type,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_grievances_by_status(self, status):
        """Get grievances by status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM grievances WHERE status = ? ORDER BY created_at DESC",
            (status,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_statistics(self):
        """Get grievance statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total grievances
        cursor.execute("SELECT COUNT(*) FROM grievances")
        stats['total'] = cursor.fetchone()[0]
        
        # By status
        cursor.execute("SELECT status, COUNT(*) FROM grievances GROUP BY status")
        stats['by_status'] = dict(cursor.fetchall())
        
        # By issue type
        cursor.execute("SELECT issue_type, COUNT(*) FROM grievances GROUP BY issue_type")
        stats['by_type'] = dict(cursor.fetchall())
        
        # By branch
        cursor.execute("SELECT branch, COUNT(*) FROM grievances GROUP BY branch")
        stats['by_branch'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def _row_to_dict(self, row):
        """Convert database row to dictionary"""
        return {
            'id': row[0],
            'erp_code': row[1],
            'employee_name': row[2],
            'branch': row[3],
            'issue_type': row[4],
            'description': row[5],
            'subject': row[6],
            'created_at': row[7],
            'updated_at': row[8],
            'status': row[9],
            'admin_notes': row[10],
            'attachment_metadata': row[11],
            'shift_start_time': row[12],
            'shift_end_time': row[13],
        }
    
    def _history_row_to_dict(self, row):
        """Convert history row to dictionary"""
        return {
            'id': row[0],
            'grievance_id': row[1],
            'status_from': row[2],
            'status_to': row[3],
            'changed_by': row[4],
            'changed_at': row[5],
            'notes': row[6],
        }
    
    def export_to_dataframe(self):
        """Export all grievances to pandas DataFrame"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM grievances", conn)
        conn.close()
        return df


# Global instance
_db = None

def get_db():
    """Get database instance"""
    global _db
    if _db is None:
        _db = GrievanceDB()
    return _db