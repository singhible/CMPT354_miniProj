import sqlite3


def create_database():
    conn = sqlite3.connect('research_grant_council.db')
    cursor = conn.cursor()

    # Create tables with constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Researcher (
            researcher_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            organization_id INTEGER,
            FOREIGN KEY (organization_id) REFERENCES Organization(organization_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Organization (
            organization_id INTEGER PRIMARY KEY,
            organization_name TEXT NOT NULL,
            organization_address TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Competition (
            competition_id INTEGER PRIMARY KEY,
            competition_number INTEGER UNIQUE NOT NULL,
            competition_title TEXT NOT NULL,
            competition_description TEXT,
            competition_area TEXT,
            competition_status TEXT,
            competition_deadline DATE,
            CHECK (competition_deadline >= DATE('now'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Proposal (
            proposal_id INTEGER PRIMARY KEY,
            requested_amount DECIMAL(15, 2) NOT NULL,
            competition_id INTEGER,
            principle_investigator_id INTEGER,
            proposal_status TEXT,
            awarded_amount DECIMAL(15, 2),
            awarded_date DATE,
            FOREIGN KEY (competition_id) REFERENCES Competition(competition_id) ON DELETE CASCADE,
            FOREIGN KEY (principle_investigator_id) REFERENCES Researcher(researcher_id),
            CHECK (requested_amount > 0)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProposalCollaborator (
            proposal_id INTEGER,
            collaborator_id INTEGER,
            PRIMARY KEY (proposal_id, collaborator_id),
            FOREIGN KEY (proposal_id) REFERENCES Proposal(proposal_id) ON DELETE CASCADE,
            FOREIGN KEY (collaborator_id) REFERENCES Researcher(researcher_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reviewer (
            reviewer_id INTEGER PRIMARY KEY,
            FOREIGN KEY (reviewer_id) REFERENCES Researcher(researcher_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReviewAssignment (
            review_assignment_id INTEGER PRIMARY KEY,
            competition_id INTEGER,
            reviewer_id INTEGER,
            proposal_id INTEGER,
            review_deadline DATE,
            review_submitted BOOLEAN,
            FOREIGN KEY (competition_id) REFERENCES Competition(competition_id) ON DELETE CASCADE,
            FOREIGN KEY (reviewer_id) REFERENCES Reviewer(reviewer_id),
            FOREIGN KEY (proposal_id) REFERENCES Proposal(proposal_id),
            CHECK (review_deadline >= DATE('now'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ConflictOfInterest (
            conflict_id INTEGER PRIMARY KEY,
            reviewer_id INTEGER,
            conflicted_researcher_id INTEGER,
            FOREIGN KEY (reviewer_id) REFERENCES Reviewer(reviewer_id),
            FOREIGN KEY (conflicted_researcher_id) REFERENCES Researcher(researcher_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Meeting (
            meeting_id INTEGER PRIMARY KEY,
            meeting_date DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MeetingParticipation (
            meeting_id INTEGER,
            competition_id INTEGER,
            reviewer_id INTEGER,
            PRIMARY KEY (meeting_id, competition_id, reviewer_id),
            FOREIGN KEY (meeting_id) REFERENCES Meeting(meeting_id) ON DELETE CASCADE,
            FOREIGN KEY (competition_id) REFERENCES Competition(competition_id),
            FOREIGN KEY (reviewer_id) REFERENCES Reviewer(reviewer_id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
