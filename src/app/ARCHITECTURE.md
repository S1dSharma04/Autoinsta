# Layer dependency rules

Dependencies point inward only. A layer may import anything to its right;
never anything to its left.

core  ←  domain  ←  application  ←  api
                 ↖               ↖  workers
domain  ←  infrastructure

Concretely:
- core/            imports nothing from this project.
- domain/          imports core only. No FastAPI, no SQLAlchemy, no aio-pika,
                    no httpx. If you're importing a third-party library here
                    that isn't a pure-Python data structure helper, stop.
- application/     imports domain, core. Depends on domain's ABCs
                    (repository interfaces), never on infrastructure's
                    concrete classes.
- infrastructure/  imports domain, core, and third-party libraries freely.
                    The only layer allowed to know Postgres/Redis/RabbitMQ
                    exist.
- api/             imports application, core. Thin: parse request, call one
                    service, shape response. No business logic here.
- engine/          imports domain, core. Not infrastructure. Pure algorithm.
- workers/         imports everything. It's a composition root, like main.py.

Enforced by import-linter — see importlinter.ini. `python -m importlinter`
fails the build if this file and reality disagree.