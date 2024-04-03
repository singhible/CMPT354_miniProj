import sqlite3

data = {'organizations': [('Harrison Inc', '5304 Williams Corners Apt. 897, Port Courtneyview, WI 81398'), 
                          ('Ramos, Lewis and Perry', '274 Fisher Crescent Suite 941, Cynthiaborough, WV 15122'), 
                          ('Johnson-Pittman', '74282 Carrie Plaza, Garymouth, GU 76171'), 
                          ('Gonzalez-Carr', '063 Jones Mountain, West Deborah, VT 69658'), 
                          ('Beard-Ford', '323 Amanda Shoal, Schneiderview, AZ 68238'), 
                          ('Herrera-Robinson', '21843 Sarah Summit, Jamesstad, GA 79680'), 
                          ('Palmer-Harmon', 'USNS Howard, FPO AA 89449'), 
                          ('Johnson-Thomas', '1568 Ronnie Mountain Apt. 630, Bensonstad, OK 38524'), 
                          ('Garcia Group', '495 Navarro Stream Suite 078, New Aprilland, MS 07023'), 
                          ('Haley Inc', '98578 Mcdonald Viaduct, Lake Joshua, MH 10514')], 
                          
        'researchers': [(1, 'Daniel', 'Webb', 'campbellcynthia@hotmail.com', 10), 
                        (2, 'Robert', 'Barry', 'michelle79@hotmail.com', 5), 
                        (3, 'James', 'Shaw', 'joshuacallahan@hotmail.com', 3), 
                        (4, 'Shannon', 'Johnson', 'bryan38@yahoo.com', 8), 
                        (5, 'Joseph', 'Carney', 'fjackson@hotmail.com', 3), 
                        (6, 'Michael', 'Huff', 'ballen@gmail.com', 8), 
                        (7, 'Diane', 'Phillips', 'richardfranklin@hotmail.com', 2), 
                        (8, 'Stephanie', 'Frost', 'johnsonmichelle@hotmail.com', 5), 
                        (9, 'William', 'Mendoza', 'chad36@yahoo.com', 2), 
                        (10, 'Christopher', 'Green', 'onelson@yahoo.com', 10), 
                        (11, 'Robert', 'Clark', 'scott93@yahoo.com', 1), 
                        (12, 'Andrew', 'Rosales', 'ifisher@hotmail.com', 4), 
                        (13, 'Thomas', 'Turner', 'john38@gmail.com', 1), 
                        (14, 'Joshua', 'Young', 'moyerwesley@hotmail.com', 8), 
                        (15, 'Nathan', 'Smith', 'johnsonstephanie@hotmail.com', 3), 
                        (16, 'Adam', 'Wang', 'maryfoster@hotmail.com', 3), 
                        (17, 'Laurie', 'Ramirez', 'christine39@gmail.com', 2), 
                        (18, 'Donald', 'Banks', 'phillip96@yahoo.com', 8), 
                        (19, 'Zachary', 'Scott', 'timothywong@gmail.com', 5), 
                        (20, 'Kerri', 'Sandoval', 'todd89@yahoo.com', 4)], 
                        
        'competitions': [(1, 4115, 'Innovative Renewable Energy Systems', 'Exploring new technologies for sustainable energy generation.', 'Renewable Energy', 'Closed', '2024-06-17'), 
                         (2, 2783, 'Cross-Platform Software Development', 'Enhancing software interoperability across various platforms.', 'Software Engineering', 'Open', '2024-06-28'), 
                         (3, 1410, 'Back-End Solutions for Data Management', 'Developing scalable back-end systems for effective data handling.', 'Data Science', 'Open', '2024-07-24'), 
                         (4, 9926, 'Improving Healthcare through Technology', 'Using technology to advance medical care and patient management.', 'Healthcare Technology',  'Open', '2024-08-08'), 
                         (5, 3656, 'E-Learning Platforms and Digital Education', 'Creating intuitive e-learning experiences for digital education.', 'Educational Technology', 'Closed', '2024-06-20'), 
                         (6, 1089, 'Sustainable Urban Development', 'Urban planning strategies for sustainable and resilient cities.', 'Urban Sustainability', 'Closed', '2024-10-06'), 
                         (7, 3079, 'Cloud Services and E-Commerce', 'Developing scalable cloud services for e-commerce platforms.', 'Cloud Computing', 'Closed', '2024-07-14'), 
                         (8, 5423, 'Advancements in Artificial Intelligence', 'Exploring new frontiers in AI research and applications.', 'Artificial Intelligence', 'Open', '2024-11-12'), 
                         (9, 5210, 'Digital Security and Privacy', 'Enhancing digital security measures and privacy protocols.', 'Cybersecurity', 'Open', '2024-08-26'), 
                         (10, 9498, 'Blockchain in Financial Services', 'Leveraging blockchain technology for secure financial transactions.', 'Blockchain Technology', 'Closed', '2025-01-13')], 
                             
        'proposals': [(1, 46573.85, 4, 15, 'Awarded', 23570.85, '2024-04-18'), 
                      (2, 45712.97, 2, 16, 'Not Awarded', None, None), 
                      (3, 46828.23, 8, 10, 'Awarded', 40181.62, '2024-04-17'), 
                      (4, 14084.68, 10, 1, 'Not Awarded', None, None), 
                      (5, 37669.87, 1, 1, 'Awarded', 21917.11, '2024-04-17'), 
                      (6, 38907.68, 9, 19, 'Submitted', None, None), 
                      (7, 34256.05, 7, 1, 'Awarded', 39228.61, '2024-04-03'), 
                      (8, 8107.5, 8, 7, 'Submitted', None, None), 
                      (9, 41316.97, 3, 3, 'Awarded', 42910.24, '2024-04-06'), 
                      (10, 39536.04, 1, 18, 'Submitted', None, None)], 
                      
        'proposal_collaborators': [(1, 8), (1, 17), (1, 7), (1, 16), (1, 2), (1, 10), (1, 12), (1, 7), (1, 1), (1, 16), (1, 7), (1, 1), (2, 20), (2, 8), (2, 7), (2, 15), (2, 6), (2, 18), (2, 10), (2, 1), (2, 13), (2, 11), (2, 2), (2, 1), (2, 16), (2, 6), (2, 6), (3, 20), (3, 4), (3, 5), (3, 9), (3, 12), (3, 9), (3, 2), (3, 3), (3, 2), (3, 18), (3, 12), (3, 13), (4, 17), (4, 18), (4, 20), (4, 2), (4, 10), (4, 10), (4, 20), (5, 4), (5, 5), (5, 3), (5, 2), (5, 12), (5, 9), (5, 19), (5, 11), (5, 12), (6, 7), (6, 16), (6, 11), (6, 9), (6, 20), (6, 17), (6, 8), (6, 8), (6, 5), (6, 15), (6, 18), (6, 18), (6, 18), (7, 4), (7, 7), (7, 12), (7, 3), (7, 7), (7, 8), (7, 9), (7, 9), (7, 15), (7, 3), (8, 15), (8, 14), (8, 3), (8, 8), (8, 19), (8, 18), (8, 15), (8, 18), (9, 15), (9, 19), (9, 2), (9, 3), (9, 8), (9, 11), (9, 3), (9, 16), (9, 12), (9, 8), (9, 17), (9, 12), (9, 14), (10, 17), (10, 20), (10, 12), (10, 7), (10, 1), (10, 8), (10, 10), (10, 2), (10, 5), (10, 18), (10, 19), (10, 8), (10, 2), (10, 12)], 
        
        'reviewers': [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)], 
        
        'review_assignments': [(3, 1, 3, '2024-05-31', True), 
                               (6, 2, 5, '2024-06-15', True), 
                               (4, 3, 7, '2024-06-05', True), 
                               (5, 4, 3, '2024-04-30', False), 
                               (2, 5, 7, '2024-06-06', False), 
                               (3, 6, 7, '2024-06-03', True), 
                               (5, 7, 5, '2024-05-27', True), 
                               (4, 8, 2, '2024-06-14', True), 
                               (8, 9, 10, '2024-05-08', False), 
                               (1, 10, 3, '2024-06-26', False)], 
                               
        'conflicts_of_interest': [(1, 13, 14), (2, 16, 3), (3, 8, 11), (4, 7, 17), (5, 18, 8), (6, 7, 4), (7, 17, 8), (8, 20, 6), (9, 2, 1), (10, 2, 19)], 
        
        'meetings': [('2024-05-19',), ('2025-01-24',), ('2024-05-23',), ('2024-10-23',), ('2024-09-29',), ('2024-12-15',), ('2024-09-08',), ('2024-04-21',), ('2024-08-14',), ('2025-02-03',)], 
        
        'meeting_participations': [(4, 2, 1), (1, 5, 8), (5, 1, 5), (1, 6, 5), (1, 7, 5), (8, 1, 8), (6, 3, 4), (9, 9, 6), (4, 2, 9), (10, 4, 4)]}

def fill_database(db_name='council.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Insert data into Organization
    cursor.executemany("INSERT INTO Organization (organization_name, organization_address) VALUES (?, ?)", data['organizations'])
    
    # Insert data into Researcher
    cursor.executemany("INSERT INTO Researcher (researcher_id, first_name, last_name, email, organization_id) VALUES (?, ?, ?, ?, ?)", data['researchers'])
    
    # Insert data into Competition
    cursor.executemany("INSERT INTO Competition (competition_id, competition_number, competition_title, competition_description, competition_area, competition_status, competition_deadline) VALUES (?, ?, ?, ?, ?, ?, ?)", data['competitions'])
    
    # Insert data into Proposal
    cursor.executemany("INSERT INTO Proposal (proposal_id, requested_amount, competition_id, principle_investigator_id, proposal_status, awarded_amount, awarded_date) VALUES (?, ?, ?, ?, ?, ?, ?)", data['proposals'])
    unique_proposal_collaborators = list(set(data['proposal_collaborators']))
    # Insert data into ProposalCollaborator
    cursor.executemany("INSERT INTO ProposalCollaborator (proposal_id, collaborator_id) VALUES (?, ?)", unique_proposal_collaborators)
    
    # Insert data into Reviewer
    cursor.executemany("INSERT INTO Reviewer (reviewer_id) VALUES (?)", data['reviewers'])
    
    # Insert data into ReviewAssignment
    cursor.executemany(
        "INSERT INTO ReviewAssignment (competition_id, reviewer_id, proposal_id, review_deadline, review_submitted) VALUES (?, ?, ?, ?, ?)", 
        data['review_assignments']
    )    
    # Insert data into ConflictOfInterest
    cursor.executemany("INSERT INTO ConflictOfInterest (conflict_id, reviewer_id, conflicted_researcher_id) VALUES (?, ?, ?)", data['conflicts_of_interest'])
    
    # Insert data into Meeting
    cursor.executemany("INSERT INTO Meeting (meeting_date) VALUES (?)", data['meetings'])
    
    # Insert data into MeetingParticipation
    cursor.executemany("INSERT INTO MeetingParticipation (meeting_id, competition_id, reviewer_id) VALUES (?, ?, ?)", data['meeting_participations'])

    conn.commit()
    conn.close()
    print("Data inserted successfully.")

if __name__ == "__main__":
    fill_database()
