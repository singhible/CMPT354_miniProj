import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()

# Generate data for Organizations
organizations = [
    (fake.company(), fake.address().replace('\n', ', ')) for _ in range(10)
]

# Generate data for Researchers
researchers = [
    (i, fake.first_name(), fake.last_name(), fake.ascii_free_email(), random.randint(1, 10)) for i in range(1, 21)
]

# Generate data for Competitions
competitions = [
    (i, random.randint(1000, 9999), fake.bs(), fake.sentence(), fake.word(), random.choice(['Open', 'Closed']), (datetime.now() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')) for i in range(1, 11)
]

# Generate data for Proposals
proposals = [
    (i, round(random.uniform(5000, 50000), 2), random.randint(1, 10), random.randint(1, 20), random.choice(['Submitted', 'Awarded', 'Not Awarded']), None if i % 2 == 0 else round(random.uniform(20000, 50000), 2), (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d') if i % 2 != 0 else None) for i in range(1, 11)
]

# Generate data for Proposal Collaborators
proposal_collaborators = [
    (i, random.randint(1, 20)) for i in range(1, 11) for _ in range(random.randint(5, 15))
]

# Generate data for Reviewers
reviewers = [
    (i,) for i in range(1, 11)
]

# Generate data for Review Assignments
review_assignments = [
    (random.randint(1, 10), i, random.randint(1, 10), (datetime.now() + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d'), random.choice([True, False])) for i in range(1, 11)
]

# Generate data for Conflicts of Interest
conflicts_of_interest = [
    (i, random.randint(1, 20), random.randint(1, 20)) for i in range(1, 11)
]

# Generate data for Meetings
meetings = [
    ((datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),) for _ in range(10)
]

# Generate data for Meeting Participations
meeting_participations = [
    (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for _ in range(10)
]

# Combine all data into a single dictionary for easy access
data = {
    "organizations": organizations,
    "researchers": researchers,
    "competitions": competitions,
    "proposals": proposals,
    "proposal_collaborators": proposal_collaborators,
    "reviewers": reviewers,
    "review_assignments": review_assignments,
    "conflicts_of_interest": conflicts_of_interest,
    "meetings": meetings,
    "meeting_participations": meeting_participations,
}

print(data)