import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('research_database.db')
cursor = conn.cursor()

# Task 1: Find all competitions open at a user-specified month with at least one large proposal
def find_open_competitions(month):
    cursor.execute("""
        SELECT c.competition_id, c.competition_title
        FROM Competition c
        WHERE strftime('%m', c.competition_deadline) = ? 
        AND c.competition_status = 'Open' 
        AND EXISTS (
            SELECT 1 FROM Proposal p 
            WHERE p.competition_id = c.competition_id 
            AND (p.requested_amount > 20000 OR 
                 (SELECT COUNT(*) FROM ProposalCollaborator pc 
                  WHERE pc.proposal_id = p.proposal_id) > 10)
        )
    """, (month,))
    return cursor.fetchall()

# Task 2: Find proposal(s) requesting the largest amount of money in a user-specified area
def find_largest_amount_proposal(area):
    cursor.execute("""
        SELECT p.proposal_id, MAX(p.requested_amount) AS max_requested_amount
        FROM Proposal p
        JOIN Competition c ON p.competition_id = c.competition_id
        WHERE c.competition_area = ?
    """, (area,))
    return cursor.fetchall()

# Task 3: Find proposals submitted before a user-specified date that are awarded the largest amount of money
def find_largest_awarded_proposals(date):
    cursor.execute("""
        SELECT p.proposal_id, MAX(p.awarded_amount) AS max_awarded_amount
        FROM Proposal p
        WHERE p.awarded_date < ?
    """, (date,))
    return cursor.fetchall()

# Task 4: Output the average requested/awarded discrepancy for a user-specified area
def average_discrepancy(area):
    cursor.execute("""
        SELECT AVG(ABS(p.requested_amount - p.awarded_amount)) AS avg_discrepancy
        FROM Proposal p
        JOIN Competition c ON p.competition_id = c.competition_id
        WHERE c.competition_area = ?
    """, (area,))
    return cursor.fetchone()[0]

# Task 5: Assign reviewers to review a specific grant application
def assign_reviewers(proposal_id):
    # Code to assign reviewers goes here
    pass

# Task 6: Find the proposal(s) a user needs to review
def find_proposals_to_review(name):
    cursor.execute("""
        SELECT p.proposal_id, p.proposal_title
        FROM Proposal p
        JOIN ReviewAssignment ra ON p.proposal_id = ra.proposal_id
        JOIN Reviewer r ON ra.reviewer_id = r.reviewer_id
        WHERE r.first_name || ' ' || r.last_name = ?
    """, (name,))
    return cursor.fetchall()

# Sample usage of the functions
if __name__ == "__main__":
    # Task 1
    print("Task 1: Find open competitions with at least one large proposal in a specific month")
    month = input("Enter month (MM): ")
    open_competitions = find_open_competitions(month)
    print(open_competitions)

    # Task 2
    print("\nTask 2: Find proposal(s) requesting the largest amount of money in a specific area")
    area = input("Enter area: ")
    largest_amount_proposal = find_largest_amount_proposal(area)
    print(largest_amount_proposal)

    # Task 3
    print("\nTask 3: Find proposals submitted before a specific date that are awarded the largest amount of money")
    date = input("Enter date (YYYY-MM-DD): ")
    largest_awarded_proposals = find_largest_awarded_proposals(date)
    print(largest_awarded_proposals)

    # Task 4
    print("\nTask 4: Output the average requested/awarded discrepancy for a specific area")
    area = input("Enter area: ")
    avg_discrepancy = average_discrepancy(area)
    print("Average discrepancy:", avg_discrepancy)

    # Task 5
    print("\nTask 5: Assign reviewers to review a specific grant application (not implemented)")

    # Task 6
    print("\nTask 6: Find the proposal(s) a user needs to review")
    name = input("Enter reviewer's name: ")
    proposals_to_review = find_proposals_to_review(name)
    print(proposals_to_review)

# Close the connection
conn.close()

