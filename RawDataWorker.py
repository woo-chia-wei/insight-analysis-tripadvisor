from Repository import Repository
from TripAdvisorProfile import extract_profile

class RawDataWorker:

    def write_raw_users(self, soups):
        data = []
        for soup in soups:
            data.append(extract_profile(soup))
        repo = Repository()
        repo.write_raw_users(data)