from urllib.parse import urlparse

def generate_short_url(original_url):
    parsed_url = urlparse(original_url)
    domain_parts = parsed_url.netloc.split('.')
    if len(domain_parts) > 2 and domain_parts[0] != 'www':
        return domain_parts[0][:4] + domain_parts[-2][:4] + domain_parts[-1][:4]
    elif len(domain_parts) > 1:
        return domain_parts[-2][:4] + domain_parts[-1][:4]
    else:
        return domain_parts[0][:8]
