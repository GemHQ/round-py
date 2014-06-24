import bitvault

client = bitvault.client("http://localhost:8998/")
auth = bitvault.authed_client(url="http://localhost:8998",
        email="foo@bar.com", password="baz")

