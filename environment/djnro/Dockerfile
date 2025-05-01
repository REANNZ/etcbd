FROM python:3.10

#libpg-dev needed for psycopg2 compilation
#this pkg is included in python:2.7, but make the statement explicit anyway
RUN apt-get update -q && apt-get -qq -y install libpq-dev \
# install locales
  && apt-get -q -y install locales \
# temporary: install utils
  && apt-get -q -y install --no-install-recommends lsof vim less file \
# cleanup: remove apt-get temporary files
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /djnro
WORKDIR /djnro

#pull in the djnro code, install it's dependencies
RUN git clone --depth 1 https://github.com/REANNZ/djnro.git ./ \
 && git checkout master
COPY requirements-additional.txt run-kml-refresh.sh uwsgi.ini ./
COPY content /
RUN pip install -r requirements.txt -r requirements-optional.txt -r requirements-additional.txt \
    # pre-compile PYC files
    && python -m compileall -q /djnro \
    # leaner image: remove wheels cached by pip
    && rm -rf /root/.cache/pip
COPY local_settings.py djnro/
# populate STATIC_DIR with static files from all modules
# Needs to be a separate RUN - after local_settings.py are copied in
RUN ./manage.py collectstatic --noinput --verbosity 0
EXPOSE 3031
CMD ["/envwrap.sh", "/startup.sh", "uwsgi", "/djnro/uwsgi.ini"]
