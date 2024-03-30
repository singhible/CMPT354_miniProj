import random
import sqlite3


def generate_sample_data():
    # Generate sample data for Researcher table
    researchers = [(f'Researcher{i}', f'Lastname{i}', f'researcher{i}@example.com') for i in range(1, 11)]

    # Generate sample data for Organization table
    organizations = [(f'Organization{i}', f'Address{i}') for i in range(1, 6)]

    # Generate sample data for Competition table
    competitions = [(1000 + i, f'Competition {i}', f'Description {i}', random.choice(['Healthcare', 'Technology', 'Environment']), 
                     random.choice(['Open', 'Closed']), '2024-12-31') for i in range(1, 6)]

    # Generate sample data for Proposal table
    proposals = [(random.uniform(1000, 50000), random.randint(1, 5), random.randint(1, 10), random.choice(['Submitted', 'Under Review', 'Rejected', 'Approved']), 
                  random.uniform(500, 50000), '2024-12-01') for _ in range(10)]

    # Generate sample data for ProposalCollaborator table
    proposal_collaborators = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(20)]

    return researchers, organizations, competitions, proposals, proposal_collaborators

def insert_sample_data():
    # Connect to the database
    conn = sqlite3.connect('research_grant_council.db')
    cursor = conn.cursor()

    # Generate sample data
    researchers, organizations, competitions, proposals, proposal_collaborators = generate_sample_data()

    # Insert sample data into tables
    cursor.executemany('INSERT INTO Researcher (first_name, last_name, email) VALUES (?, ?, ?)', researchers)
    cursor.executemany('INSERT INTO Organization (organization_name, organization_address) VALUES (?, ?)', organizations)
    cursor.executemany('INSERT INTO Competition (competition_number, competition_title, competition_description, competition_area, competition_status, competition_deadline) VALUES (?, ?, ?, ?, ?, ?)', competitions)
    cursor.executemany('INSERT INTO Proposal (requested_amount, competition_id, principle_investigator_id, proposal_status, awarded_amount, awarded_date) VALUES (?, ?, ?, ?, ?, ?)', proposals)
    cursor.executemany('INSERT INTO ProposalCollaborator (proposal_id, collaborator_id) VALUES (?, ?)', proposal_collaborators)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_sample_data()
    print("Sample data inserted successfully.")
