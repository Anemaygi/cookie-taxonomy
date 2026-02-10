from pathlib import Path

def is_cookie_writing(event):
  chunks = event.split(",consent_compliance,")
  if int(chunks[0]) == 2:
    return False
  return True


def load_rank_domain_map(path):
    rank_to_domain = {}
    with open(path, "r") as file:
        for line in file:
            rank, domain = line.strip().split(",", 1)
            rank_to_domain[int(rank)] = domain
    return rank_to_domain


def format_output(website):
    return f"{website.rank_id},{website.domain},{website.get_severity()},{len(website.cookies)}"