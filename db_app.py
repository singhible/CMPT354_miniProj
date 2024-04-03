import argparse
import sqlite3

conn = sqlite3.connect('council.db')
cursor = conn.cursor()

def view_table_contents(table_name):
    """
    Fetches and displays all contents from the specified table.

    Parameters:
        table_name (str): The name of the table to view.
    """
    query = f"SELECT * FROM {table_name}"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error fetching data from {table_name}:", e)

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

def check_reviewer_limit(proposal_id):
    """
    Check if adding another reviewer would exceed the limit of 3 reviewers per proposal.
    """
    cursor.execute("SELECT COUNT(*) FROM ReviewAssignment WHERE proposal_id = ?", (proposal_id,))
    count = cursor.fetchone()[0]
    return count < 3

def fetch_eligible_reviewers(proposal_id):
    """
    Fetches reviewers who are not in conflict with the proposal and have reviewed less than three proposals.

    Parameters:
        proposal_id (int): The ID of the proposal to find eligible reviewers for.

    Returns:
        list: A list of tuples containing eligible reviewer IDs and names.
    """
    cursor.execute("""
    SELECT r.reviewer_id, res.first_name || ' ' || res.last_name AS name
    FROM Reviewer r
    JOIN Researcher res ON r.reviewer_id = res.researcher_id
    WHERE r.reviewer_id NOT IN (
        SELECT reviewer_id FROM ReviewAssignment WHERE proposal_id = ?
    )
    AND r.reviewer_id NOT IN (
        SELECT coi.reviewer_id 
        FROM ConflictOfInterest coi
        WHERE coi.conflicted_researcher_id IN (
            SELECT principle_investigator_id FROM Proposal WHERE proposal_id = ?
            UNION
            SELECT collaborator_id FROM ProposalCollaborator WHERE proposal_id = ?
        )
    )
    AND (
        SELECT COUNT(*) 
        FROM ReviewAssignment ra 
        WHERE ra.reviewer_id = r.reviewer_id
    ) < 3;
    """, (proposal_id, proposal_id,proposal_id))
    results = cursor.fetchall()
    for result in results:
        print(f"ID: {result[0]}, Name: {result[1]}")
    return [result[0] for result in results]

def assign_reviewers(proposal_id):
    """
    Assign up to 3 reviewers to review a specific grant application, input one by one.
    """
    print("Fetching eligible reviewers for the proposal...")
    eligible_reviewers = fetch_eligible_reviewers(proposal_id)
    
    if not eligible_reviewers:
        print("No eligible reviewers available for this proposal.")
        return

    reviewers_assigned = 0
    while reviewers_assigned < 3 and check_reviewer_limit(proposal_id):
        reviewer_id = input("Enter reviewer ID to assign (or 'done' to finish): ")
        if reviewer_id.lower() == 'done':
            break
        try:
            reviewer_id = int(reviewer_id)
        except ValueError:
            print("Please enter a valid integer ID or 'done'.")
            continue

        if reviewer_id not in eligible_reviewers:
            print("This reviewer is not eligible or already assigned.")
            continue

        try:
            cursor.execute("INSERT INTO ReviewAssignment (proposal_id, reviewer_id) VALUES (?, ?)", (proposal_id, reviewer_id))
            conn.commit()
            reviewers_assigned += 1
            print(f"Reviewer {reviewer_id} assigned successfully.")
        except sqlite3.Error as e:
            print("Error assigning reviewer:", e)
            conn.rollback()

    if reviewers_assigned == 3:
        print("Maximum number of reviewers assigned.")
    elif not check_reviewer_limit(proposal_id):
        print("This proposal has reached the maximum number of reviewers.")

def find_proposals_to_review(name):
    """
    Find the proposal(s) a user needs to review.

    Parameters:
        name (str): The name of the reviewer.

    Returns:
        list: A list of tuples containing proposal IDs and competition titles to be reviewed by the user.
    """
    cursor.execute("""
        SELECT p.proposal_id, c.competition_title
        FROM Proposal p
        JOIN ReviewAssignment ra ON p.proposal_id = ra.proposal_id
        JOIN Reviewer r ON ra.reviewer_id = r.reviewer_id
        JOIN Researcher res ON r.reviewer_id = res.researcher_id
        JOIN Competition c ON p.competition_id = c.competition_id
        WHERE res.first_name || ' ' || res.last_name = ?
    """, (name,))
    return cursor.fetchall()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Application for Research Grant Council")
    parser.add_argument("--view", help="View the contents of a specified database table", metavar="TABLE_NAME")

    args = parser.parse_args()
    if args.view:
        view_table_contents(args.view)
    else:
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

        print("\nTask 5: Assign reviewers to review a specific grant application")
        proposal_id = int(input("Enter the proposal ID to assign reviewers to: "))
        assign_reviewers(proposal_id)
            
        print("\nTask 6: Find the proposal(s) a user needs to review")
        name = input("Enter reviewer's name: ")
        proposals_to_review = find_proposals_to_review(name)
        print(proposals_to_review)

conn.close()
