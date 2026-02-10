from pathlib import Path

from models import Party, Duration, InformationCapacity, Security
from models import Cookie, RawCookie, Website, WebsiteCollection
from utils import is_cookie_writing, load_rank_domain_map, format_output

output_dir = Path("./output")
output_dir.mkdir(parents=True, exist_ok=True)


# V1 

V1_WEBSITES_FOLDER = "./dataset/V1-Violating-Websites"
V1_WEBSITES_DOMAIN = "./dataset/v1.txt"

v1_websites = WebsiteCollection()
v1_rank_domain = load_rank_domain_map(V1_WEBSITES_DOMAIN)
v1_output_file = output_dir / "v1.txt"

path = Path(V1_WEBSITES_FOLDER)

for filename in path.iterdir():
    with open(filename, 'r') as file:
        rank_id = str(filename).replace(V1_WEBSITES_FOLDER[2:]+"/", "").split(".")[0]
        domain = v1_rank_domain.get(int(rank_id))
        website = v1_websites.get_or_create(rank_id, domain)
        for line in file:
            if is_cookie_writing(line.strip()):
                raw_string = line.strip().split(",consent_compliance,")[3]
                website.add_cookie(raw_string)

with open(v1_output_file, "a") as file:
  for website in v1_websites.websites.values():
    file.write(format_output(website)+"\n")


# Non-V1

NON_V1_WEBSITES_FOLDER = "./dataset/Non-V1-Websites"
NON_V1_WEBSITES_DOMAIN = "./dataset/non-v1.txt"

non_v1_websites = WebsiteCollection()
non_v1_rank_domain = load_rank_domain_map(NON_V1_WEBSITES_DOMAIN)
non_v1_output_file = output_dir / "non_v1.txt"

path = Path(NON_V1_WEBSITES_FOLDER)

for filename in path.iterdir():
    with open(filename, 'r') as file:
        rank_id = str(filename).replace(NON_V1_WEBSITES_FOLDER[2:]+"/", "").split(".")[0]
        domain = non_v1_rank_domain.get(int(rank_id))
        website = non_v1_websites.get_or_create(rank_id, domain)
        for line in file:
            if is_cookie_writing(line.strip()):
                raw_string = line.strip().split(",consent_compliance,")[3]
                website.add_cookie(raw_string)

with open(non_v1_output_file, "a") as file:
  for website in non_v1_websites.websites.values():
    file.write(format_output(website)+"\n")
