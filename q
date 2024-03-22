[0;1;31m●[0m rspm.service - Gunicorn instance to serve myproject
     Loaded: loaded (/etc/systemd/system/rspm.service; disabled; vendor preset: enabled)
     Active: [0;1;31mfailed[0m (Result: exit-code) since Thu 2023-10-12 17:51:55 UTC; 5s ago
    Process: 70972 ExecStart=/home/hpcnerajnan/RSPM/flask/bin/gunicorn --workers 3 --bind unix:application.sock -m 007 wsgi:app [0;1;31m(code=exited, status=200/CHDIR)[0m
   Main PID: 70972 (code=exited, status=200/CHDIR)

Oct 12 17:51:55 arcrspmdev systemd[1]: Started Gunicorn instance to serve myproject.
Oct 12 17:51:55 arcrspmdev systemd[70972]: [0;1;31m[0;1;39m[0;1;31mrspm.service: Changing to the requested working directory failed: No such file or directory[0m
Oct 12 17:51:55 arcrspmdev systemd[70972]: [0;1;31m[0;1;39m[0;1;31mrspm.service: Failed at step CHDIR spawning /home/hpcnerajnan/RSPM/flask/bin/gunicorn: No such file or directory[0m
Oct 12 17:51:55 arcrspmdev systemd[1]: [0;1;39m[0;1;31m[0;1;39mrspm.service: Main process exited, code=exited, status=200/CHDIR[0m
Oct 12 17:51:55 arcrspmdev systemd[1]: [0;1;38;5;185m[0;1;39m[0;1;38;5;185mrspm.service: Failed with result 'exit-code'.[0m
