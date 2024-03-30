import random
import sqlite3
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()

def insert_organizations(cursor, n=10):
    for _ in range(n):
        cursor.execute(
            "INSERT INTO Organization (organization_name, organization_address) VALUES (?, ?)",
            (fake.company(), fake.address().replace('\n', ', '))
        )

def insert_researchers(cursor, n=20):
    cursor.execute("SELECT organization_id FROM Organization")
    organization_ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(n):
        org_id = random.choice(organization_ids)
        cursor.execute(
            "INSERT INTO Researcher (first_name, last_name, email, organization_id) VALUES (?, ?, ?, ?)",
            (fake.first_name(), fake.last_name(), fake.ascii_free_email(), org_id)
        )

def insert_competitions(cursor, n=10):
    for _ in range(n):
        deadline = (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')  # Format as string
        cursor.execute(
            "INSERT INTO Competition (competition_number, competition_title, competition_description, competition_area, competition_status, competition_deadline) VALUES (?, ?, ?, ?, ?, ?)",
            (random.randint(10000, 99999), fake.catch_phrase(), fake.paragraph(), fake.word(), random.choice(["Open", "Closed", "Review"]), deadline)
        )

def insert_proposals(cursor, n=15):
    cursor.execute("SELECT competition_id FROM Competition")
    competition_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT researcher_id FROM Researcher")
    researcher_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        amount = round(random.uniform(5000, 50000), 2)
        cursor.execute(
            "INSERT INTO Proposal (requested_amount, competition_id, principle_investigator_id, proposal_status, awarded_amount, awarded_date) VALUES (?, ?, ?, ?, ?, ?)",
            (amount, random.choice(competition_ids), random.choice(researcher_ids), "Submitted", amount if amount > 20000 and random.choice([True, False]) else None, datetime.now().date() if amount > 20000 else None)
        )

def insert_proposal_collaborators(cursor, n=20):
    cursor.execute("SELECT proposal_id FROM Proposal")
    proposal_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT researcher_id FROM Researcher")
    researcher_ids = set([row[0] for row in cursor.fetchall()])  # Use a set for unique researcher IDs

    for proposal_id in proposal_ids:
        collaborators = random.sample(list(researcher_ids), min(len(researcher_ids), random.randint(5, 15)))  # Convert set to list here
        for collaborator_id in collaborators:
            cursor.execute(
                "INSERT INTO ProposalCollaborator (proposal_id, collaborator_id) VALUES (?, ?)",
                (proposal_id, collaborator_id)
            )

def insert_reviewers(cursor, n=10):
    cursor.execute("SELECT researcher_id FROM Researcher ORDER BY RANDOM() LIMIT ?", (n,))
    reviewer_ids = [row[0] for row in cursor.fetchall()]

    for reviewer_id in reviewer_ids:
        cursor.execute(
            "INSERT INTO Reviewer (reviewer_id) VALUES (?)",
            (reviewer_id,)
        )

def insert_review_assignments(cursor, n=10):
    cursor.execute("SELECT reviewer_id FROM Reviewer")
    reviewer_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT proposal_id, competition_id FROM Proposal")
    proposal_info = cursor.fetchall()

    for _ in range(n):
        proposal_id, competition_id = random.choice(proposal_info)
        deadline = (datetime.now() + timedelta(days=random.randint(30, 90))).date()
        cursor.execute(
            "INSERT INTO ReviewAssignment (competition_id, reviewer_id, proposal_id, review_deadline, review_submitted) VALUES (?, ?, ?, ?, ?)",
            (competition_id, random.choice(reviewer_ids), proposal_id, deadline, random.choice([True, False]))
        )

def insert_conflicts_of_interest(cursor, n=10):
    cursor.execute("SELECT reviewer_id FROM Reviewer")
    reviewer_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT researcher_id FROM Researcher")
    researcher_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        cursor.execute(
            "INSERT INTO ConflictOfInterest (reviewer_id, conflicted_researcher_id) VALUES (?, ?)",
            (random.choice(reviewer_ids), random.choice(researcher_ids))
        )

def insert_meetings(cursor, n=10):
    for _ in range(n):
        meeting_date = (datetime.now() + timedelta(days=random.randint(1, 365))).date()
        cursor.execute(
            "INSERT INTO Meeting (meeting_date) VALUES (?)",
            (meeting_date,)
        )

def insert_meeting_participations(cursor, n=10):
    cursor.execute("SELECT meeting_id FROM Meeting")
    meeting_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT competition_id FROM Competition")
    competition_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT reviewer_id FROM Reviewer")
    reviewer_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        cursor.execute(
            "INSERT INTO MeetingParticipation (meeting_id, competition_id, reviewer_id) VALUES (?, ?, ?)",
            (random.choice(meeting_ids), random.choice(competition_ids), random.choice(reviewer_ids))
        )

def fill_database():
    conn = sqlite3.connect('research_grant_council.db')
    cursor = conn.cursor()

    insert_organizations(cursor)
    insert_researchers(cursor)
    insert_competitions(cursor)
    insert_proposals(cursor)
    insert_proposal_collaborators(cursor, n=20)  # Adjusted to ensure more participants
    insert_reviewers(cursor)
    insert_review_assignments(cursor)
    insert_conflicts_of_interest(cursor)
    insert_meetings(cursor)
    insert_meeting_participations(cursor)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fill_database()
    print("Database filled with realistic data successfully.")
