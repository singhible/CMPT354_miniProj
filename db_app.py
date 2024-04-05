import argparse
import sqlite3
from datetime import datetime

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

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
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
        reviewer_id_input = input("Enter reviewer ID to assign (or 'done' to finish): ")
        if reviewer_id_input.lower() == 'done':
            break
        try:
            reviewer_id = int(reviewer_id_input)
            if reviewer_id not in eligible_reviewers:
                print("This reviewer is not eligible or already assigned.")
                continue
            cursor.execute("INSERT INTO ReviewAssignment (proposal_id, reviewer_id) VALUES (?, ?)", (proposal_id, reviewer_id))
            conn.commit()
            reviewers_assigned += 1
            print(f"Reviewer {reviewer_id} assigned successfully.")
        except ValueError:
            print("Please enter a valid integer ID or 'done'.")
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

def main_menu():
    while True:
        print("\nChoose an option:")
        print("1. Find open competitions with at least one large proposal in a specific month")
        print("2. Find proposal(s) requesting the largest amount of money in a specific area")
        print("3. Find proposal(s) submitted before a specific date that are awarded the largest amount of money")
        print("4. Output the average requested/awarded discrepancy for a specific area")
        print("5. Assign reviewers to review a specific grant application")
        print("6. Find the proposal(s) a user needs to review")
        print("7. View Table Contents")
        print("0. Exit")
        choice = input("> ")

        if choice == "0":
            break
        elif choice == "1":
            month = input("Enter month (MM): ")
            if month.isdigit() and len(month) == 2 and 1 <= int(month) <= 12:
                open_competitions = find_open_competitions(month)
                if open_competitions:  # This checks if the list is not empty
                    for competition in open_competitions:
                        print(competition)
                else:
                    print("No competitions found for this month.")
            else:
                print("Please enter a valid month in MM format (e.g., '03' for March).")

        elif choice == "2":
            area = input("Enter area: ")
            largest_amount_proposal = find_largest_amount_proposal(area)
            if largest_amount_proposal and largest_amount_proposal[0][0] is not None:
                for proposal in largest_amount_proposal:
                    print(proposal)
            else:
                print("No proposals found for the specified area.")

        elif choice == "3":

            date = input("Enter date (YYYY-MM-DD): ")
            if validate_date(date):
                largest_awarded_proposals = find_largest_awarded_proposals(date)
                if largest_awarded_proposals and largest_awarded_proposals[0][0] is not None:
                    for proposals in largest_awarded_proposals:
                        print(proposals)
                else:
                    print("No awarded proposals exist.")
            else:
                print("Please enter the date in YYYY-MM-DD format.")

        elif choice == "4":

            area = input("Enter area: ")
            avg_discrepancy = average_discrepancy(area)
            if average_discrepancy != 0:
                print("Average discrepancy:", avg_discrepancy)
            else:
                print("There is either no average discrepancy for the specified area or the input area is non-existent")

        elif choice == "5":
            proposal_id_input = input("Enter the proposal ID to assign reviewers to: ")
            try:
                proposal_id = int(proposal_id_input)
            except ValueError:
                print("Please enter a valid integer for the proposal ID.")

            assign_reviewers(proposal_id)

        elif choice == "6":
            name = input("Enter reviewer's name: ")
            proposals_to_review = find_proposals_to_review(name)
            if (proposals_to_review is not None):
                print(proposals_to_review)
            else:
                print("Either no proposals to review or no such reviewer")

        elif choice == "7":
            table_name = input("Enter the table name to view its contents: ")
            view_table_contents(table_name)
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()
    conn.close()
