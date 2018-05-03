venv/bin/activate: requirements.txt
	test -f venv/bin/activate || virtualenv -p /usr/bin/python3 venv
	. venv/bin/activate ;\
	pip install -r requirements.txt
	touch venv/bin/activate  # update so it's as new as requirements.txt

.PHONY: run
run: venv/bin/activate
	. venv/bin/activate ; \
	FLASK_APP=app.py python3 -m flask run --host=0.0.0.0

.PHONY: run_production
run_production:
	# environment will already be configured with requirements
	gunicorn app:app
