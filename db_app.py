import sqlite3

conn = sqlite3.connect('research_database.db')
cursor = conn.cursor()

def find_open_competitions(month):
    """
    Find all competitions open at a user-specified month, which already have at least one submitted large proposal.
    
    Parameters:
        month (str): The month in MM format.

    Returns:
        list: A list of tuples containing competition IDs and titles.
    """
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

def find_largest_amount_proposal(area):
    """
    Find proposal(s) requesting the largest amount of money in a user-specified area.

    Parameters:
        area (str): The research area.

    Returns:
        list: A list of tuples containing proposal IDs and the largest requested amount.
    """
    cursor.execute("""
        SELECT p.proposal_id, MAX(p.requested_amount) AS max_requested_amount
        FROM Proposal p
        JOIN Competition c ON p.competition_id = c.competition_id
        WHERE c.competition_area = ?
    """, (area,))
    return cursor.fetchall()

def find_largest_awarded_proposals(date):
    """
    Find proposals submitted before a user-specified date that are awarded the largest amount of money.

    Parameters:
        date (str): The date in YYYY-MM-DD format.

    Returns:
        list: A list of tuples containing proposal IDs and the largest awarded amount.
    """
    cursor.execute("""
        SELECT p.proposal_id, MAX(p.awarded_amount) AS max_awarded_amount
        FROM Proposal p
        WHERE p.awarded_date < ?
    """, (date,))
    return cursor.fetchall()

def average_discrepancy(area):
    """
    Output the average requested/awarded discrepancy for a user-specified area.

    Parameters:
        area (str): The research area.

    Returns:
        float: The average discrepancy.
    """
    cursor.execute("""
        SELECT AVG(ABS(p.requested_amount - p.awarded_amount)) AS avg_discrepancy
        FROM Proposal p
        JOIN Competition c ON p.competition_id = c.competition_id
        WHERE c.competition_area = ?
    """, (area,))
    return cursor.fetchone()[0]

def assign_reviewers(proposal_id, reviewer_ids):
    """
    Assign reviewers to review a specific grant application.

    Parameters:
        proposal_id (int): The ID of the proposal to be reviewed.
        reviewer_ids (list): A list of reviewer IDs to be assigned to review the proposal.

    Returns:
        bool: True if reviewers are successfully assigned, False otherwise.
    """
    try:
        # Remove any existing review assignments for the proposal
        cursor.execute("DELETE FROM ReviewAssignment WHERE proposal_id = ?", (proposal_id,))
        
        # Assign reviewers to review the proposal
        for reviewer_id in reviewer_ids:
            cursor.execute("INSERT INTO ReviewAssignment (proposal_id, reviewer_id) VALUES (?, ?)", (proposal_id, reviewer_id))
        
        # Commit the changes
        conn.commit()
        return True
    except sqlite3.Error as e:
        print("Error assigning reviewers:", e)
        conn.rollback()
        return False

def find_proposals_to_review(name):
    """
    Find the proposal(s) a user needs to review.

    Parameters:
        name (str): The name of the reviewer.

    Returns:
        list: A list of tuples containing proposal IDs and titles to be reviewed by the user.
    """
    cursor.execute("""
        SELECT p.proposal_id, p.proposal_title
        FROM Proposal p
        JOIN ReviewAssignment ra ON p.proposal_id = ra.proposal_id
        JOIN Reviewer r ON ra.reviewer_id = r.reviewer_id
        WHERE r.first_name || ' ' || r.last_name = ?
    """, (name,))
    return cursor.fetchall()

if __name__ == "__main__":
    print("Task 1: Find open competitions with at least one large proposal in a specific month")
    month = input("Enter month (MM): ")
    open_competitions = find_open_competitions(month)
    print(open_competitions)

    print("\nTask 2: Find proposal(s) requesting the largest amount of money in a specific area")
    area = input("Enter area: ")
    largest_amount_proposal = find_largest_amount_proposal(area)
    print(largest_amount_proposal)

    print("\nTask 3: Find proposals submitted before a specific date that are awarded the largest amount of money")
    date = input("Enter date (YYYY-MM-DD): ")
    largest_awarded_proposals = find_largest_awarded_proposals(date)
    print(largest_awarded_proposals)

    print("\nTask 4: Output the average requested/awarded discrepancy for a specific area")
    area = input("Enter area: ")
    avg_discrepancy = average_discrepancy(area)
    print("Average discrepancy:", avg_discrepancy)

    print("\nTask 5: Assign reviewers to review a specific grant application (not implemented)")

    print("\nTask 6: Find the proposal(s) a user needs to review")
    name = input("Enter reviewer's name: ")
    proposals_to_review = find_proposals_to_review(name)
    print(proposals_to_review)

conn.close()
