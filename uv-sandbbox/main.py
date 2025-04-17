#!/usr/bin/env python

# import werkzeug


class Configuration:
    def __init__(self, *, site_url: str, org_name: str):
        self.site = site_url
        self.org_name = org_name

class Configuration2:
    def __init__(self, *, site_url: str, org_name: str):
        self.site = site_url
        self.org_name = org_name

def library_function(site, org, repo, branch, commit_sha):
    print(f"{site} {org} {repo} {branch} {commit_sha}")


def wrapper(config, *args, **kwargs):
    return library_function(config.site, config.org_name, *args, **kwargs)


def main():
    print("Hello from uv-sandbbox!")
    config = Configuration(site_url="localhost", org_name="foo-org")
    wrapper(config, "myrepo", "mybranch", "1234567")
    # config2 = Configuration2("localhost", "foo-org")
    # wrapper(config2, "myrepo", "mybranch", "1234567")


if __name__ == "__main__":
    main()
