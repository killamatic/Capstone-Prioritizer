class MockDatabaseManager:
    def __init__(self):
        # In-memory storage instead of a real database connection
        self.users = {}
        self.events = []
        self.user_id_counter = 1
        self.event_id_counter = 1

    def add_user(self, username, password_hash):
        user_id = self.user_id_counter
        self.users[user_id] = {'id': user_id, 'username': username, 'password_hash': password_hash}
        self.user_id_counter += 1
        return user_id

    def get_user_by_username(self, username):
        for user_id, user_data in self.users.items():
            if user_data['username'] == username:
                return (user_data['id'], user_data['username'], user_data['password_hash'])
        return None

    def add_event(self, user_id, name, priority_level, due_date):
        event_id = self.event_id_counter
        self.events.append({
            'id': event_id,
            'user_id': user_id,
            'name': name,
            'priority_level': priority_level,
            'due_date': due_date
        })
        self.event_id_counter += 1
        return event_id

    def get_user_events(self, user_id, sort_by='priority_level', sort_order='DESC'):
        # Sort logic for the mock data
        user_events = [event for event in self.events if event['user_id'] == user_id]
        
        # Simple sorting logic
        reverse = (sort_order.upper() == 'DESC')
        sorted_events = sorted(user_events, key=lambda x: x.get(sort_by, 0), reverse=reverse)
        
        # Convert to tuple format to match real DB output for consistency
        return [(e['id'], e['user_id'], e['name'], None, e['priority_level'], e['due_date'], 0, None) for e in sorted_events]