.PHONY: test test-fast test-slow lint verify clean

test:
	python3 -m unittest discover -s tests -t . -q

test-fast:
	python3 -m unittest tests.test_loans tests.test_policy -q

test-slow:
	python3 -m unittest tests.test_integration -q

lint:
	python3 -m compileall -q library tests

verify: lint test-fast

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} +
